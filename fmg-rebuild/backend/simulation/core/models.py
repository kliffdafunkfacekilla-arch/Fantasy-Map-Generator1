from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Cell(BaseModel):
    """Represents a single Voronoi cell on the map."""
    id: int
    x: float
    y: float
    height: float = 0.0
    biome: str = "Marine"
    temperature: float = 0.0
    precipitation: float = 0.0
    state_id: Optional[int] = None
    culture_id: Optional[int] = None
    burg_id: Optional[int] = None
    province_id: Optional[int] = None
    religion_id: Optional[int] = None

class Burg(BaseModel):
    """Represents a settlement (burg)."""
    id: int
    name: str
    cell_id: int
    population: int = 0
    state_id: Optional[int] = None
    culture_id: Optional[int] = None

class State(BaseModel):
    """Represents a political state."""
    id: int
    name: str
    capital_burg_id: Optional[int] = None
    color: str = "#000000"

class Culture(BaseModel):
    """Represents a cultural group."""
    id: int
    name: str
    type: str = "Generic"
    color: str = "#ffffff"

class MapState(BaseModel):
    """The central state store containing all map data."""
    seed: str = "fantasy-default"
    width: int = 1280
    height: int = 720
    cells: List[Cell] = Field(default_factory=list)
    burgs: List[Burg] = Field(default_factory=list)
    states: List[State] = Field(default_factory=list)
    cultures: List[Culture] = Field(default_factory=list)

    # Allows adding arbitrary properties like specific module configurations
    metadata: Dict[str, str] = Field(default_factory=dict)
