from cmath import sqrt
from turtle import color
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import copy
import math
import warnings

class Point:
    def __init__(self, x, y, z, color='blue', marker='o'):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.marker = marker

    @classmethod
    def fromArray(cls, ary: np.array):
        sz = ary.size
        if sz != 3:
            raise ValueError("ary should have size of 3")
        return cls(ary[0], ary[1], ary[2])

    def toArray(self):
        return np.array([[self.x, self.y, self.z]]).T

    def plot(self, ax):
        ax.scatter(self.x, self.y, self.z, color=self.color, marker=self.marker)

    def __add__(self, other):
        if isinstance(other, Point):
            p = Point(
                self.x + other.x, self.y + other.y, self.z + other.z, 
                self.color, self.marker)
            return p
        elif isinstance(other, tuple):
            x, y, z = other
            p = Point(
                self.x + x, self.y + y, self.z + z, 
                self.color, self.marker)
            return p
        
    def __sub__(self, other):
        p = Point(
            self.x - other.x, self.y - other.y, self.z - other.z,
            self.color, self.marker)
        return p

    def __mul__(self, s):
        if type(s) == int or type(s) == float:
            p = Point(s*self.x, s*self.y, s*self.z, self.color, self.marker)
            return p

    def __str__(self):
        s = f"x: {self.x}\n" \
            f"y: {self.y}\n" \
            f"z: {self.z}\n" \
            f"color: {self.color}\n" \
            f"marker: {self.marker}\n"
        return s


def dot(p1: Point, p2: Point) -> float:
    return p1.x*p2.x + p1.y*p2.y + p1.z*p2.z


def norm(p: Point) -> float:
    return math.sqrt(dot(p,p))


def normalize(p: Point) -> Point:
    n = norm(p)
    result = copy.copy(p)
    return result* (1./n)


def cross(p1: Point, p2: Point) -> Point:
    x = p1.y*p2.z - p1.z*p2.y
    y = p1.z*p2.x - p1.x*p2.z
    z = p1.x*p2.y - p1.y*p2.x
    return Point(x, y, z)


class Line:
    def __init__(self, p1, p2, color='blue'):
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def plot(self, ax):
        xs = [self.p1.x, self.p2.x]
        ys = [self.p1.y, self.p2.y]
        zs = [self.p1.z, self.p2.z]
        ax.plot(xs, ys, zs, color=self.color)


class CsAxis:
    def __init__(self, origin=Point(0,0,0), axis_length=1) :
        self.origin = origin
        self.axis_length = axis_length
        self.x_axis = Line(origin, origin + Point(1, 0, 0)*axis_length, 'blue')
        self.y_axis = Line(origin, origin + Point(0, 1, 0)*axis_length, 'green')
        self.z_axis = Line(origin, origin + Point(0, 0, 1)*axis_length, 'red')

    def plot(self, ax):
        self.x_axis.plot(ax)
        self.y_axis.plot(ax)
        self.z_axis.plot(ax)


class CameraIntrinsics:
    def __init__(self, fx: float, fy: float, px: float, py: float, s: float):
        self.fx = fx
        self.fy = fy
        self.px = px
        self.py = py
        self.s  = s

    def getMatrix(self):
        fx = self.fx
        fy = self.fy
        px = self.px
        py = self.py
        s  = self.s
        return np.array(
            [
                [fx, s, px],
                [0, fy, py],
                [0,  0, 1.0]
            ])
        

class CameraExtrinsics:
    def __init__(self, R: np.array, t: np.array):
        shape = R.shape
        if shape[0] != 3 or shape[1] != 3:
            raise ValueError("Wrong dimensions! Input R must be a 3x3 rotation matrix")
        sz = t.size
        if sz != 3:
            raise ValueError("Wrong dimensions! Input t must be a 3x1 translation matrix")
        self.R = R
        self.t = t

    @classmethod
    def from_look_up(cls, center: Point, look: Point, up: Point):
        R = np.zeros((3,3))
        z_axis = normalize(look) # z axis in camera coordinate system
        up = up - look * dot(up, look)
        y_axis = normalize(up) # y axis in camera coordinate system
        x_axis = cross(y_axis, z_axis) # x axis = y x z
        
        R[:, 0] = x_axis.toArray().T
        R[:, 1] = y_axis.toArray().T
        R[:, 2] = z_axis.toArray().T
        t = -1*np.dot(R, center.toArray())
        return cls(R, t)

    def __str__(self):
        s = "R: \n" + self.R.__str__() + "\n" + "t: \n" + self.t.__str__()
        return s


class Camera:
    def __init__(self, center):
        pass

def test(p: Point):
    p = normalize(p)
    print(p)

center = Point(0, 0, 0)
look = Point(0, 0, 1)
up = Point(0, 1, 0)
extrinsics = CameraExtrinsics.from_look_up(center, look, up)
print(extrinsics)

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# #ax.set_aspect("auto")

# cs_axis = CsAxis()
# cs_axis.plot()

# plt.show()