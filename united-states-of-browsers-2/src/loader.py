from pathlib import Path

import yaml

from src.value_objects import Browser, InfoType, ProductName, ProfileHistory, ProfileInfo


def load_app_config(config_dirpath: Path):
    return yaml.safe_load((config_dirpath / "app.yml").read_text())


def load_profile_configs(config_dirpath: Path):
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


def make_profiles_info(profile_data: Browser):
    return [
        ProfileInfo(
            product=profile_data.name,
            profile_name=profile_name_,
            history=ProfileHistory(db_path=data_path_, **profile_data.history.dict()),
            )
        for profile_name_, profile_path_ in profile_data.locations.profile_paths.items()
        for data_path_ in profile_path_.rglob(f"*{profile_data.history.db_file}")
        if data_path_
        ]


def gather_profiles_info(config_dirpath: Path) -> dict[ProductName, list[ProfileInfo]]:
    local_browsers = load_profile_configs(config_dirpath=config_dirpath)
    return {ProductName(browser.name): make_profiles_info(browser) for browser in local_browsers if browser.locations.profile_paths}


if __name__ == "__main__":
    profiles_config = gather_profiles_info(config_dirpath=Path("../configuration/browsers"))
    app_config = load_app_config(config_dirpath=Path("../configuration"))
    ...
