from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_session_status_response_200_status import GetSessionStatusResponse200Status
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, Union
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.get_session_status_response_200_live_session_type_0 import GetSessionStatusResponse200LiveSessionType0





T = TypeVar("T", bound="GetSessionStatusResponse200")



@_attrs_define
class GetSessionStatusResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            session_id (Union[Unset, UUID]):
            status (Union[Unset, GetSessionStatusResponse200Status]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
            last_active_at (Union[Unset, datetime.datetime]):
            closed_at (Union[Unset, datetime.datetime]):
            live_session (Union['GetSessionStatusResponse200LiveSessionType0', None, Unset]): Information about the live
                browser session (only for active sessions)
     """

    success: Union[Unset, bool] = UNSET
    session_id: Union[Unset, UUID] = UNSET
    status: Union[Unset, GetSessionStatusResponse200Status] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    last_active_at: Union[Unset, datetime.datetime] = UNSET
    closed_at: Union[Unset, datetime.datetime] = UNSET
    live_session: Union['GetSessionStatusResponse200LiveSessionType0', None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.get_session_status_response_200_live_session_type_0 import GetSessionStatusResponse200LiveSessionType0
        success = self.success

        session_id: Union[Unset, str] = UNSET
        if not isinstance(self.session_id, Unset):
            session_id = str(self.session_id)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        last_active_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_active_at, Unset):
            last_active_at = self.last_active_at.isoformat()

        closed_at: Union[Unset, str] = UNSET
        if not isinstance(self.closed_at, Unset):
            closed_at = self.closed_at.isoformat()

        live_session: Union[None, Unset, dict[str, Any]]
        if isinstance(self.live_session, Unset):
            live_session = UNSET
        elif isinstance(self.live_session, GetSessionStatusResponse200LiveSessionType0):
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
        if status is not UNSET:
            field_dict["status"] = status
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
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
        from ..models.get_session_status_response_200_live_session_type_0 import GetSessionStatusResponse200LiveSessionType0
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        _session_id = d.pop("session_id", UNSET)
        session_id: Union[Unset, UUID]
        if isinstance(_session_id,  Unset):
            session_id = UNSET
        else:
            session_id = UUID(_session_id)




        _status = d.pop("status", UNSET)
        status: Union[Unset, GetSessionStatusResponse200Status]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = GetSessionStatusResponse200Status(_status)




        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)




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




        _closed_at = d.pop("closed_at", UNSET)
        closed_at: Union[Unset, datetime.datetime]
        if isinstance(_closed_at,  Unset):
            closed_at = UNSET
        else:
            closed_at = isoparse(_closed_at)




        def _parse_live_session(data: object) -> Union['GetSessionStatusResponse200LiveSessionType0', None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                live_session_type_0 = GetSessionStatusResponse200LiveSessionType0.from_dict(data)



                return live_session_type_0
            except: # noqa: E722
                pass
            return cast(Union['GetSessionStatusResponse200LiveSessionType0', None, Unset], data)

        live_session = _parse_live_session(d.pop("live_session", UNSET))


        get_session_status_response_200 = cls(
            success=success,
            session_id=session_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            last_active_at=last_active_at,
            closed_at=closed_at,
            live_session=live_session,
        )


        get_session_status_response_200.additional_properties = d
        return get_session_status_response_200

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
