from typing import Any
from ..core.base import BaseGenerator
from ..core.models import MapState

class BiomeGenerator(BaseGenerator):
    """
    Determines the biome for each cell based on height, temperature, and precipitation.
    """
    def generate(self, state: MapState, **kwargs: Any) -> None:
        """
        Calculates biome categories using a Whittaker-like classification.
        """
        for cell in state.cells:
            if cell.height < 0.25:
                cell.biome = "Marine"
            elif cell.height < 0.3:
                cell.biome = "Wetland" if cell.precipitation > 40 else "Sandy Desert"
            elif cell.temperature < 0:
                cell.biome = "Tundra"
            elif cell.precipitation > 60:
                cell.biome = "Rainforest"
            elif cell.precipitation < 20:
                cell.biome = "Badlands"
            else:
                cell.biome = "Grassland"
