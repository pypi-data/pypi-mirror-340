from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="DragAndDropResponse200")



@_attrs_define
class DragAndDropResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            action (Union[Unset, str]):  Example: drag_and_drop.
            source_selector (Union[Unset, str]): CSS selector for the source element
            target_selector (Union[Unset, str]): CSS selector for the target element
     """

    success: Union[Unset, bool] = UNSET
    action: Union[Unset, str] = UNSET
    source_selector: Union[Unset, str] = UNSET
    target_selector: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        success = self.success

        action = self.action

        source_selector = self.source_selector

        target_selector = self.target_selector


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if action is not UNSET:
            field_dict["action"] = action
        if source_selector is not UNSET:
            field_dict["source_selector"] = source_selector
        if target_selector is not UNSET:
            field_dict["target_selector"] = target_selector

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        action = d.pop("action", UNSET)

        source_selector = d.pop("source_selector", UNSET)

        target_selector = d.pop("target_selector", UNSET)

        drag_and_drop_response_200 = cls(
            success=success,
            action=action,
            source_selector=source_selector,
            target_selector=target_selector,
        )


        drag_and_drop_response_200.additional_properties = d
        return drag_and_drop_response_200

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
