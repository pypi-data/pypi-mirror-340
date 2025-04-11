"""Intake driver for cycle-based, zarr-based forecast data."""

import logging
from datetime import timedelta
from intake.source.base import DataSource
from intake.catalog.utils import coerce_datetime

from intake_forecast.utils import find_previous_cycle_time


logger = logging.getLogger(__name__)


class ZarrForecastSource(DataSource):
    name = "zarr_forecast"

    def __init__(
        self,
        urlpath,
        cycle,
        cycle_period=6,
        maxstepback=4,
        open_zarr_kwargs={"storage_options": {"token": None}},
        metadata=None,
    ):
        super().__init__(metadata=metadata)
        self.cycle = find_previous_cycle_time(coerce_datetime(cycle), cycle_period)
        self.cycle_period = cycle_period
        self.maxstepback = maxstepback
        self.open_zarr_kwargs = open_zarr_kwargs
        self._template = urlpath
        self._stepback = maxstepback

    def to_dask(self):
        import xarray as xr

        urlpath = self.cycle.strftime(self._template)
        try:
            ds = xr.open_zarr(urlpath, **self.open_zarr_kwargs)
        except FileNotFoundError as err:
            if self._stepback == 0:
                raise ValueError(
                    f"{urlpath} not found and maxstepback {self.maxstepback} reached"
                ) from err
            logger.warning(f"{urlpath} not found, stepping back {self.cycle_period}h")
            self.cycle -= timedelta(hours=self.cycle_period)
            self._stepback -= 1
            ds = self.to_dask()
        return ds

    read = to_dask

    discover = read

    read_chunked = to_dask
