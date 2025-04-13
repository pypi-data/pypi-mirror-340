from typing import Dict

import pytz


def datetime_mapper(from_type: str = "datetime64", to_type: str = "timestamp") -> Dict[str, str]:
    time_zones = pytz.all_timezones
    time_resolutions = ["ns", "ms", "us", "s"]
    all_combinations = {f"{from_type}[{res}]": f"{to_type}[{res}][pyarrow]" for res in time_resolutions}
    all_tz_combinations = {
        f"{from_type}[{res}, {tz}]": f"{to_type}[{res}, {tz}][pyarrow]" for res in time_resolutions for tz in time_zones
    }
    all_combinations.update(all_tz_combinations)
    return all_combinations


def reverse_datetime_mapper(
    from_type: str = "timestamp",
    to_type: str = "datetime64",
    adapter: str = "tz=",
) -> Dict[str, str]:
    time_zones = pytz.all_timezones
    time_resolutions = ["ns", "ms", "us", "s"]
    all_combinations = {f"{from_type}[{res}][pyarrow]": f"{to_type}[{res}]" for res in time_resolutions}
    all_tz_combinations = {
        f"{from_type}[{res}, {adapter}{tz}][pyarrow]": f"{to_type}[{res}, {tz}]"
        for res in time_resolutions
        for tz in time_zones
    }
    all_combinations.update(all_tz_combinations)
    return all_combinations
