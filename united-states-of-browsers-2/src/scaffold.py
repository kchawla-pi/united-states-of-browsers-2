from pathlib import Path
from pprint import pprint
from typing import Mapping, Sequence, Type

from pydantic.dataclasses import dataclass

from src.loader import gather_profiles_info
from database.db_reader import DBReader, RelationalDBReader
from database.schema import ChromiumHistorySchema, HistorySchema, FirefoxHistorySchema
from src.value_objects import ProductName, ProfileInfo


@dataclass
class Orchestrator:
    product_profiles: Mapping[ProductName, Sequence[ProfileInfo]]
    history_schemas: Mapping[ProductName, Type[HistorySchema]]
    history_readers: Mapping[ProductName, Type[DBReader]]

    def _make_history_yielders_per_product_profiles(self, product_name: ProductName) -> list[DBReader]:
        return [
            self.history_readers[product_name](
                profile_config=profile_,
                history_schema=self.history_schemas[product_name],
                )
            for profile_ in self.product_profiles[product_name]
            ]

    def _make_history_yielders_all_product_profiles(self):
        return[
            *self._make_history_yielders_per_product_profiles(product_name=ProductName.EDGE),
            *self._make_history_yielders_per_product_profiles(product_name=ProductName.FIREFOX),
            ]

    def _merge_histories_for_all_product_profiles(self) -> list[HistorySchema]:
        return [
            entry
            for product in self._make_history_yielders_all_product_profiles()
            for entry in product.yield_history()
            ]


if __name__ == "__main__":
    profiles_info = gather_profiles_info(config_dirpath=Path("../configuration/browsers"))
    orchestrator = Orchestrator(
        product_profiles=profiles_info,
        history_schemas={ProductName.FIREFOX: FirefoxHistorySchema, ProductName.EDGE: ChromiumHistorySchema},
        history_readers={ProductName.FIREFOX: RelationalDBReader, ProductName.EDGE: RelationalDBReader}
        )
    pprint(orchestrator._merge_histories_for_all_product_profiles())
    ...
