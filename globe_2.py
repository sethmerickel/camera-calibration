import sys
sys.path.insert(0, '.')

import matplotlib.pyplot as plt
from astropy import units as u

from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit
from poliastro.plotting import StaticOrbitPlotter

# Data from Curtis, example 4.3
r = [-6045, -3490, 2500] * u.km
v = [-3.457, 6.618, 2.533] * u.km / u.s

orb = Orbit.from_vectors(Earth, r, v)

static_plotter = StaticOrbitPlotter()
static_plotter.plot(orb)
plt.show()

print('finished')

