## Module to process and calculate explicitly spatial data.
##
## Functions:
##
## PlanarDistance() -- Returns the planar distance between two sets of
##      coordinates.
##
## HaversineDistance() -- Returns the geographic distance between two sets of
##      geographic coordinates.
##
## Angle() -- Returns the straight-line (i.e., not great circle) angle/bearing
##      from one point to another.
##
##

import os


def PlanarDistance(point1, point2):
    '''
    (tuple/list, tuple/list) -> float

    Returns the planar distance between the two points, in the same unit as the
        coordinates. Note that this function returns erroneous values when
        passed geographic coordinates. Please pass projected coordinates only.
        See HaversineDistance() for geographic coordinates.

    Arguments:
    point1 -- The x and y coordinates of a point.
    point2 -- The x and y coordinates of a point.

    Example:
    >>> PlanarDistance((0,0),(1,1))
    1.4142136
    >>> PlanarDistance((43517,25234),(12651,16548))
    32064.8803522
    '''
    import math
    # Confirm that the user passed lists/tuples
    assert isinstance(point1, (list, tuple))
    assert isinstance(point2, (list, tuple))

    try:
        # Extract the x and y coordinates
        x1, y1 = point1
        x2, y2 = point2
        # Calculate the distance between the two points
        dist = math.sqrt(((x1-x2)**2 + (y1-y2)**2))
    except Exception as e:
        print e
        return

    return dist



def HaversineDistance(point1, point2, unit='coordinates'):
    '''
    (tuple, tuple) -> float

    Calculates the great-circle distance between two geographic coordinates;
        result is in meters.

    Arguments:
    point1 -- The geographic coordinates of a point, as a tuple. The order of
        latitude and longitude must match that of point2.
    point2 -- The geographic coordinates of a point, as a tuple. The order of
        latitude and longitude must match that of point1.

    Example:
    >>> print HaversineDistance((46.732434,-117.040306), (46.732581,-117.019181))
    1609.83972203
    >>> print HaversineDistance((0,0), (1,0))
    111317.099692
    '''
    import math

##    if type(point1) <> 'tuple' and type(point2) <> 'tuple':
        ##print 'The function HaversineDistance in the module spatial takes two tuples\n\
        ##as its arguments; you passed %s and %s.' % (type(point1), type(point2))
        ##return False

    lat1, lon1 = point1
    lat2, lon2 = point2

    # Earth's radius, accounting for latitudinal variation:
    # http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
    radius = 6378 - 21 * math.sin((lat1 + lat2)/2)

    # Get each number in radians
    lat1_r,lon1_r,lat2_r,lon2_r = map(math.radians,(lat1,lon1,lat2,lon2))

    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r

    # Haversine formula:
    # http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
    # http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    # http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
    a = math.sin(dlat/2)**2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))

    # Get the distance in meters
    d = radius * c * 1000

    return d


#def Bearing(x, y):
#    from math import atan2, sin, cos, degrees
#
#    lat1, lon1 = x
#    lat2, lon2 = y
#
#    bearing = atan2(cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1), sin(lon2-lon1)*cos(lat2))
#
#    bearing = degrees(bearing)
#
#    bearing = (bearing + 360) % 360
#
#    return bearing


def Angle(point1, point2):
    '''
    (tuple, tuple) -> float

    Returns the straigt-line angle (i.e., not the great circle bearing) in
        degrees between point1 and point2.

    Arguments:
    point1 -- The geographic coordinates of a point, as a tuple. Latitude must
        be the first item in the tuple.
    point2 -- The geographic coordinates of a point, as a tuple. Latitude must
        be the first item in the tuple.

    Examples:
    >>> Angle((-100, 25), (-50, 30))
    5.710593137499642
    Angle((25,100), (30,50))
    -84.28940686250037
    '''
    import math

    x1, y1 = point1
    x2, y2 = point2

    deltaY = y2 - y1
    deltaX = x2 - x1

    #angleInDegrees = math.atan2(deltaY, deltaX) * 180 / math.pi
    return math.degrees(math.atan2(deltaY, deltaX))



##################################
#### Module's main function
def __main():
    pass



# If the module was run directly, call the main function
if __name__ == '__main__':
    __main()