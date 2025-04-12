from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.browser_session import BrowserSession





T = TypeVar("T", bound="ListBrowserSessionsResponse200")



@_attrs_define
class ListBrowserSessionsResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            sessions (Union[Unset, list['BrowserSession']]):
            count (Union[Unset, int]): Number of sessions returned
            filtered_by (Union[Unset, str]): The status filter applied, or "all" if no filter
     """

    success: Union[Unset, bool] = UNSET
    sessions: Union[Unset, list['BrowserSession']] = UNSET
    count: Union[Unset, int] = UNSET
    filtered_by: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.browser_session import BrowserSession
        success = self.success

        sessions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = []
            for sessions_item_data in self.sessions:
                sessions_item = sessions_item_data.to_dict()
                sessions.append(sessions_item)



        count = self.count

        filtered_by = self.filtered_by


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if count is not UNSET:
            field_dict["count"] = count
        if filtered_by is not UNSET:
            field_dict["filtered_by"] = filtered_by

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.browser_session import BrowserSession
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        sessions = []
        _sessions = d.pop("sessions", UNSET)
        for sessions_item_data in (_sessions or []):
            sessions_item = BrowserSession.from_dict(sessions_item_data)



            sessions.append(sessions_item)


        count = d.pop("count", UNSET)

        filtered_by = d.pop("filtered_by", UNSET)

        list_browser_sessions_response_200 = cls(
            success=success,
            sessions=sessions,
            count=count,
            filtered_by=filtered_by,
        )


        list_browser_sessions_response_200.additional_properties = d
        return list_browser_sessions_response_200

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
