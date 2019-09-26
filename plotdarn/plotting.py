# -*- coding: utf-8 -*-

"""Plotting components"""
import geoviews as gv
import numpy as np
from .locations import north_pole
from .convert import convert_mag_single, convert_mag_arr
from plotdarn import utils


def plot_magnetic_north(dtime, col='green'):
    """
    Will create the plotting component to plot the geomagnetic north pole
    :param dtime: datetime
    :param col: str color to plot point with
    :return:
    """
    magnetic_north = convert_mag_single(north_pole, dtime)
    return gv.Points((magnetic_north.lon, magnetic_north.lat)).opts(color=col, size=3)


def plot_magnetic_longitudes(dtime):
    """
    Will create the plotting components for the longitudes 0, 45, 90, 135, 180 in both directions
    :param dtime:
    :return:
    """
    all_lons = None
    longitudes = [-135, -90, -45, 0, 45, 90, 135, 180]
    for lon in longitudes:
        lat_array = np.arange(50, 80)
        lon_array = np.full(lat_array.shape, lon)

        converted = convert_mag_arr(lat_array, lon_array, dtime)

        path = gv.Points(converted[:, [1, 0]]).opts(color='grey', size=1)
        if all_lons is None:
            all_lons = path
        else:
            all_lons = all_lons * path
    return all_lons


def plot_magnetic_latitudes(dtime):
    """
    Will create the plotting components for the latitudes 80, 70, 60, 50
    :param dtime:
    :return:
    """
    all_lats = None
    latitudes = [80, 70, 60, 50]
    spacers = [6, 4, 3, 2]
    for i, lat in enumerate(latitudes):
        spacer = spacers[i]
        lon_array = np.arange(-180, 180, spacer)
        lat_array = np.full(lon_array.shape, lat)

        converted = convert_mag_arr(lat_array, lon_array, dtime)

        path = gv.Points(converted[:, [1, 0]]).opts(color='grey', size=1)
        if all_lats is None:
            all_lats = path
        else:
            all_lats = all_lats * path
    return all_lats


def plot_boundary(dtime, boundary_lat, boundary_lon):
    """
    Plot the green boundary line
    :param dtime:
    :param boundary_lat:
    :param boundary_lon:
    :return:
    """
    boundary = convert_mag_arr(boundary_lat, boundary_lon, dtime)
    boundary = utils.cross_dateline(boundary, close=True)

    return gv.Path(boundary[:, [1, 0]]).opts(color='limegreen')
