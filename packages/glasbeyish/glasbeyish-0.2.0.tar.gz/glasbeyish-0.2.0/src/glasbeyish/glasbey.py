from itertools import combinations
from typing import Optional, Callable, Iterable, Iterator
from numbers import Number

import numpy as np
import hsluv as hsluv_
from nice_colorsys.hsluv import luv
from multiset_key_dict import MultisetKeyDict
from heap_mapping import MinMaxHeap

default_rng = np.random.default_rng()

def random_luv(
        rng: Optional[np.random.Generator] = None,
        limit: Callable[[luv], bool] = lambda x: True
) -> luv:
    """Generate a random color in the CIELUV color space.

    Parameters:
        rng:   The pseudo-random number generator to use.
        limit: A function that returns true iff the generated color is valid.

    Returns:
        A random color represented in the CIELUV color space.
    """
    if rng is None:
        rng = np.random.default_rng()
    while True:
        color = luv(
            rng.uniform(0, 100),
            rng.uniform(-134, 220),
            rng.uniform(-140, 122)
        )
        L, C, h = color.to_cielch()
        if C <= hsluv_._max_chroma_for_lh(L, h) and limit(color):
            break
    return color

def geom_schedule(init: Number, steps: int, mul: Number) -> Iterator[Number]:
    """Generate a geometric sequence init, init*mul, ... init*mul**steps.

    Parameters:
        init:  The constant coefficient, the initial value.
        steps: The number of elements in the sequence.
        mul:   The base of the exponent, amount by which to multiply per step.
    """
    for _ in range(steps):
        yield init
        init *= mul

def euclidean_distance(a, b):
    return np.linalg.norm(b - a)

def glasbey_simulated_annealing(
        n: int,
        rng: Optional[np.random.Generator] = None,
        seed: int = None,
        schedule: Optional[Iterable[Number]] = None,
        steps: int = 10_000,
        random_color: Callable = random_luv,
        color_dist: Callable = euclidean_distance,
        **random_kwargs
) -> tuple[list[luv], np.float64]:
    """Find a palette of distinct colors using simulated annealing.

    The colors are generated using a method similar the simulated annealing
    method described in the paper "Colour Displays for Categorical Images" by
    Glasbey et al.

    If no pseudo-random number generator (PRNG) is provided, the default is to
    use the np.random.default_rng generator.

    Parameters:
        n (int):      The number of colors to produce.
        rng:          The PRNG to use.
        seed (int):   Random seed to use if no PRNG is provided.
        schedule:     Schedule of temperatures to use for simulated annealing.
        steps (int):  Steps to take in simulated annealing optimization.
        random_color: Function to get a random color; first parameter is PRNG.
        color_dist:   Function to get distance of two colors as numpy arrays.

    Returns:
        Generated palette and minimum pairwise distance among colors.
    """    
    if rng is None:
        rng_args = []
        if seed is not None:
            rng_args.append(seed)
        rng = np.random.default_rng(*rng_args)
    if schedule is None:
        schedule = geom_schedule(1, steps, 0.99)
    random_kwargs["rng"] = rng
    colors = np.array([random_color(**random_kwargs) for _ in range(n)])
    dists = MultisetKeyDict(mapping_type=MinMaxHeap)
    for (i, a), (j, b) in combinations(enumerate(colors), 2):
        dists[[i, j]] = color_dist(a, b)
    for temperature in schedule:
        argmin = list(dists.min_value.distinct())
        #print(argmin)
        old_min = dists[argmin]
        new_color = np.array(random_color(**random_kwargs))
        choice = argmin[int(rng.random() < 0.5)]
        old_dists = MultisetKeyDict()
        for i, _ in enumerate(colors):
            if i != choice:
                old_dists[[i, choice]] = dists[[i, choice]]
        for i, c in enumerate(colors):
            if i != choice:
                dists[[i, choice]] = color_dist(new_color, c)
        new_min = dists.min.priority
        if rng.random() <= min(1, np.exp((new_min - old_min)/temperature)):
            colors[choice] = new_color
        else:
            for i, c in enumerate(colors):
                if i != choice:
                    dists[[i, choice]] = old_dists[[i, choice]]
    return [luv(*c) for c in colors], dists[argmin]

def glasbey(*args, **kwargs) -> list[luv]:
    """Wrapper for glasbey_simulated_annealing that only returns the palette."""
    return glasbey_simulated_annealing(*args, **kwargs)[0]
