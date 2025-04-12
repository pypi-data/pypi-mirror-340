from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.press_key_body_wait import PressKeyBodyWait
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="PressKeyBody")



@_attrs_define
class PressKeyBody:
    """ 
        Attributes:
            selector (str): CSS selector for the element
            key (str): Key to press (e.g., "Enter", "Tab", "Escape", "ArrowUp", etc.)
            wait (Union[Unset, PressKeyBodyWait]): Wait strategy after key press:
                * auto - automatically determine best wait strategy
                * navigation - wait for page navigation
                * network - wait for network to be idle
                * none - don't wait
                 Default: PressKeyBodyWait.AUTO.
     """

    selector: str
    key: str
    wait: Union[Unset, PressKeyBodyWait] = PressKeyBodyWait.AUTO
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        selector = self.selector

        key = self.key

        wait: Union[Unset, str] = UNSET
        if not isinstance(self.wait, Unset):
            wait = self.wait.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "selector": selector,
            "key": key,
        })
        if wait is not UNSET:
            field_dict["wait"] = wait

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        selector = d.pop("selector")

        key = d.pop("key")

        _wait = d.pop("wait", UNSET)
        wait: Union[Unset, PressKeyBodyWait]
        if isinstance(_wait,  Unset):
            wait = UNSET
        else:
            wait = PressKeyBodyWait(_wait)




        press_key_body = cls(
            selector=selector,
            key=key,
            wait=wait,
        )


        press_key_body.additional_properties = d
        return press_key_body

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
