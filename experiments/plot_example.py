import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))  # find orbits.py and plotting.py

import matplotlib.pyplot as plt
from orbits import R_EARTH
from plotting import plot_transfer

R1 = R_EARTH + 400
R2 = R_EARTH + 800

# The Hohmann ellipse: tangent to both orbits
plot_transfer(R1, R2, R1, R2, title="Hohmann transfer: 400 km to 800 km")

output = os.path.join(os.path.dirname(__file__), "..", "results", "hohmann_transfer.png")
plt.savefig(output, dpi=150, bbox_inches="tight")
plt.show()