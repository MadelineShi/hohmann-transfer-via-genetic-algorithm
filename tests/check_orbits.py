from orbits import R_EARTH, circular_speed, vis_viva

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

def check_speeds(name, our_value, bate_value):
    if round(our_value, 4) == bate_value:
        result = "MATCH"
    else:
        result = "DOES NOT MATCH"
    print(f"{name:<20} mine = {our_value:.4f}   book = {bate_value}   {result}")

check_speeds("v_c at 400 km", circular_speed(R1), BATE_V_CS1)
check_speeds("v_c at 800 km", circular_speed(R2), BATE_V_CS2)
check_speeds("v1 on ellipse", vis_viva(R1, A_T), BATE_V1)
check_speeds("v2 on ellipse", vis_viva(R2, A_T), BATE_V2)