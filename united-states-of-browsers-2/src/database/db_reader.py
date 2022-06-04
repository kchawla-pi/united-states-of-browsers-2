import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from pprint import pprint
from typing import Type

from pydantic.dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from config_loader.loader import gather_profiles_info
from database.schema import ChromiumHistorySchema, FirefoxHistorySchema, HistorySchema
from src.value_objects import ProductName, ProfileInfo

logger = logging.getLogger(__name__)


def yield_temp_copy(filepath):
    yield filepath
    # with NamedTemporaryFile(prefix=f"{filepath.name}-") as temp_file:
    #     shutil.copy(filepath, temp_file.name)
    #     yield temp_file.name


class DBReader(metaclass=ABCMeta):
    profile_config : ProfileInfo
    history_schema: Type[HistorySchema]

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def yield_history(self):
        ...


@dataclass
class RelationalDBReader(DBReader):
    profile_config: ProfileInfo
    history_schema: Type[HistorySchema]

    def connect(self) -> Engine:
        connection_string = (
            f"{self.profile_config.history.db_type}:///"
            f"{next(yield_temp_copy(self.profile_config.history.db_path))}"
        )
        logger.debug("DB Connection string: %s", connection_string)
        return create_engine(
            connection_string,
            echo=True,
            future=True,
            )

    def yield_history(self):
        # db_engine.execution_options()
        with Session(bind=self.connect(), future=True) as session:
            for history in session.query(self.history_schema):
                yield self.profile_config.product, self.profile_config.profile_name, history


class RelationalDBWriter:
    ...



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    profiles_info = gather_profiles_info(config_dirpath=Path("../../configuration/browsers"))
    # read_history = BrowserReader(profile_config=profiles_info[ProductName.FIREFOX][0], history_schema=FirefoxHistory)
    for profile_ in profiles_info[ProductName.EDGE]:
        read_history = RelationalDBReader(profile_config=profile_, history_schema=ChromiumHistorySchema)
        pprint(list(read_history.yield_history()))
        # pprint([history for history in next(read_history.connect())])
    for profile_ in profiles_info[ProductName.FIREFOX]:
        read_history = RelationalDBReader(profile_config=profile_, history_schema=FirefoxHistorySchema)
        pprint(list(read_history.yield_history()))
