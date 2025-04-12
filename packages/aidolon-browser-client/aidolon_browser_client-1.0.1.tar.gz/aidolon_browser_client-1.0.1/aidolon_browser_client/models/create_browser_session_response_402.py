from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.create_browser_session_response_402_details import CreateBrowserSessionResponse402Details





T = TypeVar("T", bound="CreateBrowserSessionResponse402")



@_attrs_define
class CreateBrowserSessionResponse402:
    """ 
        Attributes:
            success (bool):
            error (str): Human-readable error message
            error_code (str): Machine-readable error code
            details (Union[Unset, CreateBrowserSessionResponse402Details]):
     """

    success: bool
    error: str
    error_code: str
    details: Union[Unset, 'CreateBrowserSessionResponse402Details'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.create_browser_session_response_402_details import CreateBrowserSessionResponse402Details
        success = self.success

        error = self.error

        error_code = self.error_code

        details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "success": success,
            "error": error,
            "error_code": error_code,
        })
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_browser_session_response_402_details import CreateBrowserSessionResponse402Details
        d = dict(src_dict)
        success = d.pop("success")

        error = d.pop("error")

        error_code = d.pop("error_code")

        _details = d.pop("details", UNSET)
        details: Union[Unset, CreateBrowserSessionResponse402Details]
        if isinstance(_details,  Unset):
            details = UNSET
        else:
            details = CreateBrowserSessionResponse402Details.from_dict(_details)




        create_browser_session_response_402 = cls(
            success=success,
            error=error,
            error_code=error_code,
            details=details,
        )


        create_browser_session_response_402.additional_properties = d
        return create_browser_session_response_402

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
