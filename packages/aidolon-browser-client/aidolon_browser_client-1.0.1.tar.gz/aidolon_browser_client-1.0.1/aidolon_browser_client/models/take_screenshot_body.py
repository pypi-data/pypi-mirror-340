from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="TakeScreenshotBody")



@_attrs_define
class TakeScreenshotBody:
    """ 
        Attributes:
            full_page (Union[Unset, bool]): Whether to capture the full page or just the viewport Default: False.
            delay (Union[Unset, float]): Delay in seconds before taking the screenshot
     """

    full_page: Union[Unset, bool] = False
    delay: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        full_page = self.full_page

        delay = self.delay


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if full_page is not UNSET:
            field_dict["full_page"] = full_page
        if delay is not UNSET:
            field_dict["delay"] = delay

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_page = d.pop("full_page", UNSET)

        delay = d.pop("delay", UNSET)

        take_screenshot_body = cls(
            full_page=full_page,
            delay=delay,
        )


        take_screenshot_body.additional_properties = d
        return take_screenshot_body

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
