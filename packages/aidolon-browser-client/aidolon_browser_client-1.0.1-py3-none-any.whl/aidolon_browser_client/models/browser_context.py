from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.browser_context_session_storage import BrowserContextSessionStorage
  from ..models.browser_context_cookies_item import BrowserContextCookiesItem
  from ..models.browser_context_local_storage import BrowserContextLocalStorage





T = TypeVar("T", bound="BrowserContext")



@_attrs_define
class BrowserContext:
    """ 
        Attributes:
            cookies (Union[Unset, list['BrowserContextCookiesItem']]):
            local_storage (Union[Unset, BrowserContextLocalStorage]): Local storage key-value pairs
            session_storage (Union[Unset, BrowserContextSessionStorage]): Session storage key-value pairs
            user_agent (Union[Unset, str]): User agent used by the browser
     """

    cookies: Union[Unset, list['BrowserContextCookiesItem']] = UNSET
    local_storage: Union[Unset, 'BrowserContextLocalStorage'] = UNSET
    session_storage: Union[Unset, 'BrowserContextSessionStorage'] = UNSET
    user_agent: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.browser_context_session_storage import BrowserContextSessionStorage
        from ..models.browser_context_cookies_item import BrowserContextCookiesItem
        from ..models.browser_context_local_storage import BrowserContextLocalStorage
        cookies: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cookies, Unset):
            cookies = []
            for cookies_item_data in self.cookies:
                cookies_item = cookies_item_data.to_dict()
                cookies.append(cookies_item)



        local_storage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.local_storage, Unset):
            local_storage = self.local_storage.to_dict()

        session_storage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.session_storage, Unset):
            session_storage = self.session_storage.to_dict()

        user_agent = self.user_agent


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if cookies is not UNSET:
            field_dict["cookies"] = cookies
        if local_storage is not UNSET:
            field_dict["localStorage"] = local_storage
        if session_storage is not UNSET:
            field_dict["sessionStorage"] = session_storage
        if user_agent is not UNSET:
            field_dict["userAgent"] = user_agent

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.browser_context_session_storage import BrowserContextSessionStorage
        from ..models.browser_context_cookies_item import BrowserContextCookiesItem
        from ..models.browser_context_local_storage import BrowserContextLocalStorage
        d = dict(src_dict)
        cookies = []
        _cookies = d.pop("cookies", UNSET)
        for cookies_item_data in (_cookies or []):
            cookies_item = BrowserContextCookiesItem.from_dict(cookies_item_data)



            cookies.append(cookies_item)


        _local_storage = d.pop("localStorage", UNSET)
        local_storage: Union[Unset, BrowserContextLocalStorage]
        if isinstance(_local_storage,  Unset):
            local_storage = UNSET
        else:
            local_storage = BrowserContextLocalStorage.from_dict(_local_storage)




        _session_storage = d.pop("sessionStorage", UNSET)
        session_storage: Union[Unset, BrowserContextSessionStorage]
        if isinstance(_session_storage,  Unset):
            session_storage = UNSET
        else:
            session_storage = BrowserContextSessionStorage.from_dict(_session_storage)




        user_agent = d.pop("userAgent", UNSET)

        browser_context = cls(
            cookies=cookies,
            local_storage=local_storage,
            session_storage=session_storage,
            user_agent=user_agent,
        )


        browser_context.additional_properties = d
        return browser_context

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
