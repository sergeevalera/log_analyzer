import re
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Optional

from log_analyzer.own_logger import logger
from log_analyzer.settings import log_filename_pattern


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
    date_parsed: date = datetime.min

    def __post_init__(self):
        compiled_re = re.compile(log_filename_pattern)
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


@dataclass
class RequestData:
    remote_addr: str
    remote_user: Optional[str]
    http_x_real_ip: Optional[str]
    time_local: str
    request_method: str
    request_url: str
    request_protocol: str
    status: int
    body_bytes_sent: int
    http_referer: Optional[str]
    http_user_agent: Optional[str]
    http_x_forwarded_for: Optional[str]
    http_X_REQUEST_ID: Optional[str]
    http_X_RB_USER: Optional[str]
    request_time: float

    def __post_init__(self):
        self.status = int(self.status)
        self.remote_user = None if self.remote_user == "-" else self.remote_user
        self.http_x_real_ip = None if self.http_x_real_ip == "-" else self.http_x_real_ip
        self.body_bytes_sent = int(self.body_bytes_sent)
        self.http_referer = None if self.http_referer == "-" else self.http_referer
        self.http_user_agent = None if self.http_user_agent == "-" else self.http_user_agent
        self.http_x_forwarded_for = (
            None if self.http_x_forwarded_for == "-" else self.http_x_forwarded_for
        )
        self.http_X_REQUEST_ID = None if self.http_X_REQUEST_ID == "-" else self.http_X_REQUEST_ID
        self.http_X_RB_USER = None if self.http_X_RB_USER == "-" else self.http_X_RB_USER
        self.request_time = float(self.request_time)
