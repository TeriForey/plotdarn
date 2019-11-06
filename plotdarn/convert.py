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
    if isinstance(dtime, str):
        try:
            dtime = dt.datetime.strptime(dtime, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                dtime = dt.datetime.strptime(dtime, "%Y-%m-%d %H:%M%z")
            except ValueError:
                raise ValueError("Unable to convert string to datetime")

    converted = aacgmv2.convert_latlon(loc.lat, loc.lon, 100, dtime, code='A2G')
    newloc = Location(converted[0], converted[1])
    return newloc


def arr_mag_to_geo(latitudes, longitudes, dtime):
    """
    Convert two arrays of latitudes and longitudes of geomagnetic coords into geodetic coords. Numpy array is returned
    of lat, lon pairs, e.g. [[lat, lon], [lat, lon]]
    :param latitudes: ndarray
    :param longitudes: ndarray
    :param dtime: datetime
    :return: array with lat and lon in that order
    """
    if len(latitudes) != len(longitudes):
        raise ValueError("Input latitude and longitude must be the same length!")
    if isinstance(latitudes, np.ndarray):
        if latitudes.shape != longitudes.shape:
            raise ValueError('Arrays are not of equal length')
        if len(latitudes.shape) > 1:
            raise ValueError('Latitudes should be in a single dimension')
    if isinstance(longitudes, np.ndarray):
        if len(longitudes.shape) > 1:
            raise ValueError('Longitudes should be in a single dimension')

    converted = aacgmv2.convert_latlon_arr(latitudes, longitudes, 100, dtime, code='A2G')
    return converted[0:2]
