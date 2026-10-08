import math
import random
from typing import Any
from ..core.base import BaseGenerator
from ..core.models import MapState

class ClimateGenerator(BaseGenerator):
    """
    Generates temperature and precipitation based on latitude and elevation.
    """
    def generate(self, state: MapState, **kwargs: Any) -> None:
        """
        Calculates temperature and precipitation for each cell.
        """
        random.seed(state.seed)
        for cell in state.cells:
            # Climate simulation (temperature decreases with latitude/y coordinate)
            lat_factor = 1.0 - (cell.y / state.height) if state.height > 0 else 0.5
            cell.temperature = 25 * math.sin(lat_factor * math.pi) + random.uniform(-2, 2)

            # Precipitation based on noise
            cell.precipitation = max(0.0, 100 * (math.sin(cell.x * 0.01) * math.cos(cell.y * 0.01) + 1.0) / 2.0 + random.uniform(-10, 10))
