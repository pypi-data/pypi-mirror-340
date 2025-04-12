from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.browser_session_status import BrowserSessionStatus
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, Union
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.browser_session_live_session_type_0 import BrowserSessionLiveSessionType0





T = TypeVar("T", bound="BrowserSession")



@_attrs_define
class BrowserSession:
    """ 
        Attributes:
            session_id (UUID): Unique identifier for the browser session
            status (BrowserSessionStatus): Current status of the session
            created_at (datetime.datetime): When the session was created
            embed_url (Union[Unset, str]): URL to embed the browser session in an iframe
            updated_at (Union[Unset, datetime.datetime]): When the session was last updated
            last_active_at (Union[Unset, datetime.datetime]): When the session was last active
            closed_at (Union[None, Unset, datetime.datetime]): When the session was closed, if applicable
            live_session (Union['BrowserSessionLiveSessionType0', None, Unset]): Information about the live browser session
     """

    session_id: UUID
    status: BrowserSessionStatus
    created_at: datetime.datetime
    embed_url: Union[Unset, str] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    last_active_at: Union[Unset, datetime.datetime] = UNSET
    closed_at: Union[None, Unset, datetime.datetime] = UNSET
    live_session: Union['BrowserSessionLiveSessionType0', None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.browser_session_live_session_type_0 import BrowserSessionLiveSessionType0
        session_id = str(self.session_id)

        status = self.status.value

        created_at = self.created_at.isoformat()

        embed_url = self.embed_url

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        last_active_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_active_at, Unset):
            last_active_at = self.last_active_at.isoformat()

        closed_at: Union[None, Unset, str]
        if isinstance(self.closed_at, Unset):
            closed_at = UNSET
        elif isinstance(self.closed_at, datetime.datetime):
            closed_at = self.closed_at.isoformat()
        else:
            closed_at = self.closed_at

        live_session: Union[None, Unset, dict[str, Any]]
        if isinstance(self.live_session, Unset):
            live_session = UNSET
        elif isinstance(self.live_session, BrowserSessionLiveSessionType0):
            live_session = self.live_session.to_dict()
        else:
            live_session = self.live_session


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "session_id": session_id,
            "status": status,
            "created_at": created_at,
        })
        if embed_url is not UNSET:
            field_dict["embed_url"] = embed_url
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if last_active_at is not UNSET:
            field_dict["last_active_at"] = last_active_at
        if closed_at is not UNSET:
            field_dict["closed_at"] = closed_at
        if live_session is not UNSET:
            field_dict["live_session"] = live_session

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.browser_session_live_session_type_0 import BrowserSessionLiveSessionType0
        d = dict(src_dict)
        session_id = UUID(d.pop("session_id"))




        status = BrowserSessionStatus(d.pop("status"))




        created_at = isoparse(d.pop("created_at"))




        embed_url = d.pop("embed_url", UNSET)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)




        _last_active_at = d.pop("last_active_at", UNSET)
        last_active_at: Union[Unset, datetime.datetime]
        if isinstance(_last_active_at,  Unset):
            last_active_at = UNSET
        else:
            last_active_at = isoparse(_last_active_at)




        def _parse_closed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                closed_at_type_0 = isoparse(data)



                return closed_at_type_0
            except: # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        closed_at = _parse_closed_at(d.pop("closed_at", UNSET))


        def _parse_live_session(data: object) -> Union['BrowserSessionLiveSessionType0', None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                live_session_type_0 = BrowserSessionLiveSessionType0.from_dict(data)



                return live_session_type_0
            except: # noqa: E722
                pass
            return cast(Union['BrowserSessionLiveSessionType0', None, Unset], data)

        live_session = _parse_live_session(d.pop("live_session", UNSET))


        browser_session = cls(
            session_id=session_id,
            status=status,
            created_at=created_at,
            embed_url=embed_url,
            updated_at=updated_at,
            last_active_at=last_active_at,
            closed_at=closed_at,
            live_session=live_session,
        )


        browser_session.additional_properties = d
        return browser_session

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
