import os
from pathlib import Path
from typing import Any

import yaml

from opentakserver.defaultconfig import DefaultConfig


def get_config() -> dict[str, Any]:
    config = DefaultConfig.to_dict()
    config_file = os.path.join(
        config.get("OTS_DATA_FOLDER", os.path.join(Path.home(), "ots")), "config.yml"
    )

    # allow specific override via env
    config_file = os.environ.get("OTS_CONFIG_FILE", config_file)

    if not os.path.exists(config_file):
        DefaultConfig.to_file()  # persist default settings
    else:
        with open(config_file, "r") as f:
            config.update(
                yaml.safe_load(f)
            )  # override defaults with values from config.yml
    return config


cfg = get_config()
