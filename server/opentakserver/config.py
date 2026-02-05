import os
from pathlib import Path
from typing import Any

import yaml

from opentakserver.defaultconfig import DefaultConfig


def _ensure_bool(v: str) -> bool:
    if v is None:
        return False
    return str(v).lower() in ["true", "1", "yes", "on", "y"]


def _apply_env_overrides(config: dict[str, Any]) -> dict[str, Any]:
    env_lookup = {k.lower(): k for k in os.environ}
    for key in dir(DefaultConfig):
        if key.isupper():
            env_key = env_lookup.get(key.lower())
            if env_key:
                print(f"applying env override for {key}")
                original_value = DefaultConfig.__dict__[key]
                env_value = os.environ[env_key]
                if isinstance(original_value, bool):
                    config[key] = _ensure_bool(env_value)
                elif isinstance(original_value, int):
                    config[key] = int(env_value)
                elif isinstance(original_value, float):
                    config[key] = float(env_value)
                elif isinstance(original_value, list):
                    config[key] = env_value.split(",")
                else:
                    config[key] = env_value
    return config


def get_config() -> dict[str, Any]:
    config = DefaultConfig.to_dict()
    config_file = os.path.join(
        config.get("OTS_DATA_FOLDER", os.path.join(Path.home(), "ots")), "config.yml"
    )

    config_file = os.environ.get("OTS_CONFIG_FILE", config_file)

    if not os.path.exists(config_file):
        # persist defaults, which are derived from environ or defaults during first startup
        DefaultConfig.to_file()
    else:
        # load config from file, backfill missing keys from DefaultConfig
        with open(config_file, "r") as f:
            config.update(yaml.safe_load(f))

    # add option to override both defaults, and file config using environment variables
    if _ensure_bool(os.environ.get("OTS_ENVVAR_OVERRIDES", "False")):
        config = _apply_env_overrides(config)

    return config


cfg = get_config()
