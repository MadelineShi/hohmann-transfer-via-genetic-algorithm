"""
plotting.py: draw orbits and transfer ellipses for the Hohmann-transfer GA project.
"""

import math
import numpy as np
import matplotlib.pyplot as plt

from orbits import R_EARTH


def plot_transfer(r_p, r_a, r1, r2, ax=None, title=None):
    """
    Draw Earth, the start and target circular orbits, and one transfer ellipse,
    with Earth at the ellipse's focus and periapsis on the +x axis.

    Args:
        r_p: int
            periapsis of the transfer ellipse, closest distance to Earth's center (km)
        r_a: int
            apoapsis of the transfer ellipse, farthest distance from Earth's center (km)
        r1: int
            radius of the starting circular orbit (km)
        r2: int
            radius of the target circular orbit (km)
        ax: package
            existing matplotlib axes to draw on; if None, a new figure is made
        title: string
            optional title for the plot

    Returns:
        the matplotlib axes, so more ellipses can be drawn on the same plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    theta = np.linspace(0, 2 * math.pi, 400)    # 400 angles around the full orbit

    # Earth, start orbit and target orbit (circles)
    ax.add_patch(plt.Circle((0, 0), R_EARTH, color="#378ADD", alpha=0.3, label="Earth"))
    ax.plot(r1 * np.cos(theta), r1 * np.sin(theta), color="#1D9E75", label=f"Start orbit R1 ({r1:,.0f} km)")
    ax.plot(r2 * np.cos(theta), r2 * np.sin(theta), color="#7F77DD", label=f"Target orbit R2 ({r2:,.0f} km)")

    # Transfer ellipse in polar form, with Earth at the focus
    e = (r_a - r_p) / (r_a + r_p)   # eccentricity
    p = r_p * (1 + e)   # semi-latus rectum
    r = p / (1 + e * np.cos(theta)) # distance from Earth at each angle
    ax.plot(r * np.cos(theta), r * np.sin(theta), color="#D85A30", linewidth=2,
            label=f"Transfer ellipse [{r_p:,.0f}, {r_a:,.0f}] km")

    ax.set_aspect("equal")                          # circles look like circles
    ax.set_xlabel("x (km)")
    ax.set_ylabel("y (km)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8)
    if title:
        ax.set_title(title)
    return ax