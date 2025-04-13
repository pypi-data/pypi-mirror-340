from __future__ import annotations

from typing import TYPE_CHECKING

from .logger import logger
from .markdown import iter_images

if TYPE_CHECKING:
    from collections.abc import Iterator

    from nbstore import Notebook, Store

    from .image import Image


def convert(markdown: str, store: Store) -> Iterator[str | Image]:
    for image in iter_images(markdown):
        if isinstance(image, str):
            yield image
        else:
            try:
                yield from convert_image(image, store)
            except ValueError:
                logger.warning(f"Could not convert {image.url}#{image.identifier}")
                yield image.markdown


def convert_image(image: Image, store: Store) -> Iterator[str | Image]:
    nb = store.get_notebook(image.url)

    if image.pop(".execute") and store.needs_execution(image.url):
        logger.info(f"Executing notebook: {nb.path}")
        nb.execute()

    if image.pop(".source"):
        yield from get_source(image, nb)
        return

    if has_cell := image.pop(".cell"):
        yield from get_source(image, nb)

    if mime_content := nb.get_mime_content(image.identifier):
        yield image.convert(*mime_content)

    elif not has_cell:
        yield from get_source(image, nb)


def get_source(image: Image, nb: Notebook) -> Iterator[str]:
    if source := nb.get_source(image.identifier):
        language = nb.get_language()
        yield f"```{{.{language}{image.attr}}}\n{source}\n```\n\n"
