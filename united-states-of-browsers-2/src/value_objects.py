import os
from enum import Enum
from pathlib import Path

import yaml
from pydantic import BaseModel, DirectoryPath, Field, root_validator


class ProductName(str, Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    EDGE = "edge"


class OSName(str, Enum):
    WINDOWS = "nt"
    LINUX = "linux"
    MACOS = "macos"


class DataBaseType(str, Enum):
    SQLITE = "sqlite"


class InfoType(str, Enum):
    HISTORY = "history"
    BOOKMARK = "bookmark"
    LIKED = "liked"


class History(BaseModel):
    db_type: str = Field(alias="type")
    datasource: str = Field(alias="file")
    collection: str
    fields: list[str] = Field(alias="fields")


class Locations(BaseModel):
    profiles: list[str]
    paths: list[DirectoryPath] = Field(alias=OSName(os.name).value)

    @root_validator(pre=True)
    def discard_bad_paths(cls, values):
        values[OSName(os.name).value] = [
            path_
            for path_ in values[OSName(os.name).value]
            if Path(path_).exists()
            ]
        return values


class Browser(BaseModel):
    name: ProductName
    history: History
    locations: Locations


def make_profile(config_dirpath: Path):
    fields = yaml.safe_load((config_dirpath / "fields.yml").read_text())["local"]
    locations = yaml.safe_load((config_dirpath / "locations.yml").read_text())["local"]

    if fields.keys() == locations.keys():
        browser_names = fields.keys() | locations.keys()
    else:
        raise ValueError("Incomplete browser config")

    return [
        Browser(
            name=browser,
            history=fields[browser][InfoType.HISTORY],
            locations=locations[browser],
            )
        for browser in browser_names
        ]


if __name__ == "__main__":
    local_browsers = make_profile(config_dirpath=Path("../configuration"))
    local_browsers
