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

"""The two burns of a Hohmann transfer from r1 to r2 (eq. 3-8 to 3-12)"""
def hohmann_burns(r1, r2, mu = MU_EARTH):
    a_t = (r1 + r2) / 2 # transfer ellipse, eq. 3-8
    dv1 = vis_viva(r1, a_t, mu) - circular_speed(r1, mu) 
    # burn 1: speed up onto the ellipse
    dv2 = circular_speed(r2, mu) - vis_viva(r2, a_t, mu) 
    # burn 2: speed up onto the larger circle
    return dv1, dv2

"""Total change of velocity of Hohmann transfer (answer key for GA)"""
def hohmann_dv (r1, r2, mu= MU_EARTH):
    dv1, dv2 = hohmann_burns(r1, r2, mu)
    return dv1 + dv2