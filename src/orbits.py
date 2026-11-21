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

def circular_speed(r, mu=MU_EARTH):
    """
    Speed on a circular orbit of radius r (eq. 3-11)

    Parameters
    ----------
    r: int
        orbit radius, measured from Earth's center (km)
    mu: int
        gravitational parameter of central body (km^3/s^2)
    
    Returns
    -------
    circular orbital speed (km/s)
    """
    return math.sqrt(mu/r)

def vis_viva(r, a, mu = MU_EARTH):
    """
    Speed at distance r on an orbit with semi-major 
    axis a (eq. 3-10)

    Parameters
    ----------
    r: int
        current distance from Earth's center (km)
    a: int
        semi-major axis of the orbit, half its longest width (km)
    mu: int
        gravitational parameter of central body (km^3/s^2)
    
    Returns
    -------
    orbital speed at distance r (km/s)
    """
    return math.sqrt(mu * (2 / r - 1 / a))

def hohmann_burns(r1, r2, mu = MU_EARTH):
    """
    The two burns of a Hohmann transfer from r1 to r2 (eq. 3-8 to 3-12)

    Parameters
    ----------
    r1: int
        radius of the starting circular orbit (km)
    r2: int
        radius of the target circular orbit (km)
    mu: int
        gravitational parameter of central body (km^3/s^2)
    
    Returns
    -------
    (dv1, dv2): the first and second burns (km/s)
    """

    a_t = (r1 + r2) / 2 # transfer ellipse, eq. 3-8
    dv1 = vis_viva(r1, a_t, mu) - circular_speed(r1, mu) 
    # burn 1: speed up onto the ellipse
    dv2 = circular_speed(r2, mu) - vis_viva(r2, a_t, mu) 
    # burn 2: speed up onto the larger circle
    return dv1, dv2

def hohmann_dv (r1, r2, mu= MU_EARTH):
    """
    Total change of velocity of Hohmann transfer (answer key for GA)

    Parameters
    ----------
    r1: int
        radius of the starting circular orbit (km)
    r2: int
        radius of the target circular orbit (km)
    mu: int
        gravitational parameter of central body (km^3/s^2)
    
    Returns
    -------
    total delta-v, dv1 + dv2 (km/s)
    """
    dv1, dv2 = hohmann_burns(r1, r2, mu)
    return dv1 + dv2

def burn_at_crossing(r, a, e, mu = MU_EARTH):
    """
    Delta-v to switch between a circular orbit of radius r and an ellipse
    (semi-major axis a, eccentricity e) where they cross. The two 
    velocities differ in size and direction (angle gamma), so the burn
    comes from the Law of Cosines

    Parameters
    ----------
    r: int
        radius of the circular orbit, where the burn happens (km)
    a: int
        semi-major axis of the ellipse (km)
    e: int
        eccentricity of the ellipse (0 = circle, between 0 and 1 = ellipse)
    mu: int
        gravitational parameter of central body (km^3/s^2)
    
    Returns
    -------
    size of the burn (km/s)
    """
    v = vis_viva(r, a , mu) # speed on the ellipse
    v_c = circular_speed(r, mu) # speed on the circle
    h = math.sqrt(mu * a * (1 - e ** 2)) # ellipse's angular momentum
    cos_gamma =  h / (r * v) # flight path angle
    if cos_gamma > 1:
        cos_gamma = 1.0 # guard against going above 1 from rounding

    return math.sqrt(v ** 2 + v_c ** 2 - 2 * v * v_c * cos_gamma)

def transfer_dv(r_p, r_a, r1, r2, mu= MU_EARTH):
    """
    Total delta(v) for the geometric encoding [r_p, r_a], where there's
    a burn at r1 onto the ellipse, then burn at r2 onto the target 
    circle. This is the GA's fitness for the geometric encoding.
    Ideally, we achieve lower values for better fitness.

    Parameters
    ----------
    r_p: int
        periapsis, the ellipse's closest distance to Earth's center (gene 1, km)
    r_a: int
        apoapsis, the ellipse's farthest distance from Earth's center (gene 2, km)
    r1: int
        radius of the starting circular orbit (km)
    r2: int
        radius of the target circular orbit (km)
    mu: int
        gravitational parameter of central body (km^3/s^2)
    
    Returns
    -------
    total delta-v of both burns (km/s)
    """
    a = (r_p + r_a) / 2 # semi-major axis
    e = (r_a - r_p) / (r_a + r_p) # eccentricity
    return burn_at_crossing(r1, a, e, mu) + burn_at_crossing(r2, a, e, mu)

def burn_transfer_dv(dv_t, dv_r, r1, r2, mu = MU_EARTH):
    """
    Total change in velocity for burn-based encoding [dv_t, dv_r]. A first
    burn on the starting circle creates the new orbit, then a second burn
    at r2 puts the spacecraft on the target circle. This is how we derive
    the Genetic Algorithm's fitness for the burn-based encoding, with lower
    values mean better fitness.

    Parameters
    ----------
        dv_t: int
            forward (tangential) part of the first burn [gene 1] in km/s
        dv_r: int
            outward (radial) part of the second burn [gene 2] in km/s
        r1: int
            radius of starting circular orbit in km
        r2: int
            radius of target circular orbit in km
        mu: int
            gravitational parameter of the central body in km^3/s^2
    Returns
    -------
    total change in velocity of both burns in km/s, or infinity if new
    orbit never reaches r2 (not feasible transfer)
    """

    v_t = circular_speed(r1, mu) + dv_t # forward speed after burn
    v_r = dv_r  # outward speed after burn
    v_squared = v_t ** 2 + v_r ** 2 # total speed, squared

    if v_squared >= 2 * mu / r1:    # too fast, will escape Earth's orbit
        return math.inf

    h = r1 * v_t    # angular momentum
    a = 1 / (2 / r1 - v_squared / mu)   # semi-major axis, from vis-viva eq
    e_squared =  1 - h ** 2 / (mu * a)
    if e_squared < 0:
        e_squared = 0.0
    e = math.sqrt(e_squared) # eccentricity, guarded against rounding below 0
    r_a = a * (1 + e) # farthest point of new orbit

    if r_a < r2:    # never reaches target orbit
        return math.inf
    
    burn_1 = math.sqrt(dv_t ** 2 + dv_r ** 2)   # size of first burn
    burn_2 = burn_at_crossing(r2, a, e, mu) # second burn, onto target circle
    
    return burn_1 + burn_2