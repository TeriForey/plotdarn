import pvlib


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
