from pathlib import Path
from typing import Any, Callable, Optional, TypedDict

import structlog
from typing_extensions import NotRequired


class LoggerFactoryTypeAnnotation(TypedDict):
    logger_factory: NotRequired[Callable[..., Any]]


def structlog_configure(own_log_filepath: Optional[Path]) -> None:
    kwargs: LoggerFactoryTypeAnnotation = {}
    if own_log_filepath:
        kwargs = {
            "logger_factory": structlog.WriteLoggerFactory(
                file=own_log_filepath.with_suffix(".json").open("wt")
            )
        }
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.EventRenamer("message"),
            structlog.processors.JSONRenderer(),
        ],
        **kwargs
    )


logger = structlog.get_logger()
