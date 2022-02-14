from asyncio import constants
import math

class Constants:
    URAD2RAD = 10**(-6)
    DEG2RAD = math.pi / 180.0
    WGS84_MAJOR_AXIS = 6378137.0 # meters
    WGS84_MINOR_AXIS = 6356752.314245 # meters
    WGS84_INVERSE_FLATTENING = 298.257223563 # 1/f
    WGS84_FLATTENING = 1.0/WGS84_INVERSE_FLATTENING # f
    WGS84_ECCENTRICITY = math.sqrt(2.0*WGS84_FLATTENING*(1.0 - WGS84_FLATTENING)) # e


def urad2rad(urad: float) -> float:
    return urad * Constants.URAD2RAD


def rad2urad(rad: float) -> float:
    return rad / Constants.URAD2RAD


def deg2rad(deg: float) -> float:
    return deg * Constants.DEG2RAD


def rad2deg(rad: float) -> float:
    return rad / Constants.DEG2RAD


def urad2deg(urad: float) -> float:
    return rad2deg(urad2rad(urad))


def deg2urad(deg: float) -> float:
    return rad2urad(deg2rad(deg))


##################### Spatial Algorithms #######################
def lla2xyz(lat: float, lon: float, h_el: float) -> tuple[float, float, float]:
    '''
        Input:
            Lat: Geodetic latitude (degrees)
            Lon: Geodetic Longitude (degrees)
            h_el: Ellipsoidal height (meters)
        Output: 
            tuple (x, y, z) (meters)'''
    Re = Constants.WGS84_MINOR_AXIS
    e = Constants.WGS84_ECCENTRICITY
    lat = deg2rad(lat)
    lon = deg2rad(lon)
    den = math.sqrt(1.0 - e*e*math.sin(lat)**2)
    N = Re/den
    S = (Re*(1 - e*e))/den
    slat = math.sin(lat)
    clat = math.cos(lat)
    slon = math.sin(lon)
    clon = math.cos(lon)
    x = (N + h_el)*clat*clon
    y = (N + h_el)*clat*slon
    z = (S + h_el)*slat
    return (x, y, z)




