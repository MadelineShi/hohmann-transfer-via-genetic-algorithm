"""
orbits.py: orbit math for the Hohmann-transfer GA project.
Formulas from Bate, Mueller, White and Saylor, Fundamentals of
Astrodynamics, 2nd ed., Section 3.4.2. 

Units: km and km/s.

All radii are measured from Earth's CENTER, not its surface.
"""
import math

# Earth's gravitational parameter, in km^3/s^2
MU_EARTH = 398600.4418 
# Earth's radius, in km
R_EARTH = 6378.137

"""Speed on a circular orbit of radius r (eq. 3-11)"""
def circular_speed(r, mu=MU_EARTH):
    return math.sqrt(mu/r)

"""Speed at distance r on an orbit with semi-major 
axis a (eq. 3-10)"""
def vis_viva(r, a, mu = MU_EARTH):
    return math.sqrt(mu * (2 / r - 1 / a))