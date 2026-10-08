from abc import ABC, abstractmethod
from typing import Any
from .models import MapState

class BaseGenerator(ABC):
    """
    Abstract base class for all simulation generators.
    Enforces a standard interface for modules that mutate the MapState.
    """

    @abstractmethod
    def generate(self, state: MapState, **kwargs: Any) -> None:
        """
        Executes the procedural generation logic on the given MapState.

        Args:
            state (MapState): The central map state to read from and mutate.
            **kwargs: Additional optional arguments for the generator.
        """
        pass
