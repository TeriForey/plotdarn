from .locations import Location
from spacepy.coordinates import Coords
from spacepy.time import Ticktock
import aacgmv2
import datetime as dt
import numpy as np


def loc_mag_to_geo(loc, dtime):
    """
    Convert a single location in geomagnetic coords into geodetic coords
    :param loc:
        location.Location object with longitude and latitude in geomagnetic coords
    :param dtime:
        either datetime object or parse-able string
    :return:
        location.Location object with longitude and latitude in geodetic coords
    """
    dtime = _check_time(dtime)

    converted = aacgmv2.convert_latlon(loc.lat, loc.lon, 100, dtime, code='A2G')
    newloc = Location(converted[0], converted[1])
    return newloc


def arr_mag_to_geo(latitudes, longitudes, dtime):
    """
    Convert two arrays of latitudes and longitudes of geomagnetic coords into geodetic coords. Numpy array is returned
    of lat, lons e.g. [[lat, lat], [lon, lon]]
    :param latitudes: ndarray
    :param longitudes: ndarray
    :param dtime: datetime
    :return: array with lat and lon in that order
    """
    dtime = _check_time(dtime)
    _check_arrays(latitudes, longitudes)

    converted = aacgmv2.convert_latlon_arr(latitudes, longitudes, 100, dtime, code='A2G')
    return converted[0:2]


def loc_geo_to_mag(loc, dtime):
    """
    Convert a single location in geodetic coords into geomagnetic coords
    :param loc:
        location.Location object with longitude and latitude in geodetic coords
    :param dtime:
        either datetime object or parse-able string
    :return:
        location.Location object with longitude and latitude in geomagnetic coords
    """
    dtime = _check_time(dtime)

    converted = aacgmv2.convert_latlon(loc.lat, loc.lon, 100, dtime, code='G2A')
    newloc = Location(converted[0], converted[1])
    return newloc


def arr_geo_to_mag(latitudes, longitudes, dtime):
    """
    Convert two arrays of latitudes and longitudes of geodetic coords into geomagnetic coords. Numpy array is returned
    of lat, lons, e.g. [[lat, lat], [lon, lon]]
    :param latitudes: ndarray
    :param longitudes: ndarray
    :param dtime: datetime
    :return: array with lat and lon in that order
    """
    dtime = _check_time(dtime)
    _check_arrays(latitudes, longitudes)

    converted = aacgmv2.convert_latlon_arr(latitudes, longitudes, 100, dtime, code='G2A')
    return converted[0:2]


def mlon_to_mlt(mlon, dtime):
    return aacgmv2.convert_mlt(mlon, dtime, m2a=False)


def mlat_mlt_to_xy(mlat, mlt, minlat):
    r = (90. - np.abs(mlat)) / (90. - minlat)
    a = (np.array(mlt) - 6.) / 12. * np.pi
    return r * np.cos(a), r * np.sin(a)


def xy_angle_to_origin(x, y, angle):
    angle_from_origin = np.arctan2(y, x)
    first_step = 180 - (180 - angle) - np.degrees(angle_from_origin)
    result = (180 - first_step) % 360
    return result


def _check_time(dtime):
    if isinstance(dtime, str):
        try:
            dtime = dt.datetime.strptime(dtime, "%Y-%m-%d %H:%M")
        except ValueError:
            dtime = dt.datetime.strptime(dtime, "%Y-%m-%d %H:%M%z")
    return dtime


def _check_arrays(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError("Input latitude and longitude must be the same length!")
    if isinstance(arr1, np.ndarray):
        if arr1.shape != arr2.shape:
            raise ValueError('Arrays are not of equal length')
        if len(arr1.shape) > 1:
            raise ValueError('Latitudes should be in a single dimension')
    if isinstance(arr2, np.ndarray):
        if len(arr2.shape) > 1:
            raise ValueError('Longitudes should be in a single dimension')
