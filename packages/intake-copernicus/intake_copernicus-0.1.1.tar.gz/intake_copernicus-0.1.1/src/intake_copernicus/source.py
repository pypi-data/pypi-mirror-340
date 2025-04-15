"""Copernicus datasources."""
import logging
from intake.source.base import Schema, DataSource


logger = logging.getLogger(__name__)


class CopernicusMarineSource(DataSource):
    """Copernicus dataset from the Copernicus Marine API.

    Parameters
    ----------
    dataset_id: str
        The ID of the dataset.
    username: str
        Username for authentication, if required.
    password: str
        Password for authentication, if required.
    service: str, optional
        Force the use of a specific service (timeseries, geoseries or OpenDAP).
    dataset_version: bool, optional
        Force the use of a specific dataset version.
    variables: list, optional
        List of variable names to be loaded from the dataset.
    minimum_longitude: float, optional
        The minimum longitude for subsetting the data.
    maximum_longitude: float, optional
        The maximum longitude for subsetting the data.
    minimum_latitude: float, optional
        The minimum latitude for subsetting the data.
    maximum_latitude: float, optional
        The maximum latitude for subsetting the data.
    minimum_depth: float, optional
        The minimum depth for subsetting the data.
    maximum_depth: float, optional
        The maximum depth for subsetting the data.
    start_datetime: str, optional
        The start datetime for temporal subsetting.
    end_datetime: str, optional
        The end datetime for temporal subsetting.
    squeeze: bool, optional
        Convenience to squeeze out all the dimensions of size 1.
    **kwargs:
        Further keyword arguments to be passed to copernicusmarine.open_dataset.

    Notes
    -----
    Check the full list of kwargs in the `open_dataset` function documentation.

    """

    name = "copernicus_marine"

    def __init__(
        self,
        dataset_id: str,
        username: str = None,
        password: str = None,
        service: str = None,
        dataset_version: bool = None,
        dataset_part: bool = None,
        variables: list = None,
        minimum_longitude: float = None,
        maximum_longitude: float = None,
        minimum_latitude: float = None,
        maximum_latitude: float = None,
        minimum_depth: float = None,
        maximum_depth: float = None,
        start_datetime: str = None,
        end_datetime: str = None,
        squeeze: bool = False,
        metadata: dict = {},
        **kwargs,
    ):
        super().__init__(metadata=metadata)
        self.dataset_id = dataset_id
        self.username = username
        self.password = password
        self.service = service
        self.dataset_version = dataset_version
        self.dataset_part = dataset_part
        self.variables = variables
        self.minimum_longitude = minimum_longitude
        self.maximum_longitude = maximum_longitude
        self.minimum_latitude = minimum_latitude
        self.maximum_latitude = maximum_latitude
        self.minimum_depth = minimum_depth
        self.maximum_depth = maximum_depth
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.squeeze = squeeze
        self._ds = None
        self.kwargs = kwargs

    def _get_schema(self):
        """Make schema object, which embeds xarray object and some details"""
        if self._ds is None:
            self.to_dask()

            metadata = {
                "dims": dict(self._ds.dims),
                "data_vars": {k: list(self._ds[k].coords) for k in self._ds.data_vars.keys()},
                "coords": tuple(self._ds.coords.keys()),
            }
            metadata.update(self._ds.attrs)
            self._schema = Schema(
                datashape=None,
                dtype=None,
                shape=None,
                npartitions=None,
                extra_metadata=metadata)
        return self._schema

    def to_dask(self) -> None:
        from copernicusmarine import open_dataset

        self._ds = open_dataset(
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            dataset_part=self.dataset_part,
            username=self.username,
            password=self.password,
            variables=self.variables,
            minimum_longitude=self.minimum_longitude,
            maximum_longitude=self.maximum_longitude,
            minimum_latitude=self.minimum_latitude,
            maximum_latitude=self.maximum_latitude,
            minimum_depth=self.minimum_depth,
            maximum_depth=self.maximum_depth,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            service=self.service,
            **self.kwargs,
        )
        if self.squeeze:
            self._ds = self._ds.squeeze().reset_coords()

        return self._ds

    read = to_dask

    discover = read

    read_chunked = to_dask


if __name__ == "__main__":
    import os

    source = CopernicusMarineSource(
        dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
        username=os.getenv("COPERNICUS_USER"),
        password=os.getenv("COPERNICUS_KEY"),
        service="timeseries",
        # minimum_depth=0,
        # maximum_depth=0,
        # squeeze=True,
    )
    dset_reanalysis = source.to_dask()

    source = CopernicusMarineSource(
        dataset_id="cmems_mod_glo_phy_myint_0.083deg_P1D-m",
        username=os.getenv("COPERNICUS_USER"),
        password=os.getenv("COPERNICUS_KEY"),
        service="timeseries",
        # minimum_depth=0,
        # maximum_depth=0,
        # squeeze=True,
    )
    dset_nrt = source.to_dask()

    # import ipdb; ipdb.set_trace()