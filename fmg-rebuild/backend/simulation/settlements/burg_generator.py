from typing import Any
from ..core.base import BaseGenerator
from ..core.models import MapState

class BurgGenerator(BaseGenerator):
    """
    Generates settlements (burgs) and assigns populations based on local habitability.
    """
    def generate(self, state: MapState, **kwargs: Any) -> None:
        """
        Calculates placement rating equations (harbors, crossroads, defensive layouts, and capital status).
        """
        pass
