"""Utility functions."""
import numpy as np


def unique_times(ds):
    """Remove duplicate times from dataset."""
    _, index = np.unique(ds["time"], return_index=True)
    return ds.isel(time=index)