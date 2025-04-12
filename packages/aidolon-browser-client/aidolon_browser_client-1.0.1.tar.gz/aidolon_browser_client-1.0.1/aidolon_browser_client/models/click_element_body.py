from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.click_element_body_wait import ClickElementBodyWait
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="ClickElementBody")



@_attrs_define
class ClickElementBody:
    """ 
        Attributes:
            selector (str): CSS selector for the element to click
            wait (Union[Unset, ClickElementBodyWait]): Wait strategy after click:
                * auto - automatically determine best wait strategy
                * navigation - wait for page navigation
                * network - wait for network to be idle
                * none - don't wait
                 Default: ClickElementBodyWait.AUTO.
     """

    selector: str
    wait: Union[Unset, ClickElementBodyWait] = ClickElementBodyWait.AUTO
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        selector = self.selector

        wait: Union[Unset, str] = UNSET
        if not isinstance(self.wait, Unset):
            wait = self.wait.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "selector": selector,
        })
        if wait is not UNSET:
            field_dict["wait"] = wait

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        selector = d.pop("selector")

        _wait = d.pop("wait", UNSET)
        wait: Union[Unset, ClickElementBodyWait]
        if isinstance(_wait,  Unset):
            wait = UNSET
        else:
            wait = ClickElementBodyWait(_wait)




        click_element_body = cls(
            selector=selector,
            wait=wait,
        )


        click_element_body.additional_properties = d
        return click_element_body

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
