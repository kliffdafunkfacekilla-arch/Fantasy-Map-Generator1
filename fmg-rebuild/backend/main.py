import asyncio
import math
import random
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.weather import router as weather_router
from agents.demographics import router as demographics_router
from agents.orchestrator import router as orchestrator_router

app = FastAPI(title="Fantasy Map Generator Rebuild API")

app.include_router(weather_router)
app.include_router(demographics_router)
app.include_router(orchestrator_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from simulation.core.models import MapState, Cell
from simulation.pipeline import SimulationPipeline

# In-memory database of active maps
active_maps: Dict[str, MapState] = {}
simulation_pipeline = SimulationPipeline()

def generate_procedural_map(seed: str, width: int, height: int, num_cells: int = 2000) -> MapState:
    """
    Generates a procedural map layout by running the modular simulation pipeline.
    """
    return simulation_pipeline.run_all(seed=seed, width=width, height=height, num_cells=num_cells)

# Real-time WebSocket connection manager for multiplayer sync
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, map_id: str, websocket: WebSocket):
        await websocket.accept()
        if map_id not in self.active_connections:
            self.active_connections[map_id] = []
        self.active_connections[map_id].append(websocket)

    def disconnect(self, map_id: str, websocket: WebSocket):
        if map_id in self.active_connections:
            if websocket in self.active_connections[map_id]:
                self.active_connections[map_id].remove(websocket)

    async def broadcast(self, map_id: str, message: dict, exclude: Optional[WebSocket] = None):
        if map_id in self.active_connections:
            for connection in self.active_connections[map_id]:
                if connection != exclude:
                    await connection.send_json(message)

manager = ConnectionManager()

@app.get("/api/map/{map_id}")
async def get_map(map_id: str, seed: Optional[str] = "fantasy-default", width: int = 1280, height: int = 720):
    if map_id not in active_maps:
        active_maps[map_id] = generate_procedural_map(seed, width, height)
    return active_maps[map_id]

@app.websocket("/ws/map/{map_id}")
async def websocket_endpoint(websocket: WebSocket, map_id: str):
    await manager.connect(map_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Simple operation handler: mutate cell
            if data.get("op") == "MUTATE_CELL":
                cell_id = data.get("cellId")
                changes = data.get("changes", {})
                
                # Apply mutation to internal state
                if map_id in active_maps:
                    map_state = active_maps[map_id]
                    if 0 <= cell_id < len(map_state.cells):
                        cell = map_state.cells[cell_id]
                        for key, val in changes.items():
                            if hasattr(cell, key):
                                setattr(cell, key, val)
                
                # Broadcast delta changes to other connected clients
                await manager.broadcast(
                    map_id=map_id,
                    message={
                        "op": "CELL_MUTATED",
                        "cellId": cell_id,
                        "changes": changes
                    },
                    exclude=websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(map_id, websocket)
