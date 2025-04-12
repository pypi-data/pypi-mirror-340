from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="TypeTextBody")



@_attrs_define
class TypeTextBody:
    """ 
        Attributes:
            selector (str): CSS selector for the element to type into
            text (str): Text to type
            delay (Union[Unset, float]): Delay between keystrokes in seconds Default: 0.1.
     """

    selector: str
    text: str
    delay: Union[Unset, float] = 0.1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        selector = self.selector

        text = self.text

        delay = self.delay


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "selector": selector,
            "text": text,
        })
        if delay is not UNSET:
            field_dict["delay"] = delay

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        selector = d.pop("selector")

        text = d.pop("text")

        delay = d.pop("delay", UNSET)

        type_text_body = cls(
            selector=selector,
            text=text,
            delay=delay,
        )


        type_text_body.additional_properties = d
        return type_text_body

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
