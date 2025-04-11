from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from typing import Callable, ClassVar, List, Optional

import numpy as np
from pydantic import field_validator

from mfire.composite.component import RiskComponentComposite
from mfire.composite.operator import ComparisonOperator
from mfire.text.base.builder import BaseBuilder
from mfire.text.base.geo import BaseGeo
from mfire.text.base.reducer import BaseReducer
from mfire.utils.calc import round_to_previous_multiple
from mfire.utils.lpn import Lpn
from mfire.utils.string import concatenate_string, get_synonym, split_var_name
from mfire.utils.wwmf import Wwmf

_start_stop_str = "{start} à {stop}"


class RepValueReducer(BaseReducer):
    feminine: bool = False
    plural: bool = False
    differentiate_plain_and_mountain: bool = False

    parent: RiskComponentComposite

    @field_validator("infos", mode="before")
    def check_infos(cls, infos: dict) -> dict:
        """Validate if data has a var_name key with an accumulated variable as value."""
        var_name: Optional[str] = infos.get("var_name")
        if var_name is None:
            raise KeyError("Key 'var_name' not found.")

        return infos

    @property
    def phenomenon(self) -> str:
        return ""

    @property
    def def_article(self) -> str:
        """Returns the definite article based on plural and feminine"""
        if self.plural:
            return self._("les")
        return self._("la") if self.feminine else self._("le")

    @property
    def indef_article(self) -> str:
        """Returns the indefinite article based on plural and feminine"""
        if self.plural:
            return self._("des")
        return self._("une") if self.feminine else self._("un")

    @property
    def around_word(self) -> str:
        return self._("de")

    @staticmethod
    def compare(a: dict, b: dict) -> bool:
        """Compares representative values.

        If the plain values are equals or don't exist, the comparison is based on the
        mountain value.

        Args:
            a (dict): First value to compare
            b (dict): Second value to compare.

        Returns:
            bool: True if dictionary a is the largest, False otherwise.
        """
        try:
            operator = ComparisonOperator(a["plain"]["operator"].strict)
            if not operator.is_order or operator(
                a["plain"]["value"], b["plain"]["value"]
            ):
                return True
            if a["plain"]["value"] != b["plain"]["value"]:
                return False
        except KeyError:
            if (plain_in_a := "plain" in a) or "plain" in b:
                return plain_in_a

        try:
            operator = ComparisonOperator(a["mountain"]["operator"].strict)
            return operator.is_order and operator(
                a["mountain"]["value"], b["mountain"]["value"]
            )
        except KeyError:
            return "mountain" in a

    def units(self, unit: Optional[str]) -> str:
        """
        Get the unity. If None then it returns an empty string
        """
        return self._(unit) or ""

    def round(self, x: Optional[float], **_kwargs) -> Optional[str]:
        """
        Make a rounding of the value

        Args:
            x (Optional[float]): Value to round

        Returns:
            [Optional[str]]: String of the rounded value or None if not possible
        """
        return str(x) if x is not None and abs(x) > 1e-6 else None

    @property
    def around(self) -> str:
        """
        Returns a synonym of the around
        """
        return get_synonym(self.around_word, self.language)

    @property
    def definite_var_name(self) -> str:
        """Returns the definite var_name name."""
        return f"{self.def_article} {self.phenomenon}"

    @property
    def indefinite_var_name(self) -> str:
        """Returns the indefinite var_name name."""
        return f"{self.indef_article} {self.phenomenon}"

    def _compute_plain_frmt_table(self, frmt_table: dict) -> Optional[str]:
        if "plain" not in self.infos:
            return None

        plain_dict = self.infos["plain"]
        operator = ComparisonOperator(plain_dict.get("operator"))
        rep_value, local = self.parent.replace_critical(plain_dict)
        rep_plain = self.round(
            rep_value, operator=operator, around=frmt_table["around"]
        )
        if rep_plain is not None:
            if rep_plain != "":
                frmt_table[
                    "plain_value"
                ] = f"{rep_plain} {self.units(plain_dict['units'])}"

            local_plain = self.round(
                local, operator=operator, around=frmt_table["around"]
            )
            if local_plain is not None and local_plain != rep_plain:
                frmt_table[
                    "local_plain_value"
                ] = f"{local_plain} {self.units(plain_dict['units'])}"
        return rep_plain

    def _compute_mountain_frmt_table(self, frmt_table: dict, rep_plain: Optional[str]):
        if "mountain" not in self.infos:
            return
        mountain_dict = self.infos["mountain"]
        operator = ComparisonOperator(mountain_dict.get("operator"))
        rep_value, local = self.parent.replace_critical(mountain_dict)
        rep_mountain = self.round(
            rep_value, operator=operator, around=frmt_table["around"]
        )
        if rep_mountain is not None and (
            self.differentiate_plain_and_mountain or rep_plain != rep_mountain
        ):
            if rep_mountain != "":
                frmt_table[
                    "mountain_value"
                ] = f"{rep_mountain} {self.units(mountain_dict['units'])}"

            local_mountain = self.round(
                local, operator=operator, around=frmt_table["around"]
            )
            if local_mountain is not None and local_mountain != rep_mountain:
                frmt_table[
                    "local_mountain_value"
                ] = f"{local_mountain} {self.units(self.infos['mountain']['units'])}"

    @cached_property
    def format_table(self):
        frmt_table = {
            "var_name": "" if "ME" in self.infos else self.phenomenon,
            "definite_var_name": self.definite_var_name,
            "indefinite_var_name": self.indefinite_var_name,
            "feminine": "e" if self.feminine else "",
            "plural": "s" if self.plural else "",
            "around": self.around,
            "accumulated_hours": "",
        }
        if (mountain_altitude := self.infos.get("mountain_altitude")) is not None:
            frmt_table["altitude"] = mountain_altitude

        rep_plain = self._compute_plain_frmt_table(frmt_table)
        self._compute_mountain_frmt_table(frmt_table, rep_plain)
        return frmt_table

    def _compute(self, **_kwargs) -> dict:
        """
        Make computation and returns the reduced data.

        Returns:
            dict: Reduced data
        """
        return self.format_table


class FFRepValueReducer(RepValueReducer):
    feminine: bool = False
    plural: bool = False

    @property
    def phenomenon(self) -> str:
        return self._("vent moyen")

    def round(self, x: Optional[float], **_kwargs) -> Optional[str]:
        """
        Rounds values to the nearest interval of 5.
        Examples:
            Input --> Output
             7.5   -->  5 à 10
             12.5   -->  10 à 15

        Args:
            x (float): Value to round

        Returns:
            [Optional[str]]: Rounded value or None if not possible
        """
        if super().round(x) is None:
            return None
        start = (int(x / 5)) * 5
        stop = start + 5
        return self._(_start_stop_str).format(start=start, stop=stop)


class TemperatureRepValueReducer(RepValueReducer):
    feminine: bool = True
    plural: bool = False

    @property
    def phenomenon(self) -> str:
        return self._("température")

    @property
    def around_word(self) -> str:
        return self._("aux alentours de")

    def round(self, x: Optional[float], **kwargs) -> Optional[str]:
        """
        Rounds down or up as appropriate.
        Examples:
            Input --> Output
             7.5 + <=  -->  7
             7.5 + >= -->  8

        Args:
            x (float): Value to round

        Returns:
            [Optional[str]]: Rounded value or None if not possible
        """
        if x is None:
            return None
        if ComparisonOperator(kwargs["operator"]).is_decreasing_order:
            return str(int(np.floor(x)))
        return str(int(np.ceil(x)))


class TemperatureMinDailyRepValueReducer(TemperatureRepValueReducer):
    @property
    def phenomenon(self) -> str:
        return self._("température minimale quotidienne")


class TemperatureMaxDailyRepValueReducer(TemperatureRepValueReducer):
    @property
    def phenomenon(self) -> str:
        return self._("température maximale quotidienne")


class FFRafRepValueReducer(RepValueReducer):
    feminine: bool = True
    plural: bool = True
    interval_size: ClassVar[int] = 10

    @property
    def phenomenon(self) -> str:
        return self._("rafales")

    @classmethod
    def interval_rep(cls, x: float) -> tuple[int, int]:
        """Return the representative interval of a gust value."""
        start: int = int(round_to_previous_multiple(x, cls.interval_size))
        return start, start + cls.interval_size

    def round(self, x: Optional[float], **kwargs) -> Optional[str]:
        """Rounds values to the nearest interval of 10.

        Examples:
            Input                            --> Output
             7.5, around=None                -->  5 à 10
             7.5, around="comprises entre"   -->  5 et 10

        Args:
            x (float): Value to round

        Returns:
            [Optional[str]]: Rounded value or None if not possible
        """
        if super().round(x) is None:
            return None
        start, stop = self.interval_rep(x)

        if (around := kwargs["around"]) is not None and around.endswith(
            self._("entre")
        ):
            return self._("{start} et {stop}").format(start=start, stop=stop)
        return self._(_start_stop_str).format(start=start, stop=stop)


class AccumulationRepValueReducer(RepValueReducer):
    feminine: bool = False
    bounds: List
    last_bound_size: int
    differentiate_plain_and_mountain: bool = True
    merge_locals: bool = True

    @field_validator("infos", mode="before")
    def check_infos(cls, infos: dict) -> dict:
        """Validate if data has a var_name key with an accumulated variable as value."""
        super().check_infos(infos)

        var_name: str = infos["var_name"]

        accumulation: Optional[int] = split_var_name(var_name)[1]

        if not accumulation:
            raise ValueError(f"No accumulation found for '{var_name}' var_name.")

        return infos

    @property
    def var_name(self) -> str:
        """Get var_name."""
        return self.infos["var_name"]

    @property
    def accumulated_hours(self) -> int:
        """
        Gets the number of hours over which the var_name is accumulated.

        Returns:
            int: Number of hours over which the var_name is accumulated
        """
        return split_var_name(self.var_name)[1]

    @property
    def definite_var_name(self) -> str:
        """Returns the definite var_name name."""
        return self._accumulation_time_suffix(f"{self.def_article} {self.phenomenon}")

    @property
    def indefinite_var_name(self) -> str:
        """Returns the indefinite var_name name."""
        return self._accumulation_time_suffix(f"{self.indef_article} {self.phenomenon}")

    @property
    def accumulated_phenomenon(self) -> str:
        """Returns the accumulated var_name name."""
        return self._accumulation_time_suffix(self.phenomenon)

    def _accumulation_time_suffix(self, var: str) -> str:
        return self._("{var} sur {accumulated_hours}h").format(
            var=var, accumulated_hours=self.accumulated_hours
        )

    @cached_property
    def format_table(self) -> dict[str, str]:
        frmt_table = super().format_table | {
            "var_name": self.accumulated_phenomenon,
            "accumulated_hours": self._("en {accumulated_hours}h").format(
                accumulated_hours=self.accumulated_hours
            ),
        }
        if (
            self.merge_locals is False
            or "plain" not in self.infos
            or "mountain" not in self.infos
        ):
            return frmt_table

        # Merge plain and mountain local values if it is possible
        p_value = frmt_table.get("plain_value")
        m_value = frmt_table.get("mountain_value")
        lp_value = frmt_table.get("local_plain_value")
        lm_value = frmt_table.get("local_mountain_value")

        if m_value is not None and m_value == p_value:
            frmt_table["equals_plain_mountain"] = True
            frmt_table.pop("mountain_value", None)
            frmt_table.pop("local_mountain_value", None)
            if lp_value is None and lm_value is not None:
                frmt_table["plain_value"] += (
                    self._(" (localement {lm_value} sur les hauteurs)")
                ).format(lm_value=lm_value)

        elif (
            p_value is None
            and m_value is None
            and lp_value is not None
            and lp_value == lm_value
        ):
            frmt_table["equals_plain_mountain"] = True
            frmt_table.pop("mountain_value", None)
            frmt_table.pop("local_mountain_value", None)

        return frmt_table

    def _value_as_string(self, x: float) -> str:
        for low_bound, up_bound in self.bounds:
            if x < up_bound:
                start, stop = low_bound, up_bound
                break
        else:
            start = int(x / self.last_bound_size) * self.last_bound_size
            stop = start + self.last_bound_size
        return self._(_start_stop_str).format(start=start, stop=stop)

    def round(self, x: Optional[float], **_kwargs) -> Optional[str]:
        if x is not None:
            if abs(x) > 1e-6:
                return self._value_as_string(x)
            return ""
        return None

    @property
    def can_merge_values(self) -> bool:
        return self.format_table.get("equals_plain_mountain", False)


class SnowRepValueReducer(AccumulationRepValueReducer):
    # List contents of the tuples with the lower limits and the amplitude of the
    # interval
    bounds: List = [(0, 1), (1, 3), (3, 5), (5, 7), (7, 10), (10, 15), (15, 20)]
    last_bound_size: int = 10

    @property
    def phenomenon(self) -> str:
        return self._("potentiel de neige")


class FallingWaterRepValueReducer(AccumulationRepValueReducer):
    # List contents of the tuples with the lower limits and the amplitude of the
    # interval
    bounds: List = [
        (3, 7),
        (7, 10),
        (10, 15),
        (15, 20),
        (20, 25),
        (25, 30),
        (30, 40),
        (40, 50),
        (50, 60),
        (60, 80),
        (80, 100),
    ]
    last_bound_size: int = 50

    def round(self, x: Optional[float], **kwargs) -> Optional[str]:
        """
        Rounds the value to the nearest interval.

        Examples:
            Input --> Output
             42   -->  40 to 45
             39   -->  35 to 40
        """
        rounding_val = super().round(x, **kwargs)
        if rounding_val not in [None, ""] and x < 3:
            return self._("au maximum") + " 3"
        return rounding_val


class PrecipitationRepValueReducer(FallingWaterRepValueReducer):
    @property
    def phenomenon(self) -> str:
        return self._("cumul de précipitation")


class RainRepValueReducer(FallingWaterRepValueReducer):
    @property
    def phenomenon(self) -> str:
        return self._("cumul de pluie")


class LpnRepValueReducer(RepValueReducer):
    def _compute(self, **_kwargs) -> dict:
        if (
            "LPN__SOL" not in self.parent.params
            or "WWMF__SOL" not in self.parent.params
        ):
            return {}

        geo_da = self.parent.geo(self.geo_id)
        if (
            snow_geo_da := geo_da.where(
                Wwmf.is_snow(self.parent.params["WWMF__SOL"].compute())
            )
        ).count() > 0:
            geo_da = snow_geo_da
        else:
            geo_da = self.parent.levels_of_risk(
                self.parent.final_risk_max_level(self.geo_id)
            )[0].spatial_risk_da.sel(id=self.geo_id)
            geo_da = geo_da.where(geo_da > 0)

        lpn_da = self.parent.params["LPN__SOL"].compute() * geo_da
        lpn = Lpn(da=lpn_da, period_describer=self.parent.period_describer)
        if lpn.extremums_da is None:
            return {}

        return {
            "key": lpn.template_key,
            "lpn": lpn.extremums,
            "temp": lpn.temporalities,
        }


class AltitudeRepValueReducer(RepValueReducer):
    """
    This class will represent the sentences "Surveillance client au-dessus/en-dessous de
    xxx m : ...

    """

    @field_validator("infos", mode="before")
    def check_infos(cls, infos: dict) -> dict:
        """Return simply data.

        This validator override RepValueReducer.check_infos which verifies that data
        has a key called var_name.
        """
        return infos

    @staticmethod
    def get_reducer(var_name: str) -> Optional[Callable]:
        prefix = split_var_name(var_name, full_var_name=False)[0]
        reducers = {
            "FF": FFRepValueReducer,
            "RAF": FFRafRepValueReducer,
            "T": TemperatureRepValueReducer,
            "TMAXQ": TemperatureMaxDailyRepValueReducer,
            "TMINQ": TemperatureMinDailyRepValueReducer,
            "PRECIP": PrecipitationRepValueReducer,
            "EAU": RainRepValueReducer,
            "NEIPOT": SnowRepValueReducer,
            "LPN": LpnRepValueReducer,
        }
        try:
            return reducers[prefix]
        except KeyError:
            return None

    def _compute_loop_new_val(self, frmt_table, key):
        new_val = frmt_table.get(key, "")
        if new_val:
            new_val = self._("de {new_val}").format(new_val=new_val)
        if local_val := frmt_table.get(f"local_{key}"):
            local_val = self._("localement de {local_val}").format(local_val=local_val)
            new_val = f"{new_val} ({local_val})" if new_val != "" else local_val
        return new_val

    def _compute_loop(self, values, var_name, infos, reducer_class):
        reducer: RepValueReducer = reducer_class(
            infos=infos | {"var_name": var_name},
            differentiate_plain_and_mountain=True,
            merge_locals=False,
            parent=self.parent,
            geo_id=self.geo_id,
        )

        is_acc = isinstance(reducer, AccumulationRepValueReducer)
        accum = f"{reducer._accumulation_time_suffix('')} " if is_acc else ""
        frmt_table = reducer.compute()

        for key, values_list in values.items():
            if new_val := self._compute_loop_new_val(frmt_table, key):
                values_list.append(accum + new_val)

        if is_acc:
            for zone in {"plain", "mountain"}.intersection(reducer.infos.keys()):
                key: str = f"{zone}_value"

                if all((key not in frmt_table, f"local_{key}" not in frmt_table)):
                    values[key].append(accum + self._("non significatif"))

    def _compute(self, **_kwargs) -> dict:
        """
        Make computation and returns the reduced data.

        Returns:
            dict: Reduced data
        """

        var_name = next(iter(self.infos))
        reducer_class = self.get_reducer(var_name)
        if reducer_class is None:
            return {}

        values: dict[str, list] = {"plain_value": [], "mountain_value": []}
        for var_name, infos in self.infos.items():
            self._compute_loop(values, var_name, infos, reducer_class)

        reducer = reducer_class(
            infos={"var_name": var_name} | next(iter(self.infos.values())),
            parent=self.parent,
            geo_id=self.geo_id,
        )
        frmt_table = reducer.compute()
        frmt_table = {
            "altitude": frmt_table.get("altitude", "xxx"),
            "var_name": reducer.phenomenon,
            "feminine": frmt_table["feminine"],
            "plural": frmt_table["plural"],
        }
        for key, val in values.items():
            if val:
                frmt_table[key] = concatenate_string(
                    val, last_delimiter=f" {self._('et')} "
                )

        return frmt_table


class RepValueBuilder(BaseBuilder):
    """
    This class enable to speak about representative values
    """

    module_name: str = "risk"
    reducer: Optional[RepValueReducer] = None
    reducer_class: type = RepValueReducer
    parent: Optional[RiskComponentComposite] = None

    @property
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_generic"

    @property
    def template_key(self) -> str:
        """
        Get the template key.

        Returns:
            str | np.ndarray: The template key.
        """
        key_parts = []

        if "plain_value" in self.reduction:
            if "local_plain_value" in self.reduction:
                key_parts.append("local")
            key_parts.append("plain")
        if "mountain_value" in self.reduction:
            if "local_mountain_value" in self.reduction:
                key_parts.append("local")
            key_parts.append("mountain")
        if key_parts and "ME" in self.infos:
            key_parts = ["ME"] + key_parts

        return "_".join(key_parts)

    @classmethod
    def get_builder(cls, infos: dict, base_geo: BaseGeo) -> Optional[RepValueBuilder]:
        """
        Returns a RepValueBuilder object for the given data dictionary.

        Args:
            infos: A dictionary of data, where the keys are the variable names and the
                values are the variable values.

        Returns:
            A RepValueBuilder object for the given data dictionary, or None if no
                builder is available.
        """
        prefix = split_var_name(infos["var_name"], full_var_name=False)[0]
        builders = {
            "FF": FFRepValueBuilder,
            "RAF": FFRafRepValueBuilder,
            "T": TemperatureRepValueBuilder,
            "TMAXQ": TemperatureMaxDailyRepValueBuilder,
            "TMINQ": TemperatureMinDailyRepValueBuilder,
            "PRECIP": PrecipitationRepValueBuilder,
            "EAU": RainRepValueBuilder,
            "NEIPOT": SnowRepValueBuilder,
            "LPN": LpnRepValueBuilder,
        }
        try:
            return builders[prefix](
                infos=infos, parent=base_geo.parent, geo_id=base_geo.geo_id
            )
        except KeyError:
            return None

    def pre_process(self):
        """Make a pre-process operation on the text."""
        super().pre_process()
        rep_value = self.reduction.get("mountain_value") or self.reduction.get(
            "plain_value", ""
        )

        if rep_value.startswith("au"):
            self.reduction["around"] = "d'"
            self.text = self.text.replace("{around} ", "{around}")

    @staticmethod
    def _compute_all_altitude(base_geo: BaseGeo, all_infos: dict) -> str:
        altitude_data = defaultdict(dict)
        for key, infos in all_infos.items():
            altitude_data[split_var_name(key)[0]][key] = infos

        text = ""
        for param, infos in altitude_data.items():
            if param != "LPN__SOL":
                builder_class = AltitudeRepValueBuilder
            else:
                builder_class = LpnRepValueBuilder
                infos |= {"var_name": param}

            if builder_text := builder_class(
                infos=infos, parent=base_geo.parent, geo_id=base_geo.geo_id
            ).compute():
                text += f"\n{builder_text}"

        return text.rstrip()

    @staticmethod
    def _compute_all_no_altitude(base_geo: BaseGeo, all_infos: dict) -> str:
        text = ""
        for key, infos in all_infos.items():
            builder_class = RepValueBuilder.get_builder(
                infos | {"var_name": key}, base_geo
            )
            if isinstance(builder_class, LpnRepValueBuilder):
                text += "\n"
            if builder_class is not None:
                text += builder_class.compute() + " "
        return text.rstrip()

    @staticmethod
    def compute_all(base_geo: BaseGeo, all_data: dict) -> str:
        """
        Calculates a textual representation of all the variables in the given data
        dictionary.

        Args:
            data: A dictionary of data, where the keys are the variable names and the
                values are the variable values.

        Returns:
            A textual representation of all the variables in the data dictionary.
        """
        if not all_data:
            return ""

        # If monitoring with altitude, generate a specific sentence
        if "mountain_altitude" in next(iter(all_data.values())):
            return RepValueBuilder._compute_all_altitude(base_geo, all_data)

        # Otherwise, generate a sentence for each variable
        return RepValueBuilder._compute_all_no_altitude(base_geo, all_data)


class FFRepValueBuilder(RepValueBuilder):
    reducer_class: type = FFRepValueReducer


class TemperatureRepValueBuilder(RepValueBuilder):
    reducer_class: type = TemperatureRepValueReducer


class TemperatureMaxDailyRepValueBuilder(RepValueBuilder):
    reducer_class: type = TemperatureMaxDailyRepValueReducer


class TemperatureMinDailyRepValueBuilder(RepValueBuilder):
    reducer_class: type = TemperatureMinDailyRepValueReducer


class FFRafRepValueBuilder(RepValueBuilder):
    reducer_class: type = FFRafRepValueReducer

    @property
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_raf"


class AccumulationRepValueBuilder(RepValueBuilder):
    reducer_class: type = AccumulationRepValueReducer

    @property
    def template_key(self) -> str:
        key_parts = []

        keys = []
        if "plain" in self.infos:
            keys.append("plain")
        if "mountain" in self.infos and not self.reducer.can_merge_values:
            keys.append("mountain")

        for zone in keys:
            if f"{zone}_value" not in self.reduction:
                key_parts.append(f"no_acc_{zone}")

                if f"local_{zone}_value" in self.reduction:
                    key_parts.append(f"local_{zone}")
            else:
                if f"local_{zone}_value" in self.reduction:
                    key_parts.append("local")
                key_parts.append(zone)

        if key_parts and "ME" in self.infos:
            key_parts = ["ME"] + key_parts

        return "_".join(key_parts)


class SnowRepValueBuilder(AccumulationRepValueBuilder):
    reducer_class: type = SnowRepValueReducer


class PrecipitationRepValueBuilder(AccumulationRepValueBuilder):
    reducer_class: type = PrecipitationRepValueReducer


class RainRepValueBuilder(AccumulationRepValueBuilder):
    reducer_class: type = RainRepValueReducer


class LpnRepValueBuilder(RepValueBuilder):
    reducer_class: type = LpnRepValueReducer

    @property
    def template_name(self) -> str | List[str]:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_lpn"

    @cached_property
    def template_key(self) -> Optional[str | List | np.ndarray]:
        """
        Get the template key.

        Returns:
            str | np.ndarray: The template key.
        """
        return self.reduction.get("key")


class AltitudeRepValueBuilder(RepValueBuilder):
    reducer_class: type = AltitudeRepValueReducer

    @property
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_altitude"

    def _compute(self, **_kwargs) -> str:
        if not self.reduction:
            return ""
        return super()._compute()
