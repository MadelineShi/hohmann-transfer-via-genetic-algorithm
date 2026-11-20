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

def burn_at_crossing(r, a, e, mu = MU_EARTH):
    """
    Delta-v to switch between a circular orbit of radus r and an ellipse
    (semi-major axis a, eccentricity e) where they cross. The two 
    velocities differ in size and direction (angle gamma), so the burn
    comes from the Law of Cosines
    """
    v = vis_viva(r, a , mu) # speed on the ellipse
    v_c = circular_speed(r, mu) # speed on the circle
    h = math.sqrt(mu * a * (1 - e ** 2)) # ellipse's angular momentum
    cos_gamma = min(1.0, h / (r * v)) # flight path angle; minimum to
    # ensure no rounding above 1

    return math.sqrt(v ** 2 + v_c ** 2 - 2 * v * v_c * cos_gamma)

def transfer_dv(r_p, r_a, r1, r2, mu= MU_EARTH):
    """
    Total delta(v) for the geometric encoding [r_p, r_a], where there's
    a burn at r1 onto the ellipse, then burn at r2 onto the target 
    circle. This is the GA's fitness for the geometric encoding.
    Ideally, we achieve lower values for better fitness.
    """
    a = (r_p + r_a) / 2 # semi-major axis
    e = (r_a - r_p) / (r_a + r_p) # eccentricity
    return burn_at_crossing(r1, a, e, mu) + burn_at_crossing(r2, a, e, mu)

