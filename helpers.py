import math

class Constants:
    URAD2RAD = 10**(-6)
    DEG2RAD = math.pi / 180.0


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

