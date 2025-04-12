from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.take_screenshot_response_200_data import TakeScreenshotResponse200Data





T = TypeVar("T", bound="TakeScreenshotResponse200")



@_attrs_define
class TakeScreenshotResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            action (Union[Unset, str]):  Example: screenshot.
            data (Union[Unset, TakeScreenshotResponse200Data]):
     """

    success: Union[Unset, bool] = UNSET
    action: Union[Unset, str] = UNSET
    data: Union[Unset, 'TakeScreenshotResponse200Data'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.take_screenshot_response_200_data import TakeScreenshotResponse200Data
        success = self.success

        action = self.action

        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if action is not UNSET:
            field_dict["action"] = action
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.take_screenshot_response_200_data import TakeScreenshotResponse200Data
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        action = d.pop("action", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, TakeScreenshotResponse200Data]
        if isinstance(_data,  Unset):
            data = UNSET
        else:
            data = TakeScreenshotResponse200Data.from_dict(_data)




        take_screenshot_response_200 = cls(
            success=success,
            action=action,
            data=data,
        )


        take_screenshot_response_200.additional_properties = d
        return take_screenshot_response_200

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
