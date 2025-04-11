from typing import Any, Literal

from ten_utils.common.constants import LOGGER_LEVELS


def validate_value_default_level_log(value: Any) -> Literal[0, 1, 2, 3, 4]:
    if value not in LOGGER_LEVELS.keys():
        return 1

    else:
        return value


def validate_value_save_log_to_file(value: Any) -> bool:
    if type(value) is not bool:
        return False

    else:
        return value
