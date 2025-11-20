@echo off
echo Initializing database...
python init_db.py
echo Starting the application...
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --port=5000
