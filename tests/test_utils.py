import numpy as np
from plotdarn.utils import scale_velocity, points_inside_boundary


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
    np.testing.assert_array_almost_equal(res, np.array([0.005, 0.01, 0.015, 0.025]))


def test_scale_vel_list():
    res = scale_velocity([1, 2, 3, 4])
    np.testing.assert_array_almost_equal(res, np.array([0.005, 0.01, 0.015, 0.02]))


def test_points_inside_simple_outside():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside = points_inside_boundary([0], [0], bx, by)
    np.testing.assert_array_equal(inside, np.array([False]))


def test_points_inside_simple_inside():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside = points_inside_boundary([1.5], [1.5], bx, by)
    np.testing.assert_array_equal(inside, np.array([True]))


def test_points_inside_border():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside = points_inside_boundary([1], [1], bx, by)
    np.testing.assert_array_equal(inside, np.array([False]))


def test_points_inside_border_radius():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside = points_inside_boundary([1], [1], bx, by, radius=0.1)
    np.testing.assert_array_equal(inside, np.array([True]))


def test_points_inside_mulitple():
    bx = [1, 2, 2, 1]
    by = [1, 1, 2, 2]
    inside = points_inside_boundary([1.1, 2, 1.5, 1.2], [1.1, 2.1, 1.5, 3], bx, by)
    np.testing.assert_array_equal(inside, np.array([True, False, True, False]))


def test_points_inside_mulitple_array():
    bx = np.array([1, 2, 2, 1])
    by = np.array([1, 1, 2, 2])
    inside = points_inside_boundary(np.array([1.1, 2, 1.5, 1.2]), np.array([1.1, 2.1, 1.5, 3]), bx, by)
    np.testing.assert_array_equal(inside, np.array([True, False, True, False]))
