from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DragAndDropBody")



@_attrs_define
class DragAndDropBody:
    """ 
        Attributes:
            source_selector (str): CSS selector for the source element (to drag)
            target_selector (str): CSS selector for the target element (drop location)
     """

    source_selector: str
    target_selector: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        source_selector = self.source_selector

        target_selector = self.target_selector


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "source_selector": source_selector,
            "target_selector": target_selector,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_selector = d.pop("source_selector")

        target_selector = d.pop("target_selector")

        drag_and_drop_body = cls(
            source_selector=source_selector,
            target_selector=target_selector,
        )


        drag_and_drop_body.additional_properties = d
        return drag_and_drop_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
