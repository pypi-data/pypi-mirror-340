import xarray as xr
from intake.source.base import DataSource

import oceantide

from intake_oceantide import __version__


class OceantideSource(DataSource):
    """Opens tide constituents dataset with oceantide accessor.

    Args:
        urlpath (str): URL path of the tide constituents dataset.
        file_format (str): Oceantide file format so appropriate reader can be chosen.
        metadata (dict): Catalog metadata
        kwargs: Further parameters are passed to the oceantide reader.

    """
    name = "oceantide"
    container = "xarray"
    version = __version__
    partition_access = True

    def __init__(self, urlpath, file_format="oceantide", metadata=None, **kwargs):
        super().__init__(metadata=metadata)
        self.urlpath = urlpath
        self.file_format = file_format
        self.kwargs = kwargs
        self._ds = None

    def _open_tide_cons(self):
        """Open the tide constituents dataset."""
        # Oceantide format has changed in favor of split real/imag vars
        if self.file_format == "oceantide":
            reader = xr.open_zarr
        else:
            reader = getattr(oceantide, f"read_{self.file_format}")
        self._ds = reader(self.urlpath, **self.kwargs)

    def to_dask(self):
        self._open_tide_cons()
        return self._ds

    read = to_dask

    discover = read

    read_chunked = to_dask
