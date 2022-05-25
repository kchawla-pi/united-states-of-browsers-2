import os
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, DirectoryPath, Field, FilePath, root_validator


class ProductName(str, Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    EDGE = "edge"


class OSName(str, Enum):
    WINDOWS = "nt"
    LINUX = "posix"
    MACOS = "macos"


class DataBaseType(str, Enum):
    SQLITE = "sqlite"


class InfoType(str, Enum):
    HISTORY = "history"
    BOOKMARK = "bookmark"
    LIKED = "liked"


class BaseHistory(BaseModel):
    db_type: str
    db_file: str
    collection: str
    fields: list[str] = Field(alias="fields")


class ProfileHistory(BaseHistory):
    db_path: FilePath


class Locations(BaseModel):
    profiles: list[str]
    paths: list[DirectoryPath] = Field(alias=OSName(os.name).value)
    profile_paths: dict[str, DirectoryPath] = Field(default_factory=list)

    @root_validator(pre=True)
    def discard_bad_paths(cls, values):
        values[OSName(os.name).value] = [
            Path(path_).expanduser().resolve()
            for path_ in values.get(OSName(os.name).value)
            if path_ and Path(path_).expanduser().resolve().exists()
            ]
        return values

    @root_validator()
    def make_profile_paths(cls, values):
        values["profile_paths"] = {
            profile_: list(path_.glob(f"*{profile_}"))[0]
            for path_ in values["paths"]
            for profile_ in values["profiles"]
            }
        return values


class ProfileInfo(BaseModel):
    product: ProductName
    profile_name: str
    history: ProfileHistory


class Browser(BaseModel):
    name: ProductName
    history: BaseHistory
    locations: Locations
