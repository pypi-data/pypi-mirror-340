import asyncio
import re
from pathlib import Path
from typing import Dict, List, Tuple

import aiofiles
import rnet
from bs4 import BeautifulSoup
from html2text import HTML2Text
from playwright.async_api import Page
from unidecode import unidecode

from .constants import SESSION_DIR
from .helpers import read_json, write_file, write_json


async def progressive_scroll(
    page: Page, time: float = 3, delay: float = 0.1, steps: int = 250
):
    await asyncio.sleep(3)  # delay to avoid rate limiting
    delta, total_time = 0.0, 0.0
    while total_time < time:
        await asyncio.sleep(delay)
        await page.mouse.wheel(0, steps)
        delta += steps
        total_time += delay


def get_course_slug(url: str) -> str:
    """
    Extracts the course slug from a Platzi course URL.

    Args:
        url (str): The Platzi course URL.

    Returns:
        str: The course slug.

    Raises:
        Exception: If the URL is not a valid Platzi course URL.
    """
    pattern = r"https://platzi\.com/cursos/([^/]+)/?"
    match = re.search(pattern, url)
    if not match:
        raise Exception("Invalid course url")
    return match.group(1)


def clean_string(text: str) -> str:
    """
    Cleans the input string by removing special characters and
    leading/trailing white spaces.

    Args:
        text (str): The input string to be cleaned.

    Returns:
        str: The cleaned string, with special characters removed and
        leading/trailing spaces stripped.
    """
    pattern = r"[ºª]|[^\w\s]"
    return re.sub(pattern, "", text).strip()


def slugify(text: str) -> str:
    """
    Slugify a string by removing special characters and
    leading/trailing white spaces, and replacing spaces with hyphens.

    Args:
        text (str): The input string to be slugified.
    Returns:
        str: The slugified string.
    """
    return unidecode(clean_string(text)).lower().replace(" ", "-")


def get_m3u8_url(content: str) -> str:
    pattern = r"https?://[^\s\"'}]+\.m3u8"
    matches = re.findall(pattern, content)

    if not matches:
        raise Exception("No m3u8 urls found")

    return matches[0]


def get_subtitles_url(content: str) -> str | None:
    pattern = r"https?://[^\s\"'}]+\.vtt"
    matches = re.findall(pattern, content)

    if not matches:
        return None

    return matches[0]


async def download(url: str, path: Path, **kwargs):
    overrides = kwargs.get("overrides", False)

    if not overrides and path.exists():
        return

    path.unlink(missing_ok=True)
    path.parent.mkdir(parents=True, exist_ok=True)

    client = rnet.Client(impersonate=rnet.Impersonate.Firefox135)
    response: rnet.Response = await client.get(url, **kwargs)

    try:
        if not response.ok:
            raise Exception("[Bad Response]")

        async with aiofiles.open(path.as_posix(), "wb") as file:
            async with response.stream() as streamer:
                async for chunk in streamer:
                    await file.write(chunk)

    except Exception as e:
        raise Exception(f"Error downloading file: [{path.name}]") from e

    finally:
        response.close()


class Cache:
    @classmethod
    def get(cls, id: str) -> dict | None:
        path = SESSION_DIR / f"{id}.json"
        try:
            return read_json(path.as_posix())
        except Exception:
            return None

    @classmethod
    def set(cls, id: str, content: dict) -> None:
        path = SESSION_DIR / f"{id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            write_json(path.as_posix(), content)
        except Exception:
            pass


def extract_video_description(html_content: str) -> Tuple[str, List[Dict], List[Dict]]:
    """
    Extract the video description, files and recommended readings from HTML content.
    
    Args:
        html_content (str): The HTML content containing the video description.
        
    Returns:
        Tuple[str, List[Dict], List[Dict]]: A tuple containing:
            - The extracted video description in markdown format
            - A list of class resources (files) with name and URL
            - A list of recommended readings with name and URL
    """
    try:
        # Configure html2text for clean markdown output
        h = HTML2Text()
        h.ignore_links = False
        h.body_width = 0  # Don't wrap text
        h.ignore_images = True
        h.unicode_snob = True
        
        description = ""
        resources = []
        readings = []
        
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the resources div that contains the description (exact class from example)
        resources_div = soup.find('div', class_=lambda c: c and 'Resources_Resources__Articlass__VDxzX' in c)
        
        if resources_div:
            # Extract the title (Resumen) for the markdown
            title_elem = resources_div.find('p', class_=lambda c: c and 'Resources_Resources__Articlass__title__' in c)
            title_text = title_elem.get_text() if title_elem else "Resumen"
            
            # Get the content div with the specific class from the example
            content_div = resources_div.find('div', class_=lambda c: c and 'Resources_Resources__Articlass__content__' in c)
            
            if content_div:
                # Remove "Seguir leyendo" button if it exists
                seguir_leyendo = content_div.find('button')
                if seguir_leyendo:
                    seguir_leyendo.decompose()
                
                # Convert the content div to markdown
                markdown_content = h.handle(str(content_div))
                
                # Ensure proper formatting of the title in markdown
                description = f"# {title_text}\n\n{markdown_content}"
        
        # Find the files section (using exact class from example)
        files_div = soup.find('div', class_=lambda c: c and 'Resources_Resources__files__Owpuc' in c)
        
        if files_div:
            # Process all sections in the files div
            sections = files_div.find_all('section', class_=lambda c: c and 'styles_SectionFL__8xjPc' in c)
            
            for section in sections:
                # Get section title
                title_elem = section.find('h4', class_=lambda c: c and 'styles_SectionFL__Title__' in c)
                section_title = title_elem.get_text().strip() if title_elem else ""
                
                # Find all links in this section
                links = section.find_all('a', href=True)
                
                for link in links:
                    # Determine file name from download attribute, title or text content
                    file_name = None
                    
                    # Check for title element inside the link
                    title_span = link.find('span', class_=lambda c: c and 'FilesAndLinks_Info__Title__' in c) or link.find('p', class_=lambda c: c and 'FilesAndLinks_Info__Title__' in c)
                    if title_span:
                        file_name = title_span.get_text().strip()
                    
                    # If no title found yet, try download attribute
                    if not file_name and link.get('download'):
                        file_name = link.get('download')
                    
                    # If still no name, use plain link text
                    if not file_name:
                        file_name = link.get_text().strip()
                    
                    # If we have a file name and URL
                    if file_name and link['href']:
                        if section_title == "Archivos de la clase":
                            resources.append({
                                "name": file_name,
                                "url": link['href'],
                                "type": "file"
                            })
                        elif section_title == "Lecturas recomendadas":
                            readings.append({
                                "name": file_name,
                                "url": link['href'],
                                "type": "link"
                            })
        
        return description, resources, readings
    except Exception as e:
        print(f"Error extracting video description: {str(e)}")
        return "", [], []
