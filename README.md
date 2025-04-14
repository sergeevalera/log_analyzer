# log_analyzer
This project analyzes Nginx log files to extract and compute statistical metrics from the most recent log file. The report provides a detailed breakdown of the metrics for each URL encountered in the log file.

<ins>For each URL found in the log file, the report includes the following metrics:</ins>\
**count** - the absolute number of times the URL appears in the log file.\
**count_perc** -the percentage of total requests that the URL represents.\
**time_sum** - the total request time for the URL, in absolute value.\
**time_perc** - the percentage of total request time that the URL represents.\
**time_avg** - the average request time for the URL.\
**time_max** - the maximum request time for the URL.\
**time_med** - the median request time for the URL.

## How to run

**Install poetry**\
[Poetry installation ways](https://python-poetry.org/docs/#installation)

**Create an enviroment**
```bash
poetry install
```

**Run the script**
```bash
poetry run analyzer
```

**If you want you can specify config**
```bash
poetry run analyzer --config "your/config/path"
```

In config you can specify all or just part of fields:
- **REPORT_SIZE** - how many urls with maximal total request time would be included to the report
- **REPORT_DIR** - the directory where report should be created
- **LOG_DIR** - the directory where log to analyze are placed
- **OWN_LOG_FILEPATH** - filepath for own logs of script. If null, logs would be passed to stdout
- **TRESHOLD_ERROR_PERC** - treshold of unparsable line percentage (if real percentage is higher,
report wouldn't be created)

Default config availavle [here](log_analyzer/default_config.json)
