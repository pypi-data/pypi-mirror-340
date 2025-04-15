from __future__ import annotations

from abc import abstractmethod
from typing import Optional

import numpy as np

from mfire.composite.component import SynthesisModule
from mfire.text.base.builder import BaseBuilder


class SynthesisBuilder(BaseBuilder):
    """
    SynthesisBuilder class that must build synthesis texts
    """

    module_name: str = "synthesis"
    parent: Optional[SynthesisModule] = None

    def _compute(self, **_kwargs) -> Optional[str]:
        """
        Generate the text according to the weather composite

        Args:
            composite (BaseComposite): Composite used to make the reduction.

        Returns:
            str: The built text.
        """
        if not self.parent.check_condition(self.geo_id):
            return None
        return super()._compute()

    @property
    @abstractmethod
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """

    @property
    @abstractmethod
    def template_key(self) -> Optional[str | np.ndarray]:
        """
        Get the template key.

        Returns:
            str | np.ndarray: The template key.
        """
