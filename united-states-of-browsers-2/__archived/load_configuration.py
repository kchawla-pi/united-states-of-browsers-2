from abc import ABCMeta
from enum import Enum
from pathlib import Path
from typing import Iterable, Literal, Mapping

import tomli

from pydantic import BaseModel


configs = tomli.loads(Path("config.toml").read_text())
configs














class Profile(BaseModel):
    name: str
    sources: Iterable[DataSourceDetails]


class LocalConfig(BaseModel):
    product: ProductName
    os: OSName
    data_paths: Iterable[Path]
    profiles: Iterable[Profile]


class ConfigFactory(metaclass=ABCMeta):
    ...


class LocalConfigFactory(ConfigFactory):

    @classmethod
    def from_dict(cls, config_mapping: Mapping):
        LocalConfig
