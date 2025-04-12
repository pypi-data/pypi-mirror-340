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





T = TypeVar("T", bound="GetBrowserContextResponse200")



@_attrs_define
class GetBrowserContextResponse200:
    """ 
        Attributes:
            success (Union[Unset, bool]):  Example: True.
            context (Union[Unset, BrowserContext]):
     """

    success: Union[Unset, bool] = UNSET
    context: Union[Unset, 'BrowserContext'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.browser_context import BrowserContext
        success = self.success

        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.browser_context import BrowserContext
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        _context = d.pop("context", UNSET)
        context: Union[Unset, BrowserContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = BrowserContext.from_dict(_context)




        get_browser_context_response_200 = cls(
            success=success,
            context=context,
        )


        get_browser_context_response_200.additional_properties = d
        return get_browser_context_response_200

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
