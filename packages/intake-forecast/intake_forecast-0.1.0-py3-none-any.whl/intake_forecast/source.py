"""Intake driver for cycle-based, zarr-based forecast data."""

import logging
from datetime import datetime, timedelta
from intake.source.base import DataSource
from intake.catalog.utils import coerce_datetime

logger = logging.getLogger(__name__)


def find_previous_cycle_time(time: datetime, cycle_period_hours: int) -> datetime:
    """Find the previous time in a cycle given the current time.

    Args:
        time (datetime): The current time
        cycle_period_hours (int): The cycle period in hours

    Returns:
        datetime: The previous time in the cycle

    """
    midnight = time.replace(hour=0, minute=0, second=0, microsecond=0)
    hours_passed = (time - midnight).total_seconds() / 3600
    cycles_passed = int(hours_passed / cycle_period_hours)
    return midnight + timedelta(hours=cycles_passed * cycle_period_hours)


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
