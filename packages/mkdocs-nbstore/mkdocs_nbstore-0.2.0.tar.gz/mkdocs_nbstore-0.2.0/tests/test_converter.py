from nbstore.store import Store

from mkdocs_nbstore.converter import convert
from mkdocs_nbstore.image import Image


def test_convert_cell(store: Store):
    markdown = "![a](matplotlib.ipynb){#matplotlib .cell}\n\na"
    it = convert(markdown, store)

    source = next(it)
    assert isinstance(source, str)
    assert source.startswith("```{.python}\n")

    image = next(it)
    assert isinstance(image, Image)

    text = next(it)
    assert isinstance(text, str)
    assert text == "\n\na"


def test_convert_source(store: Store):
    markdown = "![a](matplotlib.ipynb){#matplotlib .source}\n\na"
    it = convert(markdown, store)

    source = next(it)
    assert isinstance(source, str)
    assert source.startswith("```{.python}\n")

    text = next(it)
    assert isinstance(text, str)
    assert text == "\n\na"


def test_convert_exception(store: Store):
    markdown = "![a](matplotlib.ipynb){#invalid .c k=v}"
    it = convert(markdown, store)
    text = next(it)
    assert isinstance(text, str)
    assert text == markdown


def test_convert_image_stdout(store: Store):
    markdown = "![a](matplotlib.ipynb){#stdout}"
    it = convert(markdown, store)
    text = next(it)
    assert isinstance(text, str)
    assert text == "1"


def test_convert_execute(store: Store):
    nb = store.get_notebook("matplotlib.ipynb")
    nb.is_executed = False
    markdown = "![a](matplotlib.ipynb){#matplotlib .execute}"
    list(convert(markdown, store))
    assert nb.is_executed
