# log_analyzer
Analyzer for nginx logs

## How to run

Install poetry with any way you prefer
https://python-poetry.org/docs/#installation

Create an enviroment
poetry install

Run the script
poetry run analyzer

If you want to specify config:
poetry run analyzer --config "your/config/path"

In config you can specify all or just part of fields:
- REPORT_SIZE - how many urls with maximal total request time would be included to the report
- REPORT_DIR - the directory where report should be created
- LOG_DIR - the directory where log to analyze are placed
- OWN_LOG_FILEPATH - filepath for own logs of script. If null, logs would be passed to stdout
- TRESHOLD_ERROR_PERC - treshold of unparsable line percentage (if real percentage is higher,
report wouldn't be created)
