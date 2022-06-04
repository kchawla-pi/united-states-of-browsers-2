from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import Sequence, Type

from database.db_reader import DBReader, RelationalDBReader
from database.schema import ChromiumHistorySchema, FirefoxHistorySchema, HistorySchema
from config_loader.loader import gather_profiles_info
from value_objects import ProductName, ProfileInfo


class HistorySchemaOptions(Enum):
    EDGE = ChromiumHistorySchema
    CHROME = ChromiumHistorySchema
    FIREFOX = FirefoxHistorySchema


@dataclass
class ProductHistory:
    product: ProductName
    profiles: Sequence[ProfileInfo]
    schema: Type[HistorySchema]
    reader: Type[DBReader]

    def _make_history_yielders(self):
        return (
            entry
            for profile_ in self.profiles
            for entry in self.reader(profile_, self.schema).yield_history()
            )


if __name__ == "__main__":
    profiles_info = gather_profiles_info(config_dirpath=Path("../configuration/browsers"))

    pprint(
        list(
            ProductHistory(
                product=ProductName.FIREFOX,
                profiles=profiles_info[ProductName.FIREFOX],
                schema=FirefoxHistorySchema,
                reader=RelationalDBReader,
                )._make_history_yielders()
            )
        )
    pprint(
        list(
    ProductHistory(
        product=ProductName.EDGE,
        profiles=profiles_info[ProductName.EDGE],
        schema=ChromiumHistorySchema,
        reader=RelationalDBReader,
        )._make_history_yielders()
            ))
