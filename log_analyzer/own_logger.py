from pathlib import Path
from typing import Any, Callable, List, Optional, TypedDict

import structlog
from typing_extensions import NotRequired


class LoggerFactoryTypeAnnotation(TypedDict):
    logger_factory: NotRequired[Callable[..., Any]]


def structlog_configure(own_log_filepath: Optional[Path]) -> None:
    kwargs: LoggerFactoryTypeAnnotation = {}
    processors: List = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.EventRenamer("message"),
    ]
    if own_log_filepath:
        kwargs["logger_factory"] = structlog.WriteLoggerFactory(
            file=own_log_filepath.with_suffix(".json").open("wt")
        )
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(processors, **kwargs)


logger = structlog.get_logger()
