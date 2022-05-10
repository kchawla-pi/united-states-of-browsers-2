from pathlib import Path
from typing import Iterable, Mapping

from pydantic import BaseModel

from src.value_objects import OSName, ProductName




class BrowserProfileBuilder(BaseModel):
    config_map: Mapping

    def build(self):
        for k, v self.config_map




class LocalConfiguration(BaseModel):
    identifier: str
    paths: Mapping[OSName, Iterable[Path]]
    names: Iterable[str]


class CloudConfiguration(BaseModel):
    ...


class ProductConfiguration(BaseModel):
    name: ProductName
    local: LocalConfiguration
    cloud: CloudConfiguration


class Configuration(BaseModel):
    products: Iterable[ProductConfiguration]
