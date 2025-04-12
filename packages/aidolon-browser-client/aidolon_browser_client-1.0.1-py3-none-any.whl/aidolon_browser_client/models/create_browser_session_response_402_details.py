from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="CreateBrowserSessionResponse402Details")



@_attrs_define
class CreateBrowserSessionResponse402Details:
    """ 
        Attributes:
            required_credits (Union[Unset, float]): Credits required for the operation
            current_balance (Union[Unset, float]): User's current credit balance
            missing_credits (Union[Unset, float]): Additional credits needed
     """

    required_credits: Union[Unset, float] = UNSET
    current_balance: Union[Unset, float] = UNSET
    missing_credits: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        required_credits = self.required_credits

        current_balance = self.current_balance

        missing_credits = self.missing_credits


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if required_credits is not UNSET:
            field_dict["required_credits"] = required_credits
        if current_balance is not UNSET:
            field_dict["current_balance"] = current_balance
        if missing_credits is not UNSET:
            field_dict["missing_credits"] = missing_credits

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        required_credits = d.pop("required_credits", UNSET)

        current_balance = d.pop("current_balance", UNSET)

        missing_credits = d.pop("missing_credits", UNSET)

        create_browser_session_response_402_details = cls(
            required_credits=required_credits,
            current_balance=current_balance,
            missing_credits=missing_credits,
        )


        create_browser_session_response_402_details.additional_properties = d
        return create_browser_session_response_402_details

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
