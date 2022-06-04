from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import Sequence, Type

from dataclasses import dataclass

from database.db_reader import DBReader, RelationalDBReader
from database.schema import ChromiumHistorySchema, FirefoxHistorySchema, HistorySchema, SchemaOptions
from config_loader.loader import gather_profiles_info
from value_objects import ProductName, ProfileInfo


class HistorySchemaOptions(Enum):
    EDGE = ChromiumHistorySchema
    CHROME = ChromiumHistorySchema
    FIREFOX = FirefoxHistorySchema


@dataclass
class ProfileHistory:
    profile: ProfileInfo
    source_schema: Type[HistorySchema]
    reader: Type[DBReader]

    @classmethod
    def from_profiles_info(
        cls,
        profiles_info: Sequence[ProfileInfo],
        source_schema: Type[HistorySchema],
        reader: Type[DBReader],
        ):
        return [
            cls(
                profile=profile_,
                source_schema=source_schema,
                reader=reader,
                )
            for profile_ in profiles_info
            ]

    @property
    def yielder(self):
        return self.reader(self.profile, self.source_schema).yielder


@dataclass
class ProductHistory:
    product: ProductName
    profiles: Sequence[ProfileHistory]

    def _make_history_yielders(self):
        return (
            entry
            for profile_ in self.profiles
            for entry in profile_.yielder
            )


if __name__ == "__main__":
    profiles_info = gather_profiles_info(config_dirpath=Path("../configuration/browsers"))

    pprint(
        list(
            ProductHistory(
                product=ProductName.FIREFOX,
                profiles=ProfileHistory.from_profiles_info(
                    profiles_info=profiles_info[ProductName.FIREFOX],
                    source_schema=SchemaOptions[ProductName.FIREFOX],
                    reader=RelationalDBReader,
                    )
                )._make_history_yielders()
            )
        )
    pprint(
        list(
            ProductHistory(
                product=ProductName.EDGE,
                profiles=[
                    ProfileHistory(
                        profile=profile_,
                        source_schema=ChromiumHistorySchema,
                        reader=RelationalDBReader,
                        )
                    for profile_ in profiles_info[ProductName.EDGE]
                    ],
                )._make_history_yielders()
            )
        )
