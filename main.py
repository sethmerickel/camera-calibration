import camera_calibration as cc
import geom
import utils

if __name__ == "__main__":
    DEBUG = True
    
    #look at L3Harris
    lat_l3h = 41.1444306
    lon_l3h = -85.1658274
    alt_l3h = 261.78179 - 33.3832 # HAE Height. HAE = ORTH + UNDULATION

    gp = geom.Point.fromArray(utils.lla2xyz(lat_l3h, lon_l3h, alt_l3h))
    sc = gp + geom.normalize(gp)*1000*10**3 # 1000km radially outward from the ground point

    # Get a velocity direction. It doesn't really matter, but pick something that is 
    # debuggable
    z_hat = geom.Point.zHat()
    sc_hat = geom.normalize(sc)
    v_hat = geom.cross(z_hat, sc_hat)
    vel = v_hat*7.8*10**3 #7.8km/sec

    if DEBUG is True:
        print(f"z_hat: {gp}")
        print(f"z_hat: {sc}")
        print(f"sc_hat: {sc_hat}")
        print(f"v_hat: {v_hat}")
        print(f"vel: {vel}")

    
    sm = cc.SensorModel(sc, vel, gp,)

