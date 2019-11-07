# -*- coding: utf-8 -*-

"""Plotting components"""
from shapely.ops import linemerge, unary_union, polygonize
from shapely.geometry import shape
import numpy as np
from plotdarn import convert
import aacgmv2
from bokeh.models import ColumnDataSource, ColorBar
from bokeh.palettes import Viridis11
from bokeh.transform import log_cmap


def coastlines(dtime, geometries, minlat=50):
    """
    Return the coastline geometries in a format suitable for plotting
    :param dtime:
    :param geometries:
    :return:
    """
    xs = []
    ys = []

    for geom in geometries:
        if geom.area == 8900.069899944174 or geom.area == 4158.330801265312:
            # Asia and America break so need to trim down before converting
            line = shape({'type': 'LineString', 'coordinates': ((-180, 25), (180, 25))})
            merged = linemerge([geom.exterior, line])
            borders = unary_union(merged)
            polygons = polygonize(borders)
            geom = next(polygons)

        glat = np.array(geom.exterior.xy[1])
        glon = np.array(geom.exterior.xy[0])

        if glat.max() < 0:
            continue

        converted = convert.arr_geo_to_mag(glat, glon, dtime)
        mlts = aacgmv2.convert_mlt(converted[1], dtime, m2a=False)
        x, y = convert.mlat_mlt_to_xy(converted[0], mlts, minlat)
        xs.append(x)
        ys.append(y)
    return xs, ys


def vector_points(dtime, mlat, mlon, mag, minlat=50):
    mlts = aacgmv2.convert_mlt(mlon, dtime, m2a=False)
    x, y = convert.mlat_mlt_to_xy(mlat, mlts, minlat)
    mapper = log_cmap(field_name='m', palette=Viridis11, low=min(y), high=max(y))
    source = ColumnDataSource(dict(x=x, y=y, m=mag))
    return source, mapper


def boundary(dtime, mlat, mlon, minlat=50):
    mlts = aacgmv2.convert_mlt(mlon, dtime, m2a=False)
    x, y = convert.mlat_mlt_to_xy(mlat, mlts, minlat)
    return x, y


def gridlines(minlat=50):
    circle_80 = [[80, i / 2] for i in range(0, 49)]
    circle_70 = [[70, i / 2] for i in range(0, 49)]
    circle_60 = [[60, i / 2] for i in range(0, 49)]
    circle_50 = [[50, i / 2] for i in range(0, 49)]
    lines = [
        [[80, 0], [minlat, 0]],
        [[80, 3], [minlat, 3]],
        [[80, 6], [minlat, 6]],
        [[80, 9], [minlat, 9]],
        [[80, 12], [minlat, 12]],
        [[80, 15], [minlat, 15]],
        [[80, 18], [minlat, 18]],
        [[80, 21], [minlat, 21]],
        circle_80,
        circle_70,
        circle_60,
        circle_50
    ]
    converted_lines_x = []
    converted_lines_y = []
    for group in lines:
        converted_group_x = []
        converted_group_y = []
        for point in group:
            x, y = convert.mlat_mlt_to_xy(point[0], point[1], minlat)
            converted_group_x.append(x)
            converted_group_y.append(y)
        converted_lines_x.append(converted_group_x)
        converted_lines_y.append(converted_group_y)
    return converted_lines_x, converted_lines_y
