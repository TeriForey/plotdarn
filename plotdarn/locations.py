

class Location(object):
    """
    Location object contains latitude and longitude for a geodetic location

    Latitude must be within -90 and 90. Longitude must be within -180 and 180.
    """

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, d):
        if d > 90 or d < -90:
            raise ValueError("Latitude must be within -90 to 90 degrees")
        self._lat = d

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, d):
        if d > 180 or d < -180:
            raise ValueError("Longitude must be within -180 to 180 degrees")
        self._lon = d


north_pole = Location(90, 0)

