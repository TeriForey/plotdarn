

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
