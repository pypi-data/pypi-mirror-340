from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.browser_context import BrowserContext





T = TypeVar("T", bound="CreateBrowserSessionBody")



@_attrs_define
class CreateBrowserSessionBody:
    """ 
        Attributes:
            timeout (Union[Unset, int]): Session timeout in seconds Default: 300.
            visible (Union[Unset, bool]): Whether the browser should be visible in the UI Default: True.
            context (Union[Unset, BrowserContext]):
     """

    timeout: Union[Unset, int] = 300
    visible: Union[Unset, bool] = True
    context: Union[Unset, 'BrowserContext'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.browser_context import BrowserContext
        timeout = self.timeout

        visible = self.visible

        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if visible is not UNSET:
            field_dict["visible"] = visible
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.browser_context import BrowserContext
        d = dict(src_dict)
        timeout = d.pop("timeout", UNSET)

        visible = d.pop("visible", UNSET)

        _context = d.pop("context", UNSET)
        context: Union[Unset, BrowserContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = BrowserContext.from_dict(_context)




        create_browser_session_body = cls(
            timeout=timeout,
            visible=visible,
            context=context,
        )


        create_browser_session_body.additional_properties = d
        return create_browser_session_body

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
