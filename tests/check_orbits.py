import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))  # let Python find orbits.py in src/
from orbits import R_EARTH, circular_speed, vis_viva, hohmann_burns, hohmann_dv, transfer_dv

# Orbits from textbook example (Bate et al., Section 3.4.2, 
# p. 135)
R1 = R_EARTH + 400 # 6,778.137 km
R2 = R_EARTH + 800 # 7,178.137 km
A_T = (R1 + R2) / 2 #transfer ellipse semi-major axis

# Textbook answers, in km/s
BATE_V_CS1 = 7.6686 # circular speed at 400 km
BATE_V_CS2 = 7.4518 # circular speed at 800 km
BATE_V1 = 7.7777 # speed on the transfer ellipse at 400
BATE_V2 = 7.3443 # speed on the transfer ellipse at 800
BATE_DV1 = 0.1091 # first burn
BATE_DV2 = 0.1076 # second burn
BATE_DV_TOTAL = 0.2167 # total delta-v

HOHMANN = hohmann_dv(R1, R2) # Hohmann change in velocity value

def check_speeds(name, our_value, bate_value):
    """
    Check circular and vis-viva speeds against textbook answers
    
    Parameters
    ----------
    name: string
        the points on the orbits or ellipses we are checking
    our_value: int
        the velocity of that point
    bate_value:
        the velocity found in the textbook
    
    Returns
    -------
    Prints a message if our velocity matches the textbook or not, 
    via boolean conditions

    """
    if round(our_value, 4) == bate_value:
        result = "MATCH"
    else:
        result = "DOES NOT MATCH"
    print(f"{name:<20} mine = {our_value:.4f}   book = {bate_value}   {result}")

def check_costs_more(name, our_value, hohmann_value):
    """
    Check whether an off-tangent transfer costs more fuel than Hohmann

    Parameters
    ----------
    name: string
        the points on the orbits or ellipses we are checking
    our_value: int
        the velocity of that point
    hohmann_value: int
        the total change of velocity for R1 and r2
    
    Returns
    -------
    Prints one line showing both values and whether ours costs more.
    """
    if our_value > hohmann_value:
        result = "COSTS MORE (correct)"
    else: 
        result = "DEOS NOT COST MORE (incorrect)"
    print(f"{name:<20} mine = {our_value:.4f}   Hohmann = {hohmann_value:.4f}   {result}")

check_speeds("v_c at 400 km", circular_speed(R1), BATE_V_CS1)
check_speeds("v_c at 800 km", circular_speed(R2), BATE_V_CS2)
check_speeds("v1 on ellipse", vis_viva(R1, A_T), BATE_V1)
check_speeds("v2 on ellipse", vis_viva(R2, A_T), BATE_V2)

DV1, DV2 = hohmann_burns(R1, R2)
check_speeds("dv1 (burn 1)", DV1, BATE_DV1)
check_speeds("dv2 (burn 2)", DV2, BATE_DV2)
check_speeds("dv total", hohmann_dv(R1, R2), BATE_DV_TOTAL)
check_speeds("tangent transfer_dv", transfer_dv(R1, R2, R1, R2), BATE_DV_TOTAL)

check_costs_more("r_p 200 km lower", transfer_dv(R1 - 200, R2, R1, R2), HOHMANN)
check_costs_more("r_a 500 km higher", transfer_dv(R1, R2 + 500, R1, R2), HOHMANN)
check_costs_more("both genes off", transfer_dv(R1 - 300, R2 + 400, R1, R2), HOHMANN)
check_costs_more("r_p only 1 km lower", transfer_dv(R1 - 1, R2, R1, R2), HOHMANN)