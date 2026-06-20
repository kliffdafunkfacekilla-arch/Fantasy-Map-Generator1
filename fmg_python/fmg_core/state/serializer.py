import json
import dataclasses
from typing import Dict, Any

from fmg_python.fmg_core.state.models import Grid, Pack

class StateSerializer:
    @staticmethod
    def to_dict(obj: Any) -> Dict[str, Any]:
        """Convert a dataclass instance to a dictionary."""
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return obj

    @staticmethod
    def save_to_json(obj: Any, filepath: str) -> None:
        """Save a state object to a JSON file."""
        data = StateSerializer.to_dict(obj)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))

    # Loading logic would go here, mapping dicts back to Dataclasses
