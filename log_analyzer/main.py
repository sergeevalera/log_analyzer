import argparse
import gzip
import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any, Dict, Generator, Optional, Union, cast

from log_analyzer.classes import LogAnalyzerConfig, LogFileInfo, LogType, RequestData
from log_analyzer.own_logger import logger
from log_analyzer.settings import default_config_path, log_line_pattern


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
                elif curr_file.date_parsed > last_file.date_parsed:
                    last_file = curr_file
    return last_file


def get_file_content_by_lines(file: LogFileInfo) -> Generator[str, None, None]:
    open_func = open if file.file_extension == LogType.plain else gzip.open
    file_content = open_func(file.filepath, "rt")
    for content_line in file_content:
        yield content_line
    file_content.close()


def parse_single_line(content_line: str) -> Optional[RequestData]:
    if match := re.compile(log_line_pattern).match(content_line):
        return RequestData(**cast(Dict[str, Any], match.groupdict()))
    return None


def analyze_file_content(
    log_file: LogFileInfo, report_size: int
) -> Generator[Dict[str, Union[str, float, None]], None, None]:
    total_lines = 0
    parsed_lines = 0
    request_time = 0.0  # total for all requests
    count: Dict[str, int] = defaultdict(int)
    time_sum: Dict[str, float] = defaultdict(float)
    request_time_lists = defaultdict(list)

    for line_content in get_file_content_by_lines(log_file):
        total_lines += 1
        if line_parsed := parse_single_line(line_content):
            parsed_lines += 1
            request_time += line_parsed.request_time
            count[line_parsed.request_url] += 1
            time_sum[line_parsed.request_url] += line_parsed.request_time
            request_time_lists[line_parsed.request_url].append(line_parsed.request_time)

    for url in [k for k, v in sorted(time_sum.items(), key=lambda item: item[1], reverse=True)][
        :report_size
    ]:
        yield {
            "url": url,
            "count": count[url],
            "count_perc": count[url] / parsed_lines * 100,
            "time_sum": time_sum[url],
            "time_perc": time_sum[url] / request_time * 100,
            "time_avg": time_sum[url] / count[url],
            "time_max": max(request_time_lists[url]),
            "time_med": median(request_time_lists[url]),
        }


def generate_report(file_to_analyze: LogFileInfo, config: LogAnalyzerConfig):
    report_dir = Path(config.report_dir)
    if not report_dir.exists():
        report_dir.mkdir(parents=True)

    with open("log_analyzer/report.html", "r") as report_template_file:
        report_template = report_template_file.read()

    report_path = report_dir / f"report-{file_to_analyze.date_parsed.strftime('%Y.%m.%d')}.html"

    with open(report_path, "w") as report_file:
        report_file.write(
            report_template.replace(
                "$table_json",
                json.dumps(list(analyze_file_content(file_to_analyze, config.report_size))),
            )
        )


def main():
    try:
        args = get_namespace()
        config = get_config(args)
        if last_log_file := get_last_log_file(config.log_dir):
            logger.info(f"Last log file in selected directory is {last_log_file.filepath}")
            generate_report(file_to_analyze=last_log_file, config=config)
        else:
            logger.info("Log directory doesn't contain any nginx log file")

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
