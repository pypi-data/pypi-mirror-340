import asyncio
import os
from pathlib import Path

import typer
from typing_extensions import Annotated

from platzi import AsyncPlatzi

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def login():
    """
    Open a browser window to Login to Platzi.

    Usage:
        platzi login
    """
    asyncio.run(_login())


@app.command()
def logout():
    """
    Delete the Platzi session from the local storage.

    Usage:
        platzi logout
    """
    asyncio.run(_logout())


@app.command()
def download(
    url: Annotated[
        str,
        typer.Argument(
            help="The URL of the course to download",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        str,
        typer.Option(
            "--output", "-o",
            help="Ruta donde se guardará el contenido descargado",
            show_default=False,
        ),
    ] = None,
):
    """
    Download a Platzi course from the given URL.

    Arguments:
        url: str - The URL of the course to download.
        output_path: str - The path where the content will be saved.

    Usage:
        platzi download <url> [--output <path>]
        platzi download <url> [-o <path>]

    Example:
        platzi download https://platzi.com/cursos/fastapi-2023/
        platzi download https://platzi.com/cursos/fastapi-2023/ --output ~/Downloads/Cursos
        platzi download https://platzi.com/cursos/fastapi-2023/ -o ./Cursos
    """
    asyncio.run(_download(url, output_path))


async def _login():
    async with AsyncPlatzi() as platzi:
        await platzi.login()


async def _logout():
    async with AsyncPlatzi() as platzi:
        await platzi.logout()


async def _download(url: str, output_path: str = None):
    if output_path:
        # Convertir ~ a la ruta home del usuario
        if output_path.startswith('~'):
            output_path = os.path.expanduser(output_path)
        
        # Asegúrate de que la ruta sea absoluta
        output_path = os.path.abspath(output_path)
        
        # Crea la carpeta de destino si no existe
        Path(output_path).mkdir(parents=True, exist_ok=True)
    
    async with AsyncPlatzi() as platzi:
        await platzi.download(url, output_path=output_path)
