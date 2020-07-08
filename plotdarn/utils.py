import numpy as np
import matplotlib.path as mpltPath


def scale_velocity(vel, length=5):
    """
    Scale all velocities to a length on the graph (axis) that is 1000ms
    :param vel: ndarray
    :param length: float
    :return:
    """
    if not isinstance(vel, np.ndarray):
        vel = np.array(vel)
    return vel * (length/1000) + 1e-10


def points_inside_boundary(points_x, points_y, boundary_x, boundary_y, radius=0.0):
    """
    Takes in x, y of points and boundary and returns boolean array of points inside boundary.
    :param points_x: ndarray or list
    :param points_y: ndarray or list
    :param boundary_x: ndarray or list
    :param boundary_y: ndarray or list
    :param radius: optional: make the boundary larger or smaller
    :return:
    """
    poly = np.array([boundary_x, boundary_y]).T
    points = np.array([points_x, points_y]).T
    path = mpltPath.Path(poly)
    inside = path.contains_points(points, radius=radius)
    return inside
