SET YYYYMMDD=%date:~0,4%%date:~5,2%%date:~8,2%
SET LOG_FILE=run_server_%YYYYMMDD%.log
cd /d %~dp0

python api_server.py >> log/%LOG_FILE% 2>&1