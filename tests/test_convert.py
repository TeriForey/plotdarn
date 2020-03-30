import pytest
from plotdarn import convert
from plotdarn.locations import north_pole
from datetime import datetime
import numpy as np

NP_GLAT = 82.82981033739065
NP_GLON = -84.21565686001807
NP_MLAT = 83.73564264222507
NP_MLON = 169.7596236665287


def test_convert_single():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    newloc = convert.loc_mag_to_geo(north_pole, time)
    assert newloc.lat == NP_GLAT
    assert newloc.lon == NP_GLON


def test_convert_single_not_a_loc():
    with pytest.raises(AttributeError):
        convert.loc_mag_to_geo([20, 30], "2012-06-15 22:02")


def test_convert_single_not_a_datetime():
    time = "2012-06-15 22:02"
    res = convert.loc_mag_to_geo(north_pole, time)
    assert res.lat == NP_GLAT
    assert res.lon == NP_GLON


def test_convert_single_strdate_timezone():
    time = "2012-06-15 22:02Z"
    res = convert.loc_mag_to_geo(north_pole, time)
    assert res.lat == NP_GLAT
    assert res.lon == NP_GLON


def test_convert_single_unknown_date():
    time = "This can't be a time"
    with pytest.raises(ValueError):
        convert.loc_mag_to_geo(north_pole, time)


def test_convert_array():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    res = convert.arr_mag_to_geo([north_pole.lat], [north_pole.lon], time)
    np.testing.assert_array_equal(res, np.array([[NP_GLAT], [NP_GLON]]))


def test_convert_array_2vals():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    res = convert.arr_mag_to_geo([north_pole.lat, north_pole.lat], [north_pole.lon, north_pole.lon], time)
    expected = np.array(
        [
            [NP_GLAT, NP_GLAT],
            [NP_GLON, NP_GLON]
        ]
    )
    np.testing.assert_array_equal(res, expected)


def test_convert_array_np_input():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    input_lat = np.array([north_pole.lat, north_pole.lat])
    input_lon = np.array([north_pole.lon, north_pole.lon])
    res = convert.arr_mag_to_geo(input_lat, input_lon, time)
    expected = np.array(
        [
            [NP_GLAT, NP_GLAT],
            [NP_GLON, NP_GLON]
        ]
    )
    np.testing.assert_array_equal(res, expected)


def test_convert_array_single_input():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    with pytest.raises(TypeError):
        convert.arr_mag_to_geo(north_pole.lat, north_pole.lon, time)


def test_convert_array_uneven():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    with pytest.raises(ValueError):
        convert.arr_mag_to_geo([north_pole.lat, north_pole.lat], [north_pole.lon], time)


def test_convert_array_np_input_shape():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    input_lat = np.array([[north_pole.lat], [north_pole.lat]])
    input_lon = np.array([[north_pole.lon], [north_pole.lon]])
    with pytest.raises(ValueError):
        convert.arr_mag_to_geo(input_lat, input_lon, time)


def test_convert_geo_to_mag_loc():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    newloc = convert.loc_geo_to_mag(north_pole, time)
    assert newloc.lat == NP_MLAT
    assert newloc.lon == NP_MLON


def test_convert_single_g2m_not_a_loc():
    with pytest.raises(AttributeError):
        convert.loc_geo_to_mag([20, 30], "2012-06-15 22:02")


def test_convert_single_g2m_not_a_datetime():
    time = "2012-06-15 22:02"
    res = convert.loc_geo_to_mag(north_pole, time)
    assert res.lat == NP_MLAT
    assert res.lon == NP_MLON


def test_convert_single_g2m_strdate_timezone():
    time = "2012-06-15 22:02Z"
    res = convert.loc_geo_to_mag(north_pole, time)
    assert res.lat == NP_MLAT
    assert res.lon == NP_MLON


def test_convert_single_g2m_unknown_date():
    time = "This can't be a time"
    with pytest.raises(ValueError):
        convert.loc_geo_to_mag(north_pole, time)


def test_convert_g2m_array():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    res = convert.arr_geo_to_mag([north_pole.lat], [north_pole.lon], time)
    np.testing.assert_array_equal(res, np.array([[NP_MLAT], [NP_MLON]]))


def test_convert_array_g2m_2vals():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    res = convert.arr_geo_to_mag([north_pole.lat, north_pole.lat], [north_pole.lon, north_pole.lon], time)
    expected = np.array(
        [
            [NP_MLAT, NP_MLAT],
            [NP_MLON, NP_MLON]
        ]
    )
    np.testing.assert_array_equal(res, expected)


def test_convert_array_g2m_np_input():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    input_lat = np.array([north_pole.lat, north_pole.lat])
    input_lon = np.array([north_pole.lon, north_pole.lon])
    res = convert.arr_geo_to_mag(input_lat, input_lon, time)
    expected = np.array(
        [
            [NP_MLAT, NP_MLAT],
            [NP_MLON, NP_MLON]
        ]
    )
    np.testing.assert_array_equal(res, expected)


def test_convert_array_g2m_single_input():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    with pytest.raises(TypeError):
        convert.arr_geo_to_mag(north_pole.lat, north_pole.lon, time)


def test_convert_array_g2m_uneven():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    with pytest.raises(ValueError):
        convert.arr_geo_to_mag([north_pole.lat, north_pole.lat], [north_pole.lon], time)


def test_convert_array_g2m_np_input_shape():
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    input_lat = np.array([[north_pole.lat], [north_pole.lat]])
    input_lon = np.array([[north_pole.lon], [north_pole.lon]])
    with pytest.raises(ValueError):
        convert.arr_geo_to_mag(input_lat, input_lon, time)


def test_convert_angle_180():
    x = 2
    y = 2
    angle = 180
    res = convert.xy_angle_to_origin(x, y, angle)
    assert res == 45


def test_convert_angle_minus180():
    res = convert.xy_angle_to_origin(2, 2, -180)
    assert res == 45


def test_convert_angle_1xy_180():
    res = convert.xy_angle_to_origin(1, 1, 180)
    assert res == 45


def test_convert_angle_160():
    res = convert.xy_angle_to_origin(2, 2, 160)
    assert res == 65


def test_convert_angle_minus160():
    res = convert.xy_angle_to_origin(2, 2, -160)
    assert res == 25


def test_convert_angle_0():
    res = convert.xy_angle_to_origin(2, 2, 0)
    assert res == 225  # (180 + 45)


def test_convert_left_quad_180():
    res = convert.xy_angle_to_origin(-2, 2, 180)
    assert res == 135  # 90 + 45


def test_convert_left_quad_160():
    res = convert.xy_angle_to_origin(-2, 2, 160)
    assert res == 155  # 90 + 65


def test_convert_bottom_left_quad_180():
    res = convert.xy_angle_to_origin(-2, -2, 180)
    assert res == 225  # 180 + 45


def test_convert_bottom_left_quad_minus160():
    res = convert.xy_angle_to_origin(-2, -2, -160)
    assert res == 205  # 180 + 25


def test_convert_bottom_left_quad_0():
    res = convert.xy_angle_to_origin(-2, -2, 0)
    assert res == 45


def test_convert_bottom_right_quad_180():
    res = convert.xy_angle_to_origin(2, -2, 180)
    assert res == 315  # 180 + 90 + 45


def test_convert_bottom_right_quad_160():
    res = convert.xy_angle_to_origin(2, -2, 160)
    assert res == 335  # 180 + 90 + 65


def test_convert_bottom_right_quad_minus160():
    res = convert.xy_angle_to_origin(2, -2, -160)
    assert res == 295  # 180 + 90 + 25


def test_convert_bottom_right_quad_0():
    res = convert.xy_angle_to_origin(2, -2, 0)
    assert res == 135  # 90 + 45


def test_convert_angle_array():
    x = np.array([2, 2, 1])
    y = np.array([2, -2, 1])
    angle = np.array([180, 180, 0])
    res = convert.xy_angle_to_origin(x, y, angle)
    np.testing.assert_array_almost_equal(res, np.array([45, 315, 225]))
