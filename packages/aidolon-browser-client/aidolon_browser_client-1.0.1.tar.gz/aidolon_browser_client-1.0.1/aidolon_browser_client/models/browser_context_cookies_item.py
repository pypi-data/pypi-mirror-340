from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="BrowserContextCookiesItem")



@_attrs_define
class BrowserContextCookiesItem:
    """ 
        Attributes:
            name (Union[Unset, str]): Cookie name
            value (Union[Unset, str]): Cookie value
            domain (Union[Unset, str]): Cookie domain
            path (Union[Unset, str]): Cookie path
            expires (Union[Unset, float]): Cookie expiration time
            http_only (Union[Unset, bool]): Whether the cookie is HTTP-only
            secure (Union[Unset, bool]): Whether the cookie is secure
     """

    name: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    domain: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    expires: Union[Unset, float] = UNSET
    http_only: Union[Unset, bool] = UNSET
    secure: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        domain = self.domain

        path = self.path

        expires = self.expires

        http_only = self.http_only

        secure = self.secure


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if value is not UNSET:
            field_dict["value"] = value
        if domain is not UNSET:
            field_dict["domain"] = domain
        if path is not UNSET:
            field_dict["path"] = path
        if expires is not UNSET:
            field_dict["expires"] = expires
        if http_only is not UNSET:
            field_dict["httpOnly"] = http_only
        if secure is not UNSET:
            field_dict["secure"] = secure

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        value = d.pop("value", UNSET)

        domain = d.pop("domain", UNSET)

        path = d.pop("path", UNSET)

        expires = d.pop("expires", UNSET)

        http_only = d.pop("httpOnly", UNSET)

        secure = d.pop("secure", UNSET)

        browser_context_cookies_item = cls(
            name=name,
            value=value,
            domain=domain,
            path=path,
            expires=expires,
            http_only=http_only,
            secure=secure,
        )


        browser_context_cookies_item.additional_properties = d
        return browser_context_cookies_item

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
