from typing import List
from .core.models import MapState
from .core.base import BaseGenerator
from .grid.grid_generator import GridGenerator
from .grid.heightmap_generator import HeightmapGenerator
from .climate.climate_generator import ClimateGenerator
from .hydrology.hydrology_generator import HydrologyGenerator
from .geography.biome_generator import BiomeGenerator
from .civilization.culture_generator import CultureGenerator
from .civilization.religion_generator import ReligionGenerator
from .political.state_generator import StateGenerator
from .political.province_generator import ProvinceGenerator
from .settlements.burg_generator import BurgGenerator
from .settlements.route_generator import RouteGenerator
from .economy.economy_generator import EconomyGenerator

class SimulationPipeline:
    """
    Orchestrates the sequential execution of map simulation generators.
    Ensures data dependencies between layers are respected.
    """
    def __init__(self):
        # The exact order here matters. Later generators depend on the output of earlier ones.
        self.generators: List[BaseGenerator] = [
            GridGenerator(),
            HeightmapGenerator(),
            ClimateGenerator(),
            HydrologyGenerator(),
            BiomeGenerator(),
            CultureGenerator(),
            StateGenerator(),
            BurgGenerator(),
            ProvinceGenerator(),
            ReligionGenerator(),
            RouteGenerator(),
            EconomyGenerator(),
        ]

    def run_all(self, seed: str, width: int = 1280, height: int = 720, num_cells: int = 2000) -> MapState:
        """
        Executes the entire simulation pipeline from scratch and returns the final MapState.
        """
        state = MapState(seed=seed, width=width, height=height)

        for generator in self.generators:
            # Pass extra kwargs if needed by specific generators.
            # In a more advanced pipeline, we might pass specific configs per generator.
            if isinstance(generator, GridGenerator):
                generator.generate(state, num_cells=num_cells)
            else:
                generator.generate(state)

        return state
