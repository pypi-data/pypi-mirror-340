import tempfile
from pathlib import Path

from ten_utils.env_loader.loader import EnvLoader
from ten_utils.log import Logger, LoggerConfig


if __name__ == '__main__':
    LoggerConfig().set_default_level_log(1)

    logger = Logger(__name__)

    temp_dir = Path(tempfile.mkdtemp())
    missing_path = temp_dir / ".env.missing"

    EnvLoader(path_to_env_file=missing_path)
    # test = env_loader.load("TEST", type_env_var=list)
    # print(test)

    logger.debug("Debug message", additional_info=False)
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
