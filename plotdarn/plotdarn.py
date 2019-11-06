# -*- coding: utf-8 -*-

"""Main module."""
from datetime import datetime
from plotdarn import plotting
from bokeh.models import Range1d
from bokeh.plotting import figure
import pydarn
import geopandas as gdp


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


def read_coast(filename):
    """
    Read in a Shapefile and return a list of geometries
    :param filename:
    :return:
    """
    shp = gdp.read_file(filename)
    return shp['geometry']


def plot_superdarn(data, coastline_geoms):
    """
    Plot superDarn data using Bokeh
    :param data:
    :return: bokeh overlay
    """
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)

    p = figure(plot_width=400, plot_height=400)
    coastlines = plotting.coastlines(time, coastline_geoms)
    p.multi_line(xs=coastlines[0], ys=coastlines[1], line_color='black')
    points, mapper = plotting.vector_points(time, data['vector.mlat'], data['vector.mlon'], data['vector.vel.median'])
    p.circle(x='x', y='y', source=points, size=2)
    boundary = plotting.boundary(time, data['boundary.mlat'], data['boundary.mlon'])
    p.line(x=boundary[0], y=boundary[1], line_color='lime')
    p.x_range = Range1d(-1, 1)
    p.y_range = Range1d(-1, 1)

    return p
