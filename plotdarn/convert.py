from .locations import Location
from spacepy.coordinates import Coords
from spacepy.time import Ticktock


def convert_mag_single(loc, dtime):
    coords = Coords([1, loc.lat, loc.lon], 'MAG', 'sph')
    coords.ticks = Ticktock(dtime, 'ISO')
    converted = coords.convert('GDZ', 'sph')
    newloc = Location(converted.data[0, 1], converted.data[0, 2])
    return newloc

