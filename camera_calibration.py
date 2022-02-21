from geom import *
import utils

# class CameraIntrinsics:
#     def __init__(self, 
#         fx: float, fy: float,
#         px: float, py: float, skew: float, 
#         pitch: float, nrows: int, ncols: int
#         ):
#         self.fx = fx
#         self.fy = fy
#         self.px = px
#         self.py = py
#         self.s  = skew
#         self.pitch = pitch
#         self.nrows = nrows
#         self.ncols = ncols

#     def getMatrix(self):
#         fx = self.fx
#         fy = self.fy
#         px = self.px
#         py = self.py
#         s  = self.s
#         return np.array(
#             [
#                 [fx, s, px],
#                 [0, fy, py],
#                 [0,  0, 1.0]
#             ])

class CameraIntrinsics:

    def __init__(self,
        f: float, px: float, py: float, pitch: float,
        image_width: int, image_height: int,
        k1: float = 0, k2: float = 0, k3: float = 0,
        p1: float = 0, p2: float = 0):

        self.f     = f # focal length [mm]
        self.px    = px # principle point offset x [pixels]
        self.py    = py # principle point offset y [pixels]
        self.pitch = pitch # pitch [mm]
        self.k1    = k1 # radial distortion
        self.k2    = k2 # radial distortion
        self.k3    = k3 # radial distortion
        self.p1    = p1 # tangential distortion
        self.p2    = p2 # tangential distortion

    def project(self, theta_x: float, theta_y: float) -> tuple[float, float]:
        '''
        theta_x = tangential field angle in the z-x plane [radians]
        theta_y = tangential field angle in the z-y plane [radians]
        '''
        x = -self.f * math.tan(theta_x)
        y = -self.f * math.tan(theta_y)
        return (x, y)

    def getRadialDistortion(self):
        pass

    def getTangentialDistortion(self):
        pass
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

    def ecefToSc(self) -> np.array():
        z = normalize(-self.s)
        y = cross(z, self.v)
        x = cross(y, z)
        Rsc = np.zeros((3,3))
        Rsc[:,0] = x.toArray().T
        Rsc[:,1] = y.toArray().T
        Rsc[:,2] = z.toArray().T
        return Rsc

    def getAzEl(self, gp: Point) -> tuple[float, float]:
        # Get transform to SC frame
        Rsc = self.ecefToSc()

        # get pointing (boresight) vector
        l = normalize(self.p - self.s)

        # get l in SC CS
        lsc = Rsc @ l.toArray().T

        # get az el
        az = math.atan2(lsc.y, lsc.x)
        el = math.acos(lsc.z)
        return (az, el)

    @staticmethod
    def getAzReflectionMatrix(az: float) -> np.array:
        '''
        az -> azimuth angle [radians]
        returns reflection matrix for azimuth mirror in the instrument reference frame
        '''
        n_az = np.array([[1/np.sqrt(2), 0, -1/np.sqrt(2)]])
        Rz = utils.rotationZ(az)
        n_az = Rz @ n_az
        M = np.eye(3) - 2 * (n_az @ n_az.T)
        return M

    @staticmethod
    def getElReflectionMatrix(el: float, az: float) -> np.array:
        '''
        az -> azimuth angle [radians]
        el -> elevation angle [radians]
        returns reflection matrix for elevation mirror in the instrument reference frame
        '''
        n_el = np.array([[-1/np.sqrt(2), 0, 1/sqrt(2)]])
        Rz = utils.rotationZ(az)
        Rx = utils.rotationX(el)
        n_el = Rx @ Rz @ n_el
        M = np.eye(3) - 2 * (n_el @ n_el.T)
        return M

    @staticmethod
    def getTangentialAngles(i: Point) -> tuple[float, float]:
        pass
        
    def g2i(self, gp: Point) -> np.array():
        Rsc = self.ecefToSc()
        (az, el) = self.getAzEl()
        Maz = self.getAzReflectionMatrix(az)
        Mel = self.getElReflectionMatrix(el)


if __name__ == "__main__":
    pass

