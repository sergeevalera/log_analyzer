import argparse
import json
from pathlib import Path
from typing import Dict, Union

from loguru import logger

from log_analyzer.settings import default_config_path


def get_namespace() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", dest="config", type=str, required=False)
    return parser.parse_args()


def get_config(args: argparse.Namespace) -> Dict[str, Union[str, int]]:
    with open(Path(default_config_path), "r") as file:
        config: Dict[str, Union[str, int]] = json.loads(file.read())
    if config_path := args.config:
        logger.info(f"Config path: {config_path}")
        try:
            with open(Path(config_path), "r") as file:
                new_config = json.loads(file.read())
            config = config | {k: v for k, v in new_config.items() if k in config}
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            raise RuntimeError(f"Impossible to read the config file {config_path}.")
    logger.info(f"Config: {config}")
    return config


def analyze(config: Dict[str, Union[str, int]]) -> None:
    pass


def main():
    args = get_namespace()
    config = get_config(args)
    analyze(config)


if __name__ == "__main__":
    main()
