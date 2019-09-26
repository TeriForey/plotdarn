from .locations import Location
from spacepy.coordinates import Coords
from spacepy.time import Ticktock
import numpy as np


def convert_mag_single(loc, dtime):
    """
    Convert a single location in geomagnetic coords into geodetic coords
    :param loc:
        location.Location object with longitude and latitude in geomagnetic coords
    :param dtime:
        either datetime object or parse-able string
    :return:
        location.Location object with longitude and latitude in geodetic coords
    """
    coords = Coords([1, loc.lat, loc.lon], 'MAG', 'sph')
    coords.ticks = Ticktock(dtime, 'ISO')
    converted = coords.convert('GDZ', 'sph')
    newloc = Location(converted.data[0, 1], converted.data[0, 2])
    return newloc


def convert_mag_arr(latitudes, longitudes, dtime):
    """
    Convert two arrays of latitudes and longitudes of geomagnetic coords in geodetic coords. Numpy array is returned
    of lat, lon pairs, e.g. [[lat, lon], [lat, lon]]
    :param latitudes: ndarray
    :param longitudes: ndarray
    :param dtime: datetime
    :return: array with lat and lon in that order
    """
    if len(latitudes) != len(longitudes):
        raise ValueError("Input latitude and longitude must be the same length!")
    nvals = len(latitudes)
    data = np.array([np.ones(nvals), latitudes, longitudes])

    times = [dtime for i in range(nvals)]

    coords = Coords(data.T, 'MAG', 'sph')
    coords.ticks = Ticktock(times, 'ISO')
    converted = coords.convert('GDZ', 'sph')
    return converted.data[:, [1, 2]]
