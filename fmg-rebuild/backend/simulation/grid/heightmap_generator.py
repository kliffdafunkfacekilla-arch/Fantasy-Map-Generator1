import math
import random
from typing import Any
from ..core.base import BaseGenerator
from ..core.models import MapState

class HeightmapGenerator(BaseGenerator):
    """
    Applies elevation to the grid cells using noise and radial gradients.
    """
    def generate(self, state: MapState, **kwargs: Any) -> None:
        """
        Calculates height for each cell.
        """
        random.seed(state.seed)
        for cell in state.cells:
            # Simulating radial/island noise for height
            dx = cell.x - state.width / 2
            dy = cell.y - state.height / 2
            dist = math.sqrt(dx*dx + dy*dy)
            max_dist = math.sqrt((state.width/2)**2 + (state.height/2)**2)
            radial_factor = 1.0 - (dist / max_dist) if max_dist > 0 else 0

            # High-frequency noise simulation
            noise = (math.sin(cell.x * 0.05) + math.cos(cell.y * 0.05) + random.uniform(-0.2, 0.2)) / 3.0
            cell.height = max(0.0, min(1.0, radial_factor * 0.6 + noise * 0.4 + 0.2))
