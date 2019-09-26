# -*- coding: utf-8 -*-

"""Main module."""
import geoviews as gv
import geoviews.feature as gf
from geoviews import opts
from datetime import datetime
from cartopy import crs
from plotdarn import plotting
import pydarn


def read_file(filename):
    """
    Read SuperDarn binary file and return the first record
    :param filename:
    :return: dictionary
    """
    dmap = pydarn.DarnRead(filename)
    fitacf_dmap = dmap.read_map()
    fitacf_data = pydarn.dmap2dict(fitacf_dmap)
    return fitacf_data[0]


def plot_superdarn(data):
    """
    Plot superDarn data using Bokeh
    :param data:
    :return: bokeh overlay
    """
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)
    mag = plotting.plot_magnetic_north(time)

    longs = plotting.plot_magnetic_longitudes(time)
    lats = plotting.plot_magnetic_latitudes(time)
    boundary = plotting.plot_boundary(time, data['boundary.mlat'], data['boundary.mlon'])

    features = gv.Overlay([gf.land, gf.borders, gf.coastline])

    return (features * mag * longs * lats * boundary).opts(
        opts.Points(
            width=500, height=475, projection=crs.NorthPolarStereo()
        )
    )
