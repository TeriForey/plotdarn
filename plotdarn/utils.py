import pvlib
import numpy as np
from .locations import Location
from math import floor, sin, cos, pi, atan2, asin, radians, sqrt, degrees
import matplotlib.path as mpltPath


def antipode(val, axis='longitude'):
    """
    Simple utility to calculate antipode, that is the opposite latitude or longitude.

    :param val: latitude or longitude to calculate antipode
    :param axis: either 'latitude' or 'longitude'. Default is 'longitude'
    :return:
    """
    if axis == 'latitude':
        return -val
    elif axis == 'longitude':
        opp = 180 - abs(val)
        if val > 0:
            return -opp
        return opp
    else:
        raise ValueError("axis only accepts 'longitude' or 'latitude'")


def sun_position(loc, dtime):
    """
    Utility to calculate the sun's position relative to a location and time. Will return the azimuth, that is the
    degrees clockwise from North.

    :param loc: location object
    :param dtime: datetime
    :return: azimuth
    """
    sun = pvlib.solarposition.get_solarposition(time=dtime, latitude=loc.lat, longitude=loc.lon)
    return float(sun.azimuth)


def sun_longitude(dtime):
    """
    Calculate the longitude of the subsolar point, that is the point on earth where the sun is at it's zenith. This
    algorithm is from K.M. Laundal and A.D. Richmond (https://arxiv.org/pdf/1611.10321.pdf). This method is independent
    of any observer point on earth and therefore doesn't require the azimuth.

    :param dtime: datetime
    :return: float longitude
    """
    # Year
    year = dtime.year
    # Day of year
    doy = dtime.timetuple().tm_yday
    # universal time in seconds since start of day
    ut = (dtime.hour * 60 * 60) + (dtime.minute * 60) + dtime.second

    yr = year - 2000
    nleap = floor((year - 1601) / 4.)
    nleap = nleap - 99
    if year <= 1900:
        ncent = floor((year - 1601) / 100.)
        ncent = 3 - ncent
        nleap = nleap + ncent
    l0 = -79.549 + (-.238699 * (yr - 4 * nleap) + 3.08514e-2 * nleap)
    g0 = -2.472 + (-.2558905 * (yr - 4 * nleap) - 3.79617e-2 * nleap)
    df = (ut / 86400. - 1.5) + doy
    lf = .9856474 * df
    gf = .9856003 * df
    l = l0 + lf
    g = g0 + gf
    grad = g * pi / 180.
    lmbda = l + 1.915 * sin(grad) + .020 * sin(2. * grad)
    lmrad = lmbda * pi / 180.
    sinlm = sin(lmrad)
    n = df + 365. * yr + nleap
    epsilon = 23.439 - 4.0e-7 * n
    epsrad = epsilon * pi / 180.
    alpha = atan2(cos(epsrad) * sinlm, cos(lmrad)) * 180. / pi
    delta = asin(sin(epsrad) * sinlm) * 180. / pi
    sbslcolat = 90 - delta  # co-latitude
    etdeg = l - alpha
    nrot = round(etdeg / 360.)
    etdeg = etdeg - 360. * nrot
    aptime = ut / 240. + etdeg
    sbsllon = 180. - aptime
    nrot = round(sbsllon / 360.)
    sbsllon = sbsllon - 360. * nrot
    return sbsllon


def cross_dateline(array, close=False):
    """
    Function to re-order array of latitude and longitudes so that dateline cross isn't affected. This assumes that
    input array is drawing a circular object and that therefore the start/end positions can be changed without
    affecting the meaning!
    If it cannot be resolved, i.e. after rolling there is still a longitude gap > 180 degrees, the original array will
    be returned without any changes.
    :param array: ndarray
        Latitudes and longitudes in the form of [[lat, lon], [lat, lon]]
    :param close: bool
        Boolean as to whether the array should close up to dateline or not.
    :return:
    """

    differences = np.absolute(np.diff(array[:, 1], axis=0))
    if (differences > 180).any():
        assert len(np.nonzero(differences > 180)) == 1
        cross_point = np.nonzero(differences > 180)[0] + 1
    else:
        return array

    cross_point_from_back = len(array) - cross_point
    rolled = np.roll(array, cross_point_from_back, 0)
    test_again = np.absolute(np.diff(rolled[:, 1], axis=0))
    if (test_again > 180).any():
        return array

    if close:
        # Want to close the circle.
        loc1 = Location(rolled[0, 0], rolled[0, 1])
        loc2 = Location(rolled[-1, 0], rolled[-1, 1])

        if loc1.lon < 0:
            lon = -180
        else:
            lon = 180

        midpoint = find_intermediate_point(loc1, loc2)
        newstart = [[midpoint.lat, lon]]
        newend = [[midpoint.lat, -lon]]

        newarray = np.vstack([newstart, rolled, newend])
        return newarray

    return rolled


def find_intermediate_point(loc1, loc2):
    """
    Calculate intermediate point between two locations using haversine and fraction distance
    (0 is point a, 1 is point b). Equation taken from https://www.movable-type.co.uk/scripts/latlong.html
    :param loc1:
    :param loc2:
    :return:
    """
    d = haversine(loc1.lon, loc1.lat, loc2.lon, loc2.lat)
    fraction = (1 / ((180 - abs(loc1.lon)) + (180 - abs(loc2.lon)))) * (180 - abs(loc1.lon))
    angular_dist = d/6371e3  # this is c from haversine

    lon1, lat1, lon2, lat2 = map(radians, [loc1.lon, loc1.lat, loc2.lon, loc2.lat])

    a = sin((1-fraction) * angular_dist) / sin(angular_dist)
    b = sin(fraction * angular_dist) / sin(angular_dist)
    x = a * cos(lat1) * cos(lon1) + b * cos(lat2) * cos(lon2)
    y = a * cos(lat1) * sin(lon1) + b * cos(lat2) * sin(lon2)
    z = a * sin(lat1) + b * sin(lat2)

    lat = atan2(z, sqrt(x ** 2 + y ** 2))
    lon = atan2(y, x)

    # convert back to decimal degrees
    lat_deg, lon_deg = map(degrees, [lat, lon])

    return Location(lat_deg, lon_deg)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371e3  # Radius of earth in meters
    return c * r


def scale_velocity(vel, length=0.2):
    """
    Scale all velocities to a length on the graph (axis) that is 1000ms
    :param vel: ndarray
    :param length: float
    :return:
    """
    if not isinstance(vel, np.ndarray):
        vel = np.array(vel)
    return vel * (length/1000)


def points_inside_boundary(points_x, points_y, boundary_x, boundary_y, radius=0.0):
    """
    Takes in x, y of points and boundary and returns boolean array of points inside boundary.
    :param points_x: ndarray or list
    :param points_y: ndarray or list
    :param boundary_x: ndarray or list
    :param boundary_y: ndarray or list
    :param radius: optional: make the boundary larger or smaller
    :return:
    """
    poly = np.array([boundary_x, boundary_y]).T
    points = np.array([points_x, points_y]).T
    path = mpltPath.Path(poly)
    inside = path.contains_points(points, radius=radius)
    return inside
