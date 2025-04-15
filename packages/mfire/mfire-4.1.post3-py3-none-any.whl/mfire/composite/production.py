from __future__ import annotations

from itertools import product
from typing import Callable, ClassVar, List, Optional

from pydantic import model_validator

from mfire.composite.base import BaseComposite
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
    SynthesisCompositeInterface,
    TypeComponent,
)
from mfire.settings import get_logger
from mfire.text.manager import Manager
from mfire.text.risk.builder import RiskBuilder

# Logging
LOGGER = get_logger(name="productions.mod", bind="productions")


class ProductionComposite(BaseComposite):
    """
    Represents a ProductionComposite object containing the configuration of the
    Promethee production task.

    Args:
        baseModel: Pydantic base model.

    Returns:
        baseModel: Production object.
    """

    id: str
    name: str
    config_hash: str
    config_language: str
    config_time_zone: str
    mask_hash: str
    components: List[RiskComponentComposite | SynthesisComponentComposite]
    sort: float
    risk_builders: list[RiskBuilder] = []
    kept_hazard_names: ClassVar[list[str]] = ["Vent", "Rafales"]

    _shared_config: dict = {}

    @model_validator(mode="after")
    def init_shared_config(self) -> ProductionComposite:
        self.shared_config["language"] = self.config_language
        self.shared_config["time_zone"] = self.config_time_zone
        return self

    @property
    def sorted_components(
        self,
    ) -> List[RiskComponentComposite | SynthesisComponentComposite]:
        risks, synthesis = [], []
        for component in self.components:
            if component.type == TypeComponent.RISK:
                risks.append(component)
            else:
                synthesis.append(component)
        return risks + synthesis

    def has_risk(
        self, hazard_name: str, ids: List[str], valid_time: slice
    ) -> Optional[bool]:
        """
        Checks if a risk with the given hazard name has occurred for any of the provided
        IDs within the specified time slice.

        Args:
            hazard_name (str): The name of the hazard to check for.
            ids (List[str]): A list of IDs to check for risks.
            valid_time (slice): A time slice object representing the valid time
                range to consider.

        Returns:
            Optional[bool]:
                - True if a risk with the specified hazard name is found for any of the
                    IDs within the time slice.
                - False if there is no risks with the specified hazard name for the
                    given IDs and time slice.
                - None if there are no relevant components to check or if there are no
                    entries for the provided IDs.
        """
        for component in self.components:
            if (
                component.type == TypeComponent.SYNTHESIS
                or component.hazard_name != hazard_name
            ):
                continue

            return component.has_risk(ids, valid_time=valid_time)

    def has_field(self, hazard_name: str, field: str, ids: List[str]) -> Optional[bool]:
        """
        Checks if a specific risk with the given hazard name uses field values for any
        of the provided IDs within the specified time slice.

        Args:
            hazard_name (str): The name of the hazard to check for.
            field (str): The name of the field to check for.
            ids (List[str]): A list of IDs to check for risks.

        Returns:
            Optional[bool]:
                - True if a risk with the specified hazard name uses field values
                - False if a risk with the specified hazard name does not use field
                    values
                - None if there are no relevant components to check or if there are no
                    entries for the provided IDs.
        """
        for component in self.components:
            if (
                component.type == TypeComponent.SYNTHESIS
                or component.hazard_name != hazard_name
            ):
                continue

            return component.has_field(field, ids)

    def _get_sub_axis(self, geo_id: str) -> set[str]:
        """Get all the production axis contained in the axis with id geo_id."""
        sub_axis: set[str] = set()

        for component in self.components:
            if component.type == TypeComponent.SYNTHESIS:
                continue
            for level in component.levels:
                for event in level.events:
                    sub_axis.update(event.geos.all_sub_areas(geo_id))

        return sub_axis

    @staticmethod
    def _get_extreme_critical_values(
        builder: RiskBuilder, valid_time: slice, field_name: str, data_types: list[str]
    ) -> dict:
        """Get extreme critical values (min and/or max) in plain and/or mountain."""
        risk_infos: dict = {"pm_sep": False, "activated_risk": False}
        functions: dict[str, Callable] = {"min": min, "max": max}

        crt_values: dict = builder.reducer.get_critical_values(valid_time, field_name)

        if crt_values:
            for data_type, qualif in product(data_types, ["plain", "mountain"]):
                crt_value: dict = crt_values[field_name].get(qualif)
                if crt_value is None:
                    continue

                rep_value, local = builder.parent.replace_critical(crt_value)
                values: list[float] = list(
                    filter(lambda e: e is not None, [rep_value, local])
                )

                risk_infos[f"{qualif}_{data_type}"] = round(
                    functions[data_type](values) if values else crt_value, 2
                )

            # If critical values found, then check if there is plain/mountain
            # separation and set activated_risk to True
            pm_sep: bool = builder.parent.is_plain_mountain_separated(field_name)
            risk_infos["pm_sep"] = pm_sep
            risk_infos["activated_risk"] = True

        return risk_infos

    @classmethod
    def update_extreme_values(
        cls, risk_infos: dict, risk_infos_new: dict, data_types: list[str]
    ) -> None:
        """Update risk_infos with min and/or max of risk_infos and risk_infos_new."""
        functions: dict[str, Callable] = {"min": min, "max": max}

        for data_type, qualif in product(data_types, ["plain", "mountain"]):
            key: str = f"{qualif}_{data_type}"
            value: float = risk_infos_new.get(key)

            if value is not None:
                risk_infos[key] = (
                    functions[data_type](value, risk_infos[key])
                    if key in risk_infos
                    else value
                )

    @classmethod
    def update_risk_infos(
        cls, risk_infos: dict, risk_infos_new: dict, data_types: list[str]
    ) -> None:
        """Update risk's infos with extreme_values.

        Args:
            risk_infos (dict): Risk's infos dictionary.
            risk_infos_new (dict): Another Risk's infos dictionary used for the update.
            data_types (list[str]): data_types as a list which van be [], ['min'],
                ['max'] or ['min', 'max'].

        Returns:
            None.
        """
        # If values from risk_infos_new comes from an activated risk, then it contains
        # True at activated_risk key. Same for risk_infos
        activated_risk_new: bool = risk_infos_new["activated_risk"]
        activated_risk: bool = risk_infos["activated_risk"]

        # If risk_infos values comes from an activated risk, then
        # there is nothing because we simply keep rep values of risk_infos
        if activated_risk is False or activated_risk_new is True:
            # We keep only rep values of risk_infos_new
            if activated_risk is False and activated_risk_new is True:
                # Remove existing extreme values
                for data_type, qualif in product(data_types, ["plain", "mountain"]):
                    risk_infos.pop(f"{qualif}_{data_type}", None)

            # We update risk_infos with min and/or max values of risk_infos and
            # risk_infos_new
            cls.update_extreme_values(risk_infos, risk_infos_new, data_types)

        # Add pm_sep and activated_risk booleans
        risk_infos["pm_sep"] = risk_infos["pm_sep"] or risk_infos_new["pm_sep"]
        risk_infos["activated_risk"] = activated_risk or activated_risk_new

    def get_risk_infos(
        self,
        hazard_names: list[str],
        field_name: str,
        geo_id: str,
        valid_time: slice,
        data_types: list[str],
    ) -> dict[str, float | int | bool]:
        """Get the risk information from computed RiskBuilders.

        Args:
            hazard_names (list[str]): Hazard names concerned by the lookup.
            field_name (str): Field name of the risk.
            geo_id (str): Geo id of the risk.
            valid_time (slice): A time slice object representing the valid time
                range to consider.
            data_types (list[str]): data_types as a list which van be [], ['min'],
                ['max'] or ['min', 'max'].

        Returns:
            dict[str, float]: a dictionary with the risk's infos.
        """
        risk_infos: dict[str, float | int | bool] = {
            "pm_sep": False,
            "activated_risk": False,
        }

        # Get all the production axis contained in the axis with id geo_id
        sub_axis: set[str] = self._get_sub_axis(geo_id)

        # For all builder, get the critical values. If there is not, get the rep
        # values. If there is not, get the plain/mountain extreme values
        for builder in self.risk_builders:
            # Process only risk component
            if (
                builder.parent.type == TypeComponent.SYNTHESIS
                or builder.parent.hazard_name not in hazard_names
            ):
                continue

            if builder.geo_id not in sub_axis:
                continue

            risk_infos_cur: dict

            # Get the critical values of the current builder if multi zone risk
            if builder.is_multizone is True:
                risk_infos_cur = self._get_extreme_critical_values(
                    builder, valid_time, field_name, data_types
                )

            # If not multi zone risk, then get rep values or plain/mountain extreme
            # values
            else:
                risk_infos_cur = builder.parent.get_risk_infos(
                    field_name, builder.geo_id, valid_time, data_types
                )

            # Update the global risk_infos with risk_infos_cur
            self.update_risk_infos(risk_infos, risk_infos_cur, data_types)

        return risk_infos

    def add_interface(
        self, component: RiskComponentComposite | SynthesisComponentComposite
    ):
        # Add the interface between risk and synthesis
        if component.type == TypeComponent.SYNTHESIS:
            for weather in component.weathers:
                weather.interface = SynthesisCompositeInterface(
                    has_risk=self.has_risk,
                    has_field=self.has_field,
                    get_risk_infos=self.get_risk_infos,
                )

    def _compute(self, **_kwargs) -> List[dict]:
        """
        Compute the production task by iterating over the components and invoking
        their compute method.
        """
        result = []

        for component in self.sorted_components:
            log_ids = {
                "production_id": self.id,
                "production_name": self.name,
                "component_id": component.id,
                "component_name": component.name,
                "component_type": component.type,
            }
            self.add_interface(component)

            # Compute the component
            if not bool(component.compute()):
                result.append(None)
                continue

            # Handle of the generation of the text
            text_manager = Manager(parent=component)
            texts = {}
            for geo_id in component.geos:
                try:
                    text = text_manager.compute(geo_id=geo_id)
                except Exception:
                    LOGGER.error(
                        "Failed to generate text on geo",
                        geo_id=geo_id,
                        **log_ids,
                        exc_info=True,
                    )
                    text = self._(
                        "Ce commentaire n'a pas pu être produit à cause d'un incident "
                        "technique."
                    )

                texts[geo_id] = text

                if (
                    component.type == TypeComponent.RISK
                    and component.hazard_name in self.kept_hazard_names
                ):
                    self.risk_builders.append(text_manager.risk_builder)

            result.append(texts)
        return result
