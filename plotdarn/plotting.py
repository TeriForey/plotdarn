# -*- coding: utf-8 -*-

"""Plotting components"""
from shapely.ops import linemerge, unary_union, polygonize
from shapely.geometry import shape
import numpy as np
from plotdarn import convert
from bokeh.models import ColumnDataSource
from bokeh import palettes
from bokeh.transform import linear_cmap
from .utils import scale_velocity, points_inside_boundary
from .fitted_vectors import sdarn_get_potential_grid, fitted_vecs
from skimage import measure


def coastlines(dtime, geometries):
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
            for p in polygons:
                if p.area == 2477.716653116975 or p.area == 6247.72291492699:
                    geom = p

        glat = np.array(geom.exterior.xy[1])
        glon = np.array(geom.exterior.xy[0])

        if glat.max() < 0:
            continue

        converted = convert.arr_geo_to_mag(glat, glon, dtime)
        mlat = converted[0]
        mlon = converted[1]
        if np.any(np.isnan(mlat)):
            mask = np.ma.masked_invalid(converted)
            mlat = mask[0][~mask.mask[0]]
            mlon = mask[1][~mask.mask[1]]

        mlts = convert.mlon_to_mlt(mlon, dtime)
        x, y = convert.mlat_mlt_to_xy(mlat, mlts)
        xs.append(x)
        ys.append(y)
    return xs, ys


def coastlines_from_mlat_mlon(dtime, mlats, mlons):
    xs = []
    ys = []

    for i, mlat in enumerate(mlats):
        mlon = mlons[i]
        mlts = convert.mlon_to_mlt(mlon, dtime)
        x, y = convert.mlat_mlt_to_xy(mlat, mlts)
        xs.append(x)
        ys.append(y)
    return xs, ys


def vector(dtime, mlat, mlon, boundary, latmin=50, coeffs=None, ang=None, mag=None, plottype='LOS'):
    if plottype == 'FIT':
        ang, mag = fitted_vecs(coeffs, mlat, mlon, dtime, latmin)
        ang = np.array(ang)
        mag = np.array(mag)
    mlts = convert.mlon_to_mlt(mlon, dtime)
    x, y = convert.mlat_mlt_to_xy(mlat, mlts)
    inside = points_inside_boundary(x, y, boundary[0], boundary[1])
    mapper = linear_cmap(field_name='m', palette=palettes.Viridis256, low=0, high=1000)
    scaled_mag = scale_velocity(mag)
    converted_angles = convert.xy_angle_to_origin(x, y, ang)
    inside_source = ColumnDataSource(dict(x=x[inside], y=y[inside], m=mag[inside], le=scaled_mag[inside],
                                          an=converted_angles[inside], mlon=mlon[inside], mlat=mlat[inside],
                                          mlt=mlts[inside], ang=ang[inside]))
    outside = np.logical_not(inside)
    outside_source = ColumnDataSource(dict(x=x[outside], y=y[outside], m=mag[outside], le=scaled_mag[outside],
                                           an=converted_angles[outside], mlon=mlon[outside], mlat=mlat[outside],
                                           mlt=mlts[outside], ang=ang[outside]))
    return inside_source, outside_source, mapper


def boundary(dtime, mlat, mlon):
    mlts = convert.mlon_to_mlt(mlon, dtime)
    x, y = convert.mlat_mlt_to_xy(mlat, mlts)
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
            x, y = convert.mlat_mlt_to_xy(point[0], point[1])
            converted_group_x.append(x)
            converted_group_y.append(y)
        converted_lines_x.append(converted_group_x)
        converted_lines_y.append(converted_group_y)
    return converted_lines_x, converted_lines_y


def contours(coeffs, latmin=50):
    pot = sdarn_get_potential_grid(coeffs, latmin) / 1.e3

    xs = []
    ys = []

    levels = [-57.0000,-51.0000,-45.0000,-39.0000,-33.0000,-27.0000,-21.0000,-15.0000,-9.00000,-3.0000, 3.00000, 9.00000,15.0000,21.0000,27.0000,33.000,39.0000,45.0000,51.0000,57.0000]
    for lev in levels:
        lines = measure.find_contours(pot, lev)
        for contour in lines:
            x = contour[:, 1] - 39.5
            y = contour[:, 0] - 39.5
            xs.append(x)
            ys.append(-y)

    return xs, ys
