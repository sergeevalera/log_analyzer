from datetime import date
from pathlib import Path

from log_analyzer.classes import LogFileInfo, LogType, RequestData
from log_analyzer.main import parse_single_line


def test_parse_valid_line():
    content_line = (
        "127.0.0.1 - - [12/Oct/2023:14:49:34 +0000] "
        '"GET /health HTTP/1.1" 200 612 "-" "curl/7.64.0" "-" "-" "-" 0.001'
    )
    expected_result = RequestData(
        remote_addr="127.0.0.1",
        remote_user=None,
        http_x_real_ip=None,
        time_local="12/Oct/2023:14:49:34 +0000",
        request_method="GET",
        request_url="/health",
        request_protocol="HTTP/1.1",
        status=200,
        body_bytes_sent=612,
        http_referer=None,
        http_user_agent="curl/7.64.0",
        http_x_forwarded_for=None,
        http_X_REQUEST_ID=None,
        http_X_RB_USER=None,
        request_time=0.001,
    )

    result = parse_single_line(content_line)
    assert result == expected_result


def test_log_file_info_valid_nginx_log():
    filepath = Path("logs/nginx-access-ui.log-20231012.gz")
    expected_result = LogFileInfo(
        filepath=filepath,
        is_nginx_log=True,
        file_extension=LogType.gzip,
        date_parsed=date(2023, 10, 12),
    )

    result = LogFileInfo(filepath=filepath)
    assert result == expected_result


def test_log_file_info_invalid_date_format():
    filepath = Path("logs/nginx-access-ui.log-2023-10-12.gz")
    expected_result = LogFileInfo(
        filepath=filepath, is_nginx_log=False, file_extension=None, date_parsed=date(1, 1, 1)
    )
    print(expected_result.date_parsed)
    result = LogFileInfo(filepath=filepath)
    print(result.date_parsed)
    assert result == expected_result
