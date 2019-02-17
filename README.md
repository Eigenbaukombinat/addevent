# Simple webform to add events to a caldav calendar

## Install

git clone https://github.com/Eigenbaukombinat/addevent.git
cd addevent 
python3 -m venv .
bin/pip install -r requirements.txt

## Config

cp config.ini.example config.ini
edit config.ini to your needs

## Running

FLASK_APP=app.py bin/flask run -h 0.0.0.0

