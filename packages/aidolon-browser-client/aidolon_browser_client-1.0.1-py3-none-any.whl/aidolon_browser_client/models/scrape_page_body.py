from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.scrape_page_body_format_item import ScrapePageBodyFormatItem
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="ScrapePageBody")



@_attrs_define
class ScrapePageBody:
    """ 
        Attributes:
            format_ (Union[Unset, list[ScrapePageBodyFormatItem]]): Content formats to return
            delay (Union[Unset, float]): Delay in seconds before scraping
            screenshot (Union[Unset, bool]): Whether to include a screenshot Default: False.
            pdf (Union[Unset, bool]): Whether to include a PDF version Default: False.
     """

    format_: Union[Unset, list[ScrapePageBodyFormatItem]] = UNSET
    delay: Union[Unset, float] = UNSET
    screenshot: Union[Unset, bool] = False
    pdf: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        format_: Union[Unset, list[str]] = UNSET
        if not isinstance(self.format_, Unset):
            format_ = []
            for format_item_data in self.format_:
                format_item = format_item_data.value
                format_.append(format_item)



        delay = self.delay

        screenshot = self.screenshot

        pdf = self.pdf


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if format_ is not UNSET:
            field_dict["format"] = format_
        if delay is not UNSET:
            field_dict["delay"] = delay
        if screenshot is not UNSET:
            field_dict["screenshot"] = screenshot
        if pdf is not UNSET:
            field_dict["pdf"] = pdf

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        format_ = []
        _format_ = d.pop("format", UNSET)
        for format_item_data in (_format_ or []):
            format_item = ScrapePageBodyFormatItem(format_item_data)



            format_.append(format_item)


        delay = d.pop("delay", UNSET)

        screenshot = d.pop("screenshot", UNSET)

        pdf = d.pop("pdf", UNSET)

        scrape_page_body = cls(
            format_=format_,
            delay=delay,
            screenshot=screenshot,
            pdf=pdf,
        )


        scrape_page_body.additional_properties = d
        return scrape_page_body

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
