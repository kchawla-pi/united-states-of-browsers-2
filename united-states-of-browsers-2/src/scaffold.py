from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Sequence

from history_reader import ProductHistory
from config_loader.loader import gather_profiles_info
from database.db_reader import RelationalDBReader
from database.schema import ChromiumHistorySchema, FirefoxHistorySchema
from src.value_objects import ProductName


@dataclass
class Orchestrator:
    hsitory_readers: Sequence[ProductHistory]

    def _make_history_yielders(self):
        return (
            entry
            for reader in self.hsitory_readers
            for entry in reader._make_history_yielders()
            )


if __name__ == "__main__":
    profiles_info = gather_profiles_info(config_dirpath=Path("../configuration/browsers"))
    orchestrator = Orchestrator(
        hsitory_readers=[
            ProductHistory(
                product=ProductName.FIREFOX,
                profiles=profiles_info[ProductName.FIREFOX],
                schema=FirefoxHistorySchema,
                reader=RelationalDBReader,
                ),
            ProductHistory(
                product=ProductName.EDGE,
                profiles=profiles_info[ProductName.EDGE],
                schema=ChromiumHistorySchema,
                reader=RelationalDBReader,
                ),
            ]
        )
    pprint(list(orchestrator._make_history_yielders()))
    ...
