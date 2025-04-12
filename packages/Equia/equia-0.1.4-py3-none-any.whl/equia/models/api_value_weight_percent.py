from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiValueWeightPercent")


@attr.s(auto_attribs=True)
class ApiValueWeightPercent:
    """Weight fraction information"""

    value: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        api_value_weight_percent = cls(
            value=value,
        )

        return api_value_weight_percent
