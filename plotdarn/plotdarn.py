# -*- coding: utf-8 -*-

"""Main module."""
from datetime import datetime
from plotdarn import plotting
from bokeh.models import Range1d, ColorBar
from bokeh.plotting import figure
import pydarn
import geopandas as gdp


def read_file(filename):
    """
    Read SuperDarn binary file and return the first record
    :param filename:
    :return: dictionary
    """
    reader = pydarn.SDarnRead(filename)
    records = reader.read_map()
    return records[0]


def read_coast(filename):
    """
    Read in a Shapefile and return a list of geometries
    :param filename:
    :return:
    """
    shp = gdp.read_file(filename)
    return shp['geometry']


def plot_superdarn(data, coastline_geoms, title='SuperDarn'):
    """
    Plot superDarn data using Bokeh
    :param data:
    :return: bokeh overlay
    """
    time = datetime(year=2012, month=6, day=15, hour=22, minute=2)

    # Create bokeh figure with no grid lines
    p = figure(title=title)
    p.grid.grid_line_color = None

    # Add coastlines
    coastlines = plotting.coastlines(time, coastline_geoms)
    p.multi_line(xs=coastlines[0], ys=coastlines[1], line_color='grey')

    # Add our own MLT gridlines
    grid = plotting.gridlines()
    p.multi_line(grid[0], grid[1], line_color='grey', line_dash='dotted')

    # Add the boundary lines
    boundary = plotting.boundary(time, data['boundary.mlat'], data['boundary.mlon'])
    p.line(x=boundary[0], y=boundary[1], line_color='lime')

    # Add the vector points
    in_points, out_points, mapper = plotting.los_vector(time, data['vector.mlat'], data['vector.mlon'],
                                                        data['vector.vel.median'], data['vector.kvect'], boundary)
    p.ray(x='x', y='y', length='le', angle='an', angle_units='deg', color=mapper, source=in_points)
    p.circle(x='x', y='y', color=mapper, source=in_points, size=2)
    p.ray(x='x', y='y', length='le', angle='an', angle_units='deg', color='dimgrey', source=out_points)
    p.circle(x='x', y='y', color='dimgrey', source=out_points, size=2)
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0, 0))
    p.add_layout(color_bar, 'right')

    # Set the plot range
    p.x_range = Range1d(-40, 40)
    p.y_range = Range1d(-40, 40)

    return p
