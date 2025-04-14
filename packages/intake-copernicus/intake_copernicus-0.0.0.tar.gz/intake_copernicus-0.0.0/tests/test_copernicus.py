import os
from pathlib import Path
import intake
import pytest
import copernicusmarine

from intake_copernicus.source import CopernicusMarineSource


HERE = Path(__file__).parent


logged = copernicusmarine.login(
    username=os.getenv("COPERNICUS_USER", "dummy_user"),
    password=os.getenv("COPERNICUS_KEY", "dummy_key"),
    force_overwrite=True,
)


@pytest.mark.skipif(not logged, reason="COPERNICUS env variables not set")
def test_copernicus_marine_timeseries():
    source = CopernicusMarineSource(
        dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
        username=None,
        password=None,
        service="timeseries",
    )
    dset = source.to_dask()
    assert "uo" in dset


@pytest.mark.skipif(not logged, reason="COPERNICUS env variables not set")
def test_copernicus_marine_geoseries():
    source = CopernicusMarineSource(
        dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
        username=None,
        password=None,
        service="geoseries",
    )
    dset = source.to_dask()
    assert "uo" in dset


@pytest.mark.skipif(not logged, reason="COPERNICUS env variables not set")
def test_copernicus_marine_subset():
    source = CopernicusMarineSource(
        dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
        minimum_longitude=0,
        maximum_longitude=2,
        minimum_latitude=-1,
        maximum_latitude=1,
        minimum_depth=0,
        maximum_depth=1,
        start_datetime="2020-01-01",
        end_datetime="2020-01-02",
        username=None,
        password=None,
        service="geoseries",
    )
    dset = source.to_dask()
    assert "uo" in dset


@pytest.mark.skipif(not logged, reason="COPERNICUS env variables not set")
@pytest.mark.parametrize("dataset_id", ["cmems_mod_glo_phy_my_0.083deg_P1D-m"])
def test_catalog(dataset_id):
    cat = intake.open_catalog(HERE / "catalog.yml")
    dset = cat[dataset_id].to_dask()
    assert "uo" in dset