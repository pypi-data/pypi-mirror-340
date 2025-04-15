"""Test for intake plugins."""
from pathlib import Path
import pytest
import intake


HERE = Path(__file__).parent


@pytest.fixture(scope="module")
def catalog():
    """Open intake catalog."""
    cat = intake.open_catalog(HERE / "catalog.yml")
    return cat


def test_open_oceantide(catalog):
    dset = catalog.oceantide_testing.to_dask()
    assert hasattr(dset, "tide")
