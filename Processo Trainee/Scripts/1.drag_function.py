import numpy as np

def drag_function(V, rho, S, CD0, W, e, AR):
    return (
        0.5 * rho * V**2 * S * CD0
        + (2 * W**2) / (rho * V**2 * S * np.pi * e * AR)
    )