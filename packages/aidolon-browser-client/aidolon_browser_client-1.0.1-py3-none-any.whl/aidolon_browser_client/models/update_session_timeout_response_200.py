from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="UpdateSessionTimeoutResponse200")



@_attrs_define
class UpdateSessionTimeoutResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            session_id (Union[Unset, UUID]):
            timeout (Union[Unset, int]): The new timeout value in seconds
     """

    success: Union[Unset, bool] = UNSET
    session_id: Union[Unset, UUID] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        success = self.success

        session_id: Union[Unset, str] = UNSET
        if not isinstance(self.session_id, Unset):
            session_id = str(self.session_id)

        timeout = self.timeout


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

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




        timeout = d.pop("timeout", UNSET)

        update_session_timeout_response_200 = cls(
            success=success,
            session_id=session_id,
            timeout=timeout,
        )


        update_session_timeout_response_200.additional_properties = d
        return update_session_timeout_response_200

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
