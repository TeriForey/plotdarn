import pytest
from plotdarn.convert import convert_mag_single
from plotdarn.locations import Location, north_pole
from datetime import datetime


def test_convert_single():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    newloc = convert_mag_single(north_pole, time)
    assert newloc.lat == 80.2281362381121
    assert newloc.lon == -72.41454428382853


def test_convert_single_not_a_loc():
    with pytest.raises(AttributeError):
        convert_mag_single([20, 30], "2012")

