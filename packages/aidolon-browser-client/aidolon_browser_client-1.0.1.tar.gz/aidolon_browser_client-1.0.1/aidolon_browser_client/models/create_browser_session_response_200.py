from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, Union
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.create_browser_session_response_200_live_session_type_0 import CreateBrowserSessionResponse200LiveSessionType0





T = TypeVar("T", bound="CreateBrowserSessionResponse200")



@_attrs_define
class CreateBrowserSessionResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            session_id (Union[Unset, UUID]): Unique identifier for the session
            embed_url (Union[Unset, str]): URL to embed the browser session in an iframe
            status (Union[Unset, str]): Current status of the session Example: active.
            created_at (Union[Unset, datetime.datetime]): When the session was created
            live_session (Union['CreateBrowserSessionResponse200LiveSessionType0', None, Unset]): Information about the live
                browser session
     """

    success: Union[Unset, bool] = UNSET
    session_id: Union[Unset, UUID] = UNSET
    embed_url: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    live_session: Union['CreateBrowserSessionResponse200LiveSessionType0', None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.create_browser_session_response_200_live_session_type_0 import CreateBrowserSessionResponse200LiveSessionType0
        success = self.success

        session_id: Union[Unset, str] = UNSET
        if not isinstance(self.session_id, Unset):
            session_id = str(self.session_id)

        embed_url = self.embed_url

        status = self.status

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        live_session: Union[None, Unset, dict[str, Any]]
        if isinstance(self.live_session, Unset):
            live_session = UNSET
        elif isinstance(self.live_session, CreateBrowserSessionResponse200LiveSessionType0):
            live_session = self.live_session.to_dict()
        else:
            live_session = self.live_session


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if embed_url is not UNSET:
            field_dict["embed_url"] = embed_url
        if status is not UNSET:
            field_dict["status"] = status
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if live_session is not UNSET:
            field_dict["live_session"] = live_session

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_browser_session_response_200_live_session_type_0 import CreateBrowserSessionResponse200LiveSessionType0
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        _session_id = d.pop("session_id", UNSET)
        session_id: Union[Unset, UUID]
        if isinstance(_session_id,  Unset):
            session_id = UNSET
        else:
            session_id = UUID(_session_id)




        embed_url = d.pop("embed_url", UNSET)

        status = d.pop("status", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)




        def _parse_live_session(data: object) -> Union['CreateBrowserSessionResponse200LiveSessionType0', None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                live_session_type_0 = CreateBrowserSessionResponse200LiveSessionType0.from_dict(data)



                return live_session_type_0
            except: # noqa: E722
                pass
            return cast(Union['CreateBrowserSessionResponse200LiveSessionType0', None, Unset], data)

        live_session = _parse_live_session(d.pop("live_session", UNSET))


        create_browser_session_response_200 = cls(
            success=success,
            session_id=session_id,
            embed_url=embed_url,
            status=status,
            created_at=created_at,
            live_session=live_session,
        )


        create_browser_session_response_200.additional_properties = d
        return create_browser_session_response_200

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
