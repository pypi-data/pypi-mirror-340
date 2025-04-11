import logging
from typing import Optional
from datetime import datetime, timedelta
from intake.source.base import DataSource
from intake_xarray.xzarr import ZarrSource
from intake.catalog.utils import coerce_datetime

from intake_forecast.utils import find_previous_cycle_time, enhance


logger = logging.getLogger(__name__)


class ZarrForecastSource(DataSource):
    name = "zarr_forecast"

    def __init__(
        self,
        urlpath: str,
        cycle: datetime,
        cycle_period: int = 6,
        maxstepback: int = 4,
        open_zarr_kwargs: dict = {"storage_options": {"token": None}},
        storage_options: Optional[dict] = None,
        consolidated: Optional[bool] = None,
        metadata: dict = None,
    ):
        """Intake driver for cyclic zarr sources.

        Parameters
        ----------
        urlpath : str
            URL path template for zarr files
        cycle : datetime
            Cycle time
        cycle_period : int
            Cycle period in hours, it should be a positive factor of 24
        maxstepback : int
            Maximum number of cycles to step back when searching for past cycles
        open_zarr_kwargs : dict
            Keyword arguments for opening zarr files with xarray.open_zarr
        storage_options : Optional[dict], deprecated
            Legacy parameter for storage options for opening zarr files with
            xarray.open_zarr, it should now be provided in open_zarr_kwargs
        consolidated : Optional[bool], deprecated
            Legacy parameter for opening consolidated zarr files with
            xarray.open_zarr, it should now be provided in open_zarr_kwargs
        metadata : dict
            Metadata for the dataset

        """
        super().__init__(metadata=metadata)
        self.cycle = find_previous_cycle_time(coerce_datetime(cycle), cycle_period)
        self.cycle_period = cycle_period
        self.maxstepback = maxstepback
        self.open_zarr_kwargs = open_zarr_kwargs
        self._template = urlpath
        self._stepback = maxstepback
        # For backward compatibility with the old onzarr driver
        if storage_options is not None:
            self.open_zarr_kwargs["storage_options"] = storage_options
        if consolidated is not None:
            self.open_zarr_kwargs["consolidated"] = consolidated

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
        return enhance(ds, self.metadata)

    read = to_dask

    discover = read

    read_chunked = to_dask


class EnhancedZarrSource(ZarrSource):
    name = "zarr_enhanced"

    def __init__(self, **kwargs):
        """Zarr source with additional functionality specified from the metadata.

        Parameters
        ----------
        **kwargs
            Keyword arguments for the ZarrSource constructor

        """
        super().__init__(**kwargs)
        self.metadata = self.reader.metadata

    def to_dask(self):
        ds = super().to_dask()
        return enhance(ds, self.metadata)
