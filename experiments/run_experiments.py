"""
run_experiments.py: run the full experiment grid for the Hohmann GA project.

Grid: 2 methods (GA, hill climbing) x 2 encodings (geometric, burn-based)
      x 2 constraint methods (clamp, penalty) x 30 seeds = 240 runs.

Each run gets the same fitness-evaluation budget and saves one CSV log.
"""

import os
import sys
import math
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))  # find files in src/

from orbits import (R_EARTH, R_MIN, hohmann_dv, hohmann_burns, transfer_dv, burn_transfer_dv,
                    geometric_violation, burn_violation)

# The textbook problem: 400 km to 800 km (Bate et al., p. 135)
R1 = R_EARTH + 400  # start orbit radius (km)
R2 = R_EARTH + 800  # target orbit radius (km)
HOHMANN_DV = hohmann_dv(R1, R2) # the answer key, 0.2167 km/s

# Experiment settings (from the project plan)
BUDGET = 1500   # fitness evaluations per run, same for every method
SEEDS = range(30)   # seeds 0 to 29
SUCCESS_TOLERANCE = 1e-4    # a run "succeeds" if it ends within 0.0001 km/s of Hohmann

METHODS = ["ga", "hill_climb"]
ENCODINGS = ["geometric", "burn"]
CONSTRAINTS = ["clamp", "penalty"]

# Where the logs go: results/runs/
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "runs")

def geometric_genome_fitness(genome):
    """
    Total change in velocity (km/s) for a geometric genome with tuple r_p, r_a

    Parameters
    ----------
    genome: tuple
        the periapsis and apoapsis of the transfer ellipse in km
    
    Returns
    -------
    total delta-v of both burns (km/s) if there's no geometric violation,
    else infinity
    """
    r_p, r_a = genome

    # ellipse misses an orbit or hits the atmosphere
    if geometric_violation(r_p, r_a, R1, R2) > 0:
        return math.inf
    return transfer_dv(r_p,r_a, R1, R2)

def geometric_genome_violation(genome):
    """
    How far (km) a geometric genome [r_p, r_a] is from legal

    Parameters
    ----------
    genome: tuple
        the periapsis and apoapsis of the transfer ellipse in km
    
    Returns
    -------
    total violation in km: 0 if the ellipse reaches both orbits and stays
    above R_MIN, otherwise the sum of how far each rule is missed
    """
    r_p, r_a = genome
    return geometric_violation(r_p, r_a, R1, R2)

def burn_genome_fitness(genome):
    """
    Total delta-v (km/s) for a burn genome [dv_t, dv_r]

    Parameters
    ----------
    genome: tuple
        the periapsis and apoapsis of the transfer ellipse in km
    
    Returns
    -------
    total change in velocity of both burns in km/s, or infinity if new
    orbit never reaches r2 (not feasible transfer)

    """
    
    dv_t, dv_r = genome
    return burn_transfer_dv(dv_t, dv_r, R1, R2)

def burn_genome_violation(genome):
    """
    How far (km) a burn genome [dv_t, dv_r] is from legal
    
    Parameters
    ----------
    genome: tuple
        the periapsis and apoapsis of the transfer ellipse in km
    
    Returns
    -------
    total violation in km: 0 if the new orbit reaches r2 and stays above
    R_MIN, infinity if the burn escapes Earth
    """
    
    dv_t, dv_r = genome
    return burn_violation(dv_t, dv_r, R1, R2)

# Allowed range for each gene: (lowest, highest)
GEOMETRIC_BOUNDS = [(R_MIN, R1), (R2, R2 + 400)] # r_p (km), r_a (km)
BURN_BOUNDS = [(-0.2, 0.5), (-0.3, 0.3)] # dv_t (km/s), dv_r (km/s)

def random_search(fitness, violation, bounds, constraint, budget, seed):
    """
    Try random genomes inside the bounds and keep the best one found.
    Stand-in for Madeline's GA, with the same inputs and outputs.

    Parameters
    ----------
        fitness: function
            takes a genome, returns total delta-v in km/s (inf if illegal)
        violation: function
            takes a genome, returns km from legal (not used by random search)
        bounds: list of (low, high)
            allowed range for each gene
        constraint: str
            "clamp" or "penalty" (not used by random search)
        budget: int
            number of fitness evaluations allowed
        seed: int
            seed for the random number generator, so runs are repeatable
    Returns
    -------
    best_genome: list
        the best genome found
    best_fitness: float
        its total delta-v in km/s
    history: list of (int, float)
        (evaluations so far, best fitness so far), each time the best improves
    """

    random.seed(seed) # same seed = same "random" numbers every time

    low_1, high_1 = bounds[0] # range for gene 1
    low_2, high_2 = bounds[1] # range for gene 2

    best_genome = None
    best_fitness = math.inf # anything real beats infinity
    history = [] # (evaluation, best so far) each time the best improves

    for evaluation in range(1, budget + 1):
        genome = [random.uniform(low_1, high_1), random.uniform(low_2, high_2)]
        score = fitness(genome)

        if score < best_fitness: # new best: remember it
            best_fitness = score
            best_genome = genome
            history.append((evaluation, best_fitness))

    return best_genome, best_fitness, history