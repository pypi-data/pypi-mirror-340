from abc import abstractmethod
from typing import Dict, List, Optional

from mfire.composite.component import SynthesisModule
from mfire.settings import get_logger
from mfire.text.base.reducer import BaseReducer
from mfire.utils.period import PeriodDescriber

LOGGER = get_logger(name="synthesis_reducer.mod", bind="synthesis_reducer")


class SynthesisReducer(BaseReducer):
    parent: SynthesisModule

    @abstractmethod
    def _compute(self, **_kwargs) -> Dict | List[Dict]:
        """
        Abstract method in order to make computation and returns the reduced data in
        child classes

        Returns:
            Dict | List[Dict]: Reduced data
        """

    @property
    def period_describer(self) -> PeriodDescriber:
        return self.parent.parent.period_describer

    def has_risk(self, risk_name: str) -> Optional[bool]:
        """
        Checks if a specific risk occurred within a given geographical area and
        timeframe.

        Args:
            risk_name (str): The name of the risk to check for.

        Returns:
            Optional[bool]:
                - True if the specified risk occurred within the area and timeframe.
                - False if the risk does not happen.
                - None if there is no risk within the given geographical area and
                    timeframe.
        """
        valid_time = self.parent_data["valid_time"].data
        return self.parent.interface.has_risk(
            risk_name,
            self.parent.geos.all_sub_areas(self.geo_id),
            slice(valid_time[0], valid_time[-1]),
        )

    def has_field(self, risk_name, field: str) -> Optional[bool]:
        """
        Checks if a specific risk has given field configured within a given geographical
        area.

        Args:
            risk_name (str): The name of the risk to check for.
            field (str): The name of the field to check for.

        Returns:
            Optional[bool]:
                - True if the specified risk uses field.
                - False if the risk does not use field.
                - None if there is no risk within the given geographical area.
        """
        return self.parent.interface.has_field(
            risk_name, field, self.parent.geos.all_sub_areas(self.geo_id)
        )
