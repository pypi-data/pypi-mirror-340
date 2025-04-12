from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="CloseAllBrowserSessionsResponse200")



@_attrs_define
class CloseAllBrowserSessionsResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            closed_count (Union[Unset, int]): Number of sessions that were closed
            message (Union[Unset, str]): Success message
     """

    success: Union[Unset, bool] = UNSET
    closed_count: Union[Unset, int] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        success = self.success

        closed_count = self.closed_count

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if closed_count is not UNSET:
            field_dict["closed_count"] = closed_count
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        closed_count = d.pop("closed_count", UNSET)

        message = d.pop("message", UNSET)

        close_all_browser_sessions_response_200 = cls(
            success=success,
            closed_count=closed_count,
            message=message,
        )


        close_all_browser_sessions_response_200.additional_properties = d
        return close_all_browser_sessions_response_200

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
