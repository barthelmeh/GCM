import math, numpy as np
import time

def smoothing(t_e, cutoff):
    r = 2 * math.pi * cutoff * t_e
    return r / (r + 1)


def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev


class OneEuroFilter:
    def __init__(self, min_cutoff=1.5, beta=0.02,
                 d_cutoff=1.0):
        """Initialize the one euro filter."""
        # The parameters.
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        # Previous values.
        self.coords_prev = np.array([0., 0.])
        self.dcoords_prev = np.array([0., 0.])
        self.prev_call_time = None

    def __call__(self, coords):
        """Compute the filtered signal."""
        if self.prev_call_time is None:
            self.prev_call_time = time.time()
            return coords

        t_e = time.time() - self.prev_call_time

        # The filtered derivative of the signal.
        a_d = smoothing(t_e, self.d_cutoff)
        dcoords = (coords - self.coords_prev) / t_e
        dcoords_hat = exponential_smoothing(a_d, dcoords, self.dcoords_prev)

        # The filtered signal.
        cutoff = self.min_cutoff + self.beta * np.linalg.norm(dcoords_hat)
        a = smoothing(t_e, cutoff)
        coords_hat = exponential_smoothing(a, coords, self.coords_prev)

        # Memorize the previous values.
        self.coords_prev = coords_hat
        self.dcoords_prev = dcoords_hat

        self.prev_call_time = time.time()
        return coords_hat