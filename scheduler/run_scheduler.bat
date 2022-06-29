SET YYYYMMDD=%date:~0,4%%date:~5,2%%date:~8,2%
SET LOG_FILE=run_scheduler_%YYYYMMDD%.log
cd /d %~dp0

python scheduler.py >> ../log/%LOG_FILE% 2>&1