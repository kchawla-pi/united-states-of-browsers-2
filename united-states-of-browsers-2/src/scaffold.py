from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Sequence

from src.history_reader import ProductHistory, ProfileHistory
from src.config_loader.loader import gather_profiles_info
from src.database.db_reader import RelationalDBReader
from src.database.schema import SchemaOptions
from src.value_objects import ProductName


@dataclass
class Orchestrator:
    history_readers: Sequence[ProductHistory]

    @classmethod
    def from_profiles_info(cls, profiles_info):
        return cls(
            history_readers=[
                ProductHistory(
                    product=ProductName(product_name),
                    profiles=ProfileHistory.from_profiles_info(
                        profiles_info=profiles_info[ProductName(product_name)],
                        source_schema=SchemaOptions[ProductName(product_name)],
                        reader=RelationalDBReader,
                        )
                    )
                for product_name in profiles_info
                ]
            )

    def _make_history_yielders(self):
        return (
            entry
            for reader in self.history_readers
            for entry in reader._make_history_yielders()
            )


if __name__ == "__main__":
    profiles_info = gather_profiles_info(config_dirpath=Path("../configuration/browsers"))
    orchestrator = Orchestrator.from_profiles_info(profiles_info)
    pprint(list(orchestrator._make_history_yielders()))
    ...
