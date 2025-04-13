from mkdocs_nbstore.figure import Figure
from mkdocs_nbstore.markdown import Element


def test_figure():
    elem = Element("", "b", [".c", ".d"], {"k1": "v1 v2", "k2": "v3"})
    fig = Figure(elem, "alt", "a.ipynb")
    assert fig.markdown == '![alt](a.ipynb){#b .c .d k1="v1 v2" k2=v3}'
