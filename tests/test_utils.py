import pytest
import numpy as np
from datetime import datetime
from plotdarn.utils import antipode, sun_position, sun_longitude, cross_dateline, scale_velocity, points_around_boundary
from plotdarn.locations import north_pole, Location


def test_antipode():
    assert antipode(-72) == 108


def test_antipode_pos():
    assert antipode(72) == -108


def test_antipode_lat():
    assert antipode(20, axis='latitude') == -20


def test_antipode_lat_neg():
    assert antipode(-20, axis='latitude') == 20


def test_antipode_zero():
    assert antipode(0) == 180


def test_antipode_unknown_type():
    with pytest.raises(ValueError):
        antipode(20, axis='anything')


def test_sun_position():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    azimuth = sun_position(north_pole, time)
    assert azimuth == 330.3365208965877


def test_sun_position_2():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    loc = Location(80.2281362381121, -72.41454428382853)
    assert sun_position(loc, time) == 262.2580553157149


def test_sun_position_strtime():
    time = "2012-06-15 22:02"
    assert sun_position(north_pole, time) == 330.3365208965877


def test_sun_position_strtime_timezone():
    time = "2012-06-15 22:02Z"
    assert sun_position(north_pole, time) == 330.3365208965877


def test_sun_position_str_unknown():
    time = "Not a valid time"
    with pytest.raises(ValueError):
        sun_position(north_pole, time)


def test_sun_position_not_a_loc():
    loc = (22, 30)
    time = "2012-06-15 22:02Z"
    with pytest.raises(AttributeError):
        sun_position(loc, time)


def test_sun_longitude():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    assert sun_longitude(time) == -150.3343248158402


def test_sun_longitude_midday():
    time = datetime(year=2012, month=6, day=15, hour=12, minute=0)
    lon = sun_longitude(time)
    assert -1 <= lon <= 1
    assert sun_longitude(time) == 0.1432130201462769


def test_sun_longitude_midnight():
    time = datetime(year=2012, month=6, day=15, hour=0, minute=0)
    lon = sun_longitude(time)
    assert lon >= 179 or lon <= -179
    assert sun_longitude(time) == -179.88355840312767


def test_sun_longitude_midday_leapyear():
    time = datetime(year=2020, month=6, day=4, hour=12, minute=0)
    lon = sun_longitude(time)
    assert -1 <= lon <= 1


def test_cross_dateline_crosses_neg_first():
    array = np.array([[80, -10], [80, -90], [80, -174], [82, 173], [82, 101], [81, 40]])
    expected = np.array([[82, 173], [82, 101], [81, 40], [80, -10], [80, -90], [80, -174]])
    np.testing.assert_array_equal(cross_dateline(array), expected)


def test_cross_dateline_crosses_pos_first():
    array = np.array([[80, 10], [80, 90], [80, 174], [82, -173], [82, -101], [81, -40]])
    expected = np.array([[82, -173], [82, -101], [81, -40], [80, 10], [80, 90], [80, 174]])
    np.testing.assert_array_equal(cross_dateline(array), expected)


def test_cross_dateline_crosses_uneven_lon():
    array = np.array([[80, 10], [83, 96], [80, 90], [80, 174], [82, -173], [82, -101], [81, -40]])
    expected = np.array([[82, -173], [82, -101], [81, -40], [80, 10], [83, 96], [80, 90], [80, 174]])
    np.testing.assert_array_equal(cross_dateline(array), expected)


def test_cross_dateline_not_crossing():
    array = np.array([[32, 143], [30, 175], [30, 135]])
    np.testing.assert_array_equal(cross_dateline(array), array)


def test_cross_dateline_not_crossing_large_gap():
    array = np.array([[80, -134], [42, -82], [84, 140], [80, 179]])
    np.testing.assert_array_equal(cross_dateline(array), array)


def test_cross_dateline_neg_first_closes():
    array = np.array([[80, -10], [80, -90], [80, -174], [82, 173], [82, 101], [81, 40]])
    expected = np.array([[80.97848832236156, 180], [82, 173], [82, 101], [81, 40],
                         [80, -10], [80, -90], [80, -174], [80.97848832236156, -180]])
    np.testing.assert_array_equal(cross_dateline(array, close=True), expected)


def test_cross_dateline_pos_first_closes():
    array = np.array([[80, 10], [80, 90], [80, 174], [82, -173], [82, -101], [81, -40]])
    expected = np.array([[80.97848832236156, -180], [82, -173], [82, -101], [81, -40],
                         [80, 10], [80, 90], [80, 174], [80.97848832236156, 180]])
    np.testing.assert_array_equal(cross_dateline(array, close=True), expected)


def test_scale_vel_1000():
    res = scale_velocity(1000, 0.2)
    assert res == 0.2


def test_scale_vel_500():
    res = scale_velocity(500, 0.2)
    assert res == 0.1


def test_scale_vel_2000():
    res = scale_velocity(2000, 0.2)
    assert res == 0.4


def test_scale_vel_1():
    res = scale_velocity(1, 0.2)
    assert res == 0.0002


def test_scale_vel_1_len3():
    res = scale_velocity(1, 3)
    assert res == 0.003


def test_scale_vel_2_len3():
    res = scale_velocity(2, 3)
    assert res == 0.006


def test_scale_vel_array():
    res = scale_velocity(np.array([1, 2, 3, 5]))
    print(res)
    np.testing.assert_array_almost_equal(res, np.array([0.0002, 0.0004, 0.0006, 0.001]))


def test_scale_vel_list():
    res = scale_velocity([1, 2, 3, 4])
    np.testing.assert_array_almost_equal(res, np.array([0.0002, 0.0004, 0.0006, 0.0008]))


def test_points_inside_simple_outside():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside, outside = points_around_boundary([0], [0], bx, by)
    np.testing.assert_array_equal(inside, np.array([False]))
    np.testing.assert_array_equal(outside, np.array([True]))


def test_points_inside_simple_inside():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside, outside = points_around_boundary([1.5], [1.5], bx, by)
    np.testing.assert_array_equal(inside, np.array([True]))
    np.testing.assert_array_equal(outside, np.array([False]))


def test_points_inside_border():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside, outside = points_around_boundary([1], [1], bx, by)
    np.testing.assert_array_equal(inside, np.array([False]))
    np.testing.assert_array_equal(outside, np.array([True]))


def test_points_inside_border_radius():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside, outside = points_around_boundary([1], [1], bx, by, radius=0.1)
    np.testing.assert_array_equal(inside, np.array([True]))
    np.testing.assert_array_equal(outside, np.array([False]))


def test_points_inside_mulitple():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside, outside = points_around_boundary([1.1, 2, 1.5, 1.2], [1.1, 2.1, 1.5, 3], bx, by)
    np.testing.assert_array_equal(inside, np.array([True, False, True, False]))
    np.testing.assert_array_equal(outside, np.array([False, True, False, True]))


def test_points_inside_mulitple_array():
    bx = np.array([1, 2, 2, 1])
    by = np.array([1, 1, 2, 2])
    inside, outside = points_around_boundary(np.array([1.1, 2, 1.5, 1.2]), np.array([1.1, 2.1, 1.5, 3]), bx, by)
    np.testing.assert_array_equal(inside, np.array([True, False, True, False]))
    np.testing.assert_array_equal(outside, np.array([False, True, False, True]))
