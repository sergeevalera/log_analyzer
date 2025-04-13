default_config_path = "log_analyzer/default_config.json"
log_filename_pattern = r"^nginx-access-ui\.log-\d{8}(\.gz)?$"
log_line_pattern = (
    r"(?P<remote_addr>[\d\.]+)\s"
    r"(?P<remote_user>\S*)\s+"
    r"(?P<http_x_real_ip>\S*)\s"
    r"\[(?P<time_local>.*?)\]\s"
    r"\""
    r"(?P<request_method>.*?)\s"
    r"(?P<request_url>.*?)\s"
    r"(?P<request_protocol>.*?)"
    r"\"\s"
    r"(?P<status>\d+)\s"
    r"(?P<body_bytes_sent>\S*)\s"
    r'"(?P<http_referer>.*?)"\s'
    r'"(?P<http_user_agent>.*?)"\s'
    r'"(?P<http_x_forwarded_for>.*?)"\s'
    r'"(?P<http_X_REQUEST_ID>.*?)"\s'
    r'"(?P<http_X_RB_USER>.*?)"\s'
    r"(?P<request_time>\d+\.\d+)\s*"
)
