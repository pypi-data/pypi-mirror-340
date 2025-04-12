import functools
import json
import os
import urllib.parse
from pathlib import Path

from playwright.async_api import BrowserContext, Page, async_playwright

from .collectors import get_course_title, get_draft_chapters, get_unit
from .constants import HEADERS, LOGIN_DETAILS_URL, LOGIN_URL, SESSION_FILE
from .helpers import hash_id, read_json, write_file, write_json
from .logger import Logger
from .m3u8 import m3u8_dl
from .models import ResourceType, TypeUnit, Unit, User
from .utils import Cache, download, progressive_scroll, slugify


def login_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        self = args[0]
        if not isinstance(self, AsyncPlatzi):
            Logger.error(f"{login_required.__name__} can only decorate Platzi class.")
            return
        if not self.loggedin:
            Logger.error("Login first!")
            return
        return await func(*args, **kwargs)

    return wrapper


def try_except_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        self = args[0]
        if not isinstance(self, AsyncPlatzi):
            Logger.error(
                f"{try_except_request.__name__} can only decorate Platzi class."
            )
            return

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if str(e):
                Logger.error(e)
        return

    return wrapper


class AsyncPlatzi:
    def __init__(self, headless=False):
        self.loggedin = False
        self.headless = headless
        self.user = None

    async def __aenter__(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        self._context = await self._browser.new_context(
            java_script_enabled=True,
            is_mobile=True,
        )

        try:
            await self._load_state()
        except Exception:
            pass

        await self._set_profile()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._context.close()
        await self._browser.close()
        await self._playwright.stop()

    @property
    async def page(self) -> Page:
        return await self._context.new_page()

    @property
    def context(self) -> BrowserContext:
        return self._context

    @try_except_request
    async def _set_profile(self) -> None:
        try:
            data = await self.get_json(LOGIN_DETAILS_URL)
            self.user = User(**data)
        except Exception:
            return

        if self.user.is_authenticated:
            self.loggedin = True
            Logger.info(f"Hi, {self.user.username}!")

    @try_except_request
    async def login(self) -> None:
        Logger.info("Please login, in the opened browser")
        Logger.info("You have to login manually, you have 2 minutes to do it")

        page = await self.page
        await page.goto(LOGIN_URL)
        try:
            avatar = await page.wait_for_selector(
                ".styles-module_Menu__Avatar__FTuh-",
                timeout=2 * 60 * 1000,
            )
            if avatar:
                self.loggedin = True
                await self._save_state()
                Logger.info("Logged in successfully")
        except Exception:
            raise Exception("Login failed")
        finally:
            await page.close()

    @try_except_request
    async def logout(self):
        SESSION_FILE.unlink(missing_ok=True)
        Logger.info("Logged out successfully")

    @try_except_request
    @login_required
    async def download(self, url: str, output_path: str = None, **kwargs):
        page = await self.page
        await page.goto(url)

        # course title
        course_title = await get_course_title(page)
        Logger.print(course_title, "[COURSE]")

        # download directory
        if output_path:
            DL_DIR = Path(output_path) / slugify(course_title)
        else:
            DL_DIR = Path("Platzi") / slugify(course_title)
        DL_DIR.mkdir(parents=True, exist_ok=True)

        # save page as mhtml
        await self.save_page(
            page,
            path=DL_DIR / "presentation.mhtml",
        )

        # iterate over chapters
        draft_chapters = await get_draft_chapters(page)
        for idx, draft_chapter in enumerate(draft_chapters, 1):
            Logger.info(f"Downloading {draft_chapter.name}")

            CHAP_DIR = DL_DIR / f"{idx:02}_{draft_chapter.slug}"
            CHAP_DIR.mkdir(parents=True, exist_ok=True)

            # iterate over units
            for jdx, draft_unit in enumerate(draft_chapter.units, 1):
                cache_hash = hash_id(draft_unit.url)
                cache_data = Cache.get(cache_hash)

                if cache_data:
                    unit = Unit.model_validate(cache_data)
                else:
                    unit = await get_unit(self.context, draft_unit.url)
                    Cache.set(cache_hash, unit.model_dump())

                file_name = f"{jdx:02}_{unit.slug}"

                # download video
                if unit.video:
                    dst = CHAP_DIR / f"{file_name}.mp4"
                    Logger.print(f"[{dst.name}]", "[DOWNLOADING]")
                    await m3u8_dl(unit.video.url, dst.as_posix(), headers=HEADERS)

                    if unit.video.subtitles_url:
                        dst = CHAP_DIR / f"{file_name}.vtt"
                        Logger.print(f"[{dst.name}]", "[DOWNLOADING]")
                        await download(unit.video.subtitles_url, dst)
                    
                    # Save description to markdown file if it exists
                    if unit.video.description:
                        dst = CHAP_DIR / f"{file_name}.md"
                        Logger.print(f"[{dst.name}]", "[DOWNLOADING]")
                        write_file(dst.as_posix(), unit.video.description)
                    
                    # Process resources (files) and readings
                    has_resources = unit.video.resources and len(unit.video.resources) > 0
                    has_readings = unit.video.recommended_readings and len(unit.video.recommended_readings) > 0
                    
                    # Create a single resources directory for both files and readings
                    if has_resources or has_readings:
                        # Create a resources folder for this unit
                        resources_dir = CHAP_DIR / f"{file_name}_resources"
                        resources_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Content for the resources markdown file
                        resources_md = ""
                        
                        # Process downloadable files first
                        if has_resources:
                            resources_md += "# Archivos de la clase\n\n"
                            
                            # Save each resource
                            for resource in unit.video.resources:
                                # Skip if not a file type resource
                                if resource.type != ResourceType.FILE:
                                    continue
                                    
                                # Get filename from URL or use resource name
                                parsed_url = urllib.parse.urlparse(resource.url)
                                file_path = urllib.parse.unquote(parsed_url.path)
                                file_name_from_url = os.path.basename(file_path)
                                
                                # Use resource name as filename if URL doesn't provide a useful one
                                if not file_name_from_url or file_name_from_url == "":
                                    file_name_from_url = slugify(resource.name) + ".pdf"
                                
                                resource_dst = resources_dir / file_name_from_url
                                Logger.print(f"[{resource_dst.name}]", "[DOWNLOADING RESOURCE]")
                                
                                try:
                                    # Download the resource
                                    await download(resource.url, resource_dst)
                                    
                                    # Add to markdown file
                                    resources_md += f"- [{resource.name}](./{file_name}_resources/{file_name_from_url})\n"
                                except Exception as e:
                                    Logger.print(f"Failed to download resource: {resource.name} - {str(e)}", "[WARNING]")
                                    # Add external link if download fails
                                    resources_md += f"- [{resource.name}]({resource.url}) (external link)\n"
                        
                        # Process recommended readings and add them to the same resources folder
                        if has_readings:
                            # Add a separator if we also have resources
                            if has_resources:
                                resources_md += "\n\n"
                                
                            resources_md += "# Lecturas recomendadas\n\n"
                            
                            # Add each reading as a link
                            for reading in unit.video.recommended_readings:
                                # Create an HTML file that redirects to the recommended reading
                                reading_file_name = f"link_to_{slugify(reading.name)}.html"
                                reading_file_path = resources_dir / reading_file_name
                                
                                # Create a simple HTML file with a redirect
                                redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url={reading.url}">
    <title>{reading.name}</title>
</head>
<body>
    <h1>Redireccionando a: {reading.name}</h1>
    <p>Si no eres redireccionado automáticamente, haz click <a href="{reading.url}">aquí</a>.</p>
</body>
</html>
"""
                                # Write the HTML file
                                Logger.print(f"[{reading_file_name}]", "[CREATING READING LINK]")
                                write_file(reading_file_path.as_posix(), redirect_html)
                                
                                # Add to resources markdown
                                resources_md += f"- [{reading.name}](./{file_name}_resources/{reading_file_name})\n"
                        
                        # Save the combined resources markdown file
                        resources_md_path = CHAP_DIR / f"{file_name}_resources.md"
                        write_file(resources_md_path.as_posix(), resources_md)
                

                # download lecture
                if unit.type == TypeUnit.LECTURE:
                    dst = CHAP_DIR / f"{file_name}.mhtml"
                    Logger.print(f"[{dst.name}]", "[DOWNLOADING]")
                    await self.save_page(unit.url, path=dst)

                # download quiz
                if unit.type == TypeUnit.QUIZ:
                    dst = CHAP_DIR / f"{file_name}.mhtml"
                    Logger.print(f"[{dst.name}]", "[DOWNLOADING]")
                    await self.save_page(unit.url, path=dst)

            print("=" * 100)

    @try_except_request
    async def save_page(self, src: str | Page, path: str = "source.mhtml"):
        if isinstance(src, str):
            page = await self.page
            await page.goto(src)
        else:
            page = src

        await progressive_scroll(page)

        try:
            client = await page.context.new_cdp_session(page)
            response = await client.send("Page.captureSnapshot")
            with open(path, "w", encoding="utf-8", newline="\n") as file:
                file.write(response["data"])
        except Exception:
            raise Exception("Error saving page as mhtml")

        if isinstance(src, str):
            await page.close()

    @try_except_request
    async def get_json(self, url: str) -> dict:
        page = await self.page
        await page.goto(url)
        content = await page.locator("pre").first.text_content()
        await page.close()
        return json.loads(content or "{}")

    async def _save_state(self):
        cookies = await self.context.cookies()
        write_json(SESSION_FILE, cookies)

    async def _load_state(self):
        SESSION_FILE.touch()
        cookies = read_json(SESSION_FILE)
        await self.context.add_cookies(cookies)
