# a function azimuth(x, y, day, time)
# returns the azimuth of the sun at a point with coordinates x, y on the Earth, in a day at time
import math
import datetime
import ephem
from datetime import datetime, timedelta


def azimuth(x, y, day, time):
    # coordinates of the point
    lat = math.radians(y)
    lon = math.radians(x)
    # date and time
    date = datetime.strptime(day, "%d-%m-%Y")
    time = datetime.strptime(time, "%H:%M")
    # the sun
    sun = ephem.Sun()
    # the observer
    obs = ephem.Observer()
    obs.lat = lat
    obs.lon = lon
    obs.date = date + timedelta(hours=time.hour - 1, minutes=time.minute)
    # the azimuth
    sun.compute(obs)
    az = math.degrees(sun.az)
    return int(az)