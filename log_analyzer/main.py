import argparse
import json
from pathlib import Path
from typing import Optional

from loguru import logger

from log_analyzer.classes import LogAnalyzerConfig, LogFileInfo
from log_analyzer.settings import default_config_path


def get_namespace() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", dest="config", type=str, required=False)
    return parser.parse_args()


def get_config(args: argparse.Namespace) -> LogAnalyzerConfig:
    with open(Path(default_config_path), "r") as file:
        config = json.loads(file.read())
    if config_path := args.config:
        logger.info(f"Config path: {config_path}")
        try:
            with open(Path(config_path), "r") as file:
                new_config = json.loads(file.read())
            config = config | {k: v for k, v in new_config.items() if k in config}
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            raise RuntimeError(f"Impossible to read the config file {config_path}.")
    logger.info(f"Config: {config}")
    return LogAnalyzerConfig.from_dict(config)


def get_last_log_file(log_dir: Path) -> Optional[LogFileInfo]:
    last_file = None
    for file in log_dir.iterdir():
        if file.is_file():
            curr_file = LogFileInfo(file)
            if curr_file.is_nginx_log:
                if not last_file:
                    last_file = curr_file
                # here we have just objects with not None in .date_parsed, so we ignore mypy alert
                elif curr_file.date_parsed > last_file.date_parsed:  # type: ignore
                    last_file = curr_file
    return last_file


def analyze(config: LogFileInfo) -> None:
    pass


def main():
    args = get_namespace()
    config = get_config(args)
    last_log_file = get_last_log_file(config.log_dir)
    if not last_log_file:
        logger.info("Log directory doesn't contain any ngins log file")
    else:
        logger.info(f"Last log file in selected directory is {last_log_file.filepath}")
        analyze(last_log_file)


if __name__ == "__main__":
    main()
