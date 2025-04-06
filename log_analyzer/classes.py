import re
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger


@dataclass
class LogAnalyzerConfig:
    report_size: int
    report_dir: Path
    log_dir: Path

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogAnalyzerConfig":
        normalized_data = {k.lower(): v for k, v in data.items()}
        report_dir = Path(normalized_data["report_dir"])
        if not report_dir.exists():
            raise ValueError(f"Report directory {report_dir.name} does not exist")
        normalized_data["report_dir"] = report_dir
        log_dir = Path(normalized_data["log_dir"])
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory {cls.log_dir} has been created.")
        normalized_data["log_dir"] = log_dir
        return cls(**normalized_data)


class LogType(Enum):
    plain = auto()
    gzip = auto()


@dataclass
class LogFileInfo:
    filepath: Path
    is_nginx_log: bool = False
    file_extension: Optional[LogType] = None
    date_parsed: Optional[date] = None

    def __post_init__(self):
        pattern = r"^nginx-access-ui\.log-\d{8}(\.gz)?$"
        compiled_re = re.compile(pattern)
        if compiled_re.match(self.filepath.name):
            file_data = self.filepath.name.replace("nginx-access-ui.log-", "").split(".")
            if file_data[-1] == "gz":
                self.file_extension = LogType.gzip
            else:
                self.file_extension = LogType.plain
            try:
                self.date_parsed = datetime.strptime(file_data[0], "%Y%m%d").date()
                self.is_nginx_log = True
            except ValueError:
                self.is_nginx_log = False
        else:
            self.is_nginx_log = False
