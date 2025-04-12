from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.scrape_information_body_level_of_detail import ScrapeInformationBodyLevelOfDetail
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="ScrapeInformationBody")



@_attrs_define
class ScrapeInformationBody:
    """ 
        Attributes:
            description (str): Natural language description of the information to scrape
            level_of_detail (Union[Unset, ScrapeInformationBodyLevelOfDetail]): Level of detail to return:
                * brief - concise summary
                * standard - balanced detail
                * full - comprehensive details
                 Default: ScrapeInformationBodyLevelOfDetail.FULL.
     """

    description: str
    level_of_detail: Union[Unset, ScrapeInformationBodyLevelOfDetail] = ScrapeInformationBodyLevelOfDetail.FULL
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> dict[str, Any]:
        description = self.description

        level_of_detail: Union[Unset, str] = UNSET
        if not isinstance(self.level_of_detail, Unset):
            level_of_detail = self.level_of_detail.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
        })
        if level_of_detail is not UNSET:
            field_dict["level_of_detail"] = level_of_detail

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        _level_of_detail = d.pop("level_of_detail", UNSET)
        level_of_detail: Union[Unset, ScrapeInformationBodyLevelOfDetail]
        if isinstance(_level_of_detail,  Unset):
            level_of_detail = UNSET
        else:
            level_of_detail = ScrapeInformationBodyLevelOfDetail(_level_of_detail)




        scrape_information_body = cls(
            description=description,
            level_of_detail=level_of_detail,
        )


        scrape_information_body.additional_properties = d
        return scrape_information_body

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
