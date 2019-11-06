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
