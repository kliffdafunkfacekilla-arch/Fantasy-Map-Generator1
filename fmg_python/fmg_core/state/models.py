from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass
class GridCells:
    i: List[int] # Cell indexes
    c: List[List[int]] # Neighboring cells
    v: List[List[int]] # Vertices indexes
    b: List[int] # Border indicator
    h: List[int] # Elevation
    f: List[int] # Feature index
    t: List[int] # Distance field
    temp: List[int] # Temperature
    prec: List[int] # Precipitation

@dataclass
class GridVertices:
    p: List[List[int]] # Coordinates [x, y]
    c: List[List[int]] # Adjacent cells
    v: List[List[int]] # Adjacent vertices

@dataclass
class Grid:
    cellsDesired: int
    spacing: float
    cellsY: int
    cellsX: int
    points: List[List[float]]
    boundary: List[List[int]]
    cells: GridCells
    vertices: GridVertices
    features: List[Dict[str, Any]]

@dataclass
class PackCells:
    i: List[int]
    p: List[List[float]]
    c: List[List[int]]
    v: List[List[int]]
    b: List[int]
    g: List[int] # Grid parent cell
    h: List[int]
    f: List[int]
    t: List[int]
    s: List[int] # Score
    biome: List[int]
    burg: List[int]
    culture: List[int]
    state: List[int]
    province: List[int]
    religion: List[int]
    good: List[int]
    market: List[int]
    area: List[int]
    pop: List[float]
    r: List[int] # River
    fl: List[int] # Flux
    conf: List[int] # Confluences
    harbor: List[int]
    haven: List[int]
    routes: Dict[int, Dict[int, int]]

@dataclass
class PackVertices:
    p: List[List[int]]
    c: List[List[int]]
    v: List[List[int]]

@dataclass
class Pack:
    cells: PackCells
    vertices: PackVertices
    features: List[Dict[str, Any]]
    cultures: List[Dict[str, Any]]
    burgs: List[Dict[str, Any]]
    states: List[Dict[str, Any]]
    provinces: List[Dict[str, Any]]
    religions: List[Dict[str, Any]]
    rivers: List[Dict[str, Any]]
    markers: List[Dict[str, Any]]
    routes: List[Dict[str, Any]]
    zones: List[Dict[str, Any]]
    ice: List[Dict[str, Any]]
    goods: List[Dict[str, Any]]
    markets: List[Dict[str, Any]]
    deals: List[Dict[str, Any]]
