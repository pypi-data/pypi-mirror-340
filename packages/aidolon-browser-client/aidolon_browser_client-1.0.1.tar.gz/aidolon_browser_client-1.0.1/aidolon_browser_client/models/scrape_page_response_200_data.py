from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.scrape_page_response_200_data_json import ScrapePageResponse200DataJson





T = TypeVar("T", bound="ScrapePageResponse200Data")



@_attrs_define
class ScrapePageResponse200Data:
    """ 
        Attributes:
            html (Union[Unset, str]): HTML content (if requested)
            text (Union[Unset, str]): Plain text content (if requested)
            json (Union[Unset, ScrapePageResponse200DataJson]): Structured JSON representation (if requested)
            markdown (Union[Unset, str]): Markdown content (if requested)
            screenshot (Union[Unset, str]): Base64-encoded screenshot (if requested)
            pdf (Union[Unset, str]): Base64-encoded PDF (if requested)
     """

    html: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    json: Union[Unset, 'ScrapePageResponse200DataJson'] = UNSET
    markdown: Union[Unset, str] = UNSET
    screenshot: Union[Unset, str] = UNSET
    pdf: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        from ..models.scrape_page_response_200_data_json import ScrapePageResponse200DataJson
        html = self.html

        text = self.text

        json: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.json, Unset):
            json = self.json.to_dict()

        markdown = self.markdown

        screenshot = self.screenshot

        pdf = self.pdf


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if html is not UNSET:
            field_dict["html"] = html
        if text is not UNSET:
            field_dict["text"] = text
        if json is not UNSET:
            field_dict["json"] = json
        if markdown is not UNSET:
            field_dict["markdown"] = markdown
        if screenshot is not UNSET:
            field_dict["screenshot"] = screenshot
        if pdf is not UNSET:
            field_dict["pdf"] = pdf

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scrape_page_response_200_data_json import ScrapePageResponse200DataJson
        d = dict(src_dict)
        html = d.pop("html", UNSET)

        text = d.pop("text", UNSET)

        _json = d.pop("json", UNSET)
        json: Union[Unset, ScrapePageResponse200DataJson]
        if isinstance(_json,  Unset):
            json = UNSET
        else:
            json = ScrapePageResponse200DataJson.from_dict(_json)




        markdown = d.pop("markdown", UNSET)

        screenshot = d.pop("screenshot", UNSET)

        pdf = d.pop("pdf", UNSET)

        scrape_page_response_200_data = cls(
            html=html,
            text=text,
            json=json,
            markdown=markdown,
            screenshot=screenshot,
            pdf=pdf,
        )


        scrape_page_response_200_data.additional_properties = d
        return scrape_page_response_200_data

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
