from tkinter.messagebox import RETRY
from geom import *
class CameraIntrinsics:
    def __init__(self, 
        fx: float, fy: float,
        px: float, py: float, skew: float, 
        pitch: float, nrows: int, ncols: int
        ):
        self.fx = fx
        self.fy = fy
        self.px = px
        self.py = py
        self.s  = skew
        self.pitch = pitch
        self.nrows = nrows
        self.ncols = ncols

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


class SensorModel:
    def __init__(self, s: Point, vel: Point, p: Point, intr: CameraIntrinsics):
        '''Inputs:
                s -> spacecraft position (ecef)
                linear vel (ecef) -> spacecraft velocity
                p -> boresight (ecef)
        '''
        self.s = s
        self.vel = vel
        self.p = p
        self.intr = intr
        self.az, self.el = self.lookat(p)


    def getTransformToSC(self) -> np.array():
        z = normalize(-self.s)
        y = cross(z, self.v)
        x = cross(y, z)
        Rsc = np.zeros((3,3))
        Rsc[:,0] = x.toArray().T
        Rsc[:,1] = y.toArray().T
        Rsc[:,2] = z.toArray().T
        return Rsc


    def lookat(self, gp: Point) -> tuple[float, float]:
        # Get transform to SC frame
        Rsc = self.getTransformToSC()

        # get pointing vector
        l = normalize(self.p - self.s)

        # get l in SC CS
        lsc = Rsc*l.toArray().T

        # get az el
        az = math.atan2(lsc.y, lsc.x)
        el = math.acos(lsc.z)
        return (az, el)
        

    def g2i(self, gp: Point) -> np.array():
        Rsc = self.getTransformToSC()


class Camera:
    def __init__(self, center):
        pass

def test(p: Point):
    p = normalize(p)
    print(p)


if __name__ == "__main__":
    pass

