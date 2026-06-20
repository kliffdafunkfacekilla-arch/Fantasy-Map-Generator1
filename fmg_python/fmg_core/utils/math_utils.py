import math
from typing import List, Tuple

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate euclidean distance between two points."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_center(polygon: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Calculate the centroid of a polygon."""
    x_sum = sum(p[0] for p in polygon)
    y_sum = sum(p[1] for p in polygon)
    n = len(polygon)
    if n == 0:
        return 0.0, 0.0
    return x_sum / n, y_sum / n
