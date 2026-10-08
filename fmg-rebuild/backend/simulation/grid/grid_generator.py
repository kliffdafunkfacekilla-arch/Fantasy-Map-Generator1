import random
from typing import Any
from ..core.base import BaseGenerator
from ..core.models import MapState, Cell

class GridGenerator(BaseGenerator):
    """
    Generates the underlying Voronoi structure or grid cells for the map.
    """
    def generate(self, state: MapState, num_cells: int = 2000, **kwargs: Any) -> None:
        """
        Creates the grid points and initial cell objects.
        """
        random.seed(state.seed)
        state.cells = []
        for i in range(num_cells):
            x = random.uniform(0, state.width)
            y = random.uniform(0, state.height)
            state.cells.append(Cell(id=i, x=x, y=y))
