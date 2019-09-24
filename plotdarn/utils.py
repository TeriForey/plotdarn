

def antipode(val, axis='longitude'):
    if axis == 'latitude':
        return -val
    elif axis == 'longitude':
        opp = 180 - abs(val)
        if val > 0:
            return -opp
        return opp
    else:
        raise ValueError("axis only accepts 'longitude' or 'latitude'")
