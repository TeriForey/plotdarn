import pvlib
from math import floor, sin, cos, pi, atan2, asin


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
