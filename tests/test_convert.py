import pytest
from plotdarn.convert import convert_mag_single, convert_mag_arr
from plotdarn.locations import north_pole
from datetime import datetime
import numpy as np


def test_convert_single():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    newloc = convert_mag_single(north_pole, time)
    assert newloc.lat == 80.2281362381121
    assert newloc.lon == -72.41454428382853


def test_convert_single_not_a_loc():
    with pytest.raises(AttributeError):
        convert_mag_single([20, 30], "2012")


def test_convert_single_not_a_datetime():
    time = "2012-06-15 22:02"
    res = convert_mag_single(north_pole, time)
    assert res.lat == 80.2281362381121
    assert res.lon == -72.41454428382853


def test_convert_single_strdate_timezone():
    time = "2012-06-15 22:02Z"
    res = convert_mag_single(north_pole, time)
    assert res.lat == 80.2281362381121
    assert res.lon == -72.41454428382853


def test_convert_single_unknown_date():
    time = "This can't be a time"
    with pytest.raises(ValueError):
        convert_mag_single(north_pole, time)


def test_convert_array():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    res = convert_mag_arr([north_pole.lat], [north_pole.lon], time)
    np.testing.assert_array_equal(res, np.array([[80.2281362381121, -72.41454428382853]]))


def test_convert_array_2vals():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    res = convert_mag_arr([north_pole.lat, north_pole.lat], [north_pole.lon, north_pole.lon], time)
    expected = np.array(
        [
            [80.2281362381121, -72.41454428382853],
            [80.2281362381121, -72.41454428382853]
        ]
    )
    np.testing.assert_array_equal(res, expected)


def test_convert_array_np_input():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    input_lat = np.array([north_pole.lat, north_pole.lat])
    input_lon = np.array([north_pole.lon, north_pole.lon])
    res = convert_mag_arr(input_lat, input_lon, time)
    expected = np.array(
        [
            [80.2281362381121, -72.41454428382853],
            [80.2281362381121, -72.41454428382853]
        ]
    )
    np.testing.assert_array_equal(res, expected)


def test_convert_array_single_input():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    with pytest.raises(TypeError):
        convert_mag_arr(north_pole.lat, north_pole.lon, time)


def test_convert_array_uneven():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    with pytest.raises(ValueError):
        convert_mag_arr([north_pole.lat, north_pole.lat], [north_pole.lon], time)


def test_convert_array_np_input_shape():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    input_lat = np.array([[north_pole.lat], [north_pole.lat]])
    input_lon = np.array([[north_pole.lon], [north_pole.lon]])
    with pytest.raises(ValueError):
        convert_mag_arr(input_lat, input_lon, time)
