from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="CloseBrowserSessionResponse200")



@_attrs_define
class CloseBrowserSessionResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            session_id (Union[Unset, UUID]):
            status (Union[Unset, str]):  Example: closed.
     """

    success: Union[Unset, bool] = UNSET
    session_id: Union[Unset, UUID] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        success = self.success

        session_id: Union[Unset, str] = UNSET
        if not isinstance(self.session_id, Unset):
            session_id = str(self.session_id)

        status = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        _session_id = d.pop("session_id", UNSET)
        session_id: Union[Unset, UUID]
        if isinstance(_session_id,  Unset):
            session_id = UNSET
        else:
            session_id = UUID(_session_id)




        status = d.pop("status", UNSET)

        close_browser_session_response_200 = cls(
            success=success,
            session_id=session_id,
            status=status,
        )


        close_browser_session_response_200.additional_properties = d
        return close_browser_session_response_200

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
