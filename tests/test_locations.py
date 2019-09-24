import pytest
from plotdarn.locations import Location


def test_location_create():
    loc = Location(20, 30)
    assert loc.lat == 20
    assert loc.lon == 30


def test_location_lat_wrong():
    with pytest.raises(ValueError):
        Location(120, 30)


def test_location_lon_wrong():
    with pytest.raises(ValueError):
        Location(20, 190)


def test_location_changed_lat():
    loc = Location(20, 30)
    with pytest.raises(ValueError):
        loc.lat = 120


def test_location_changed_lon():
    loc = Location(20, 30)
    with pytest.raises(ValueError):
        loc.lon = 190
