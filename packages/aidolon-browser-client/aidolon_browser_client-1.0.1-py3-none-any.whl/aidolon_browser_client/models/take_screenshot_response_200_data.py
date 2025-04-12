from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="TakeScreenshotResponse200Data")



@_attrs_define
class TakeScreenshotResponse200Data:
    """ 
        Attributes:
            url (Union[Unset, str]): The URL of the page that was captured
            screenshot_url (Union[Unset, str]): URL to access the screenshot image
     """

    url: Union[Unset, str] = UNSET
    screenshot_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        url = self.url

        screenshot_url = self.screenshot_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if url is not UNSET:
            field_dict["url"] = url
        if screenshot_url is not UNSET:
            field_dict["screenshot_url"] = screenshot_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        screenshot_url = d.pop("screenshot_url", UNSET)

        take_screenshot_response_200_data = cls(
            url=url,
            screenshot_url=screenshot_url,
        )


        take_screenshot_response_200_data.additional_properties = d
        return take_screenshot_response_200_data

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
