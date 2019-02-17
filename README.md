# Simple webform to add events to a caldav calendar

## Install

git clone <url>/calwebadd
cd calwebadd 
python3 -m venv .
bin/pip install -r requirements.txt

## Config

cp config.ini.example config.ini
edit config.ini to your needs

## Running

FLASK_APP=create_event.py bin/flask run -h 0.0.0.0

