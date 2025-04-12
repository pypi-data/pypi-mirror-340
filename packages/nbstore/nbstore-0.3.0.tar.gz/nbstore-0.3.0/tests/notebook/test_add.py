from pathlib import Path

import pytest

from nbstore.notebook import Notebook
from nbstore.store import Store


@pytest.fixture(scope="module")
def nb(store: Store):
    return store.get_notebook("add.ipynb")


def test_add_delete(nb: Notebook):
    nb.add_data("add", "text/plain", "text")
    data = nb.get_data("add")
    assert data["text/plain"] == "text"
    nb.delete_data("add", "text/plain")
    data = nb.get_data("add")
    assert "text/plain" not in data


def test_language(nb: Notebook):
    assert nb.get_language() == "python"


def test_write(nb: Notebook, tmp_path: Path):
    path = tmp_path / "tmp.ipynb"
    nb.write(path)
    assert path.exists()
    nb2 = Notebook(path)
    data = nb2.get_mime_content("add")
    assert data
    assert data[0] == "image/png"


def test_cell_error(nb: Notebook):
    with pytest.raises(ValueError, match="Unknown identifier: unknown"):
        nb.get_cell("unknown")


def test_stream_none(nb: Notebook):
    assert nb.get_stream("add") is None


def test_data_empty(nb: Notebook):
    assert nb.get_data("empty") == {}


def test_source_include_identifier(nb: Notebook):
    source = nb.get_source("add", include_identifier=True)
    assert source.startswith("# #add\n")
