# greetings
### Description
A simple REST API that recieves a time zone and returns the appropriate greeting.
### Installation
```
git clone https://github.com/jackwsellers/greetings.git
cd greetings
virtualenv appenv
source appenv/bin/activate
pip install -r requirements.txt
cd app
python manage.py migrate
```
### Testing
Run unit tests:
```
python manage.py test
```
Run the server:
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/greetings/ to post your time_zone using the browsable API.

The time_zone field must be of the format 'GMT+HH:MM' or 'GMT-HH:MM' where HH:MM denotes the time offset.

The offset must be between -12:00 and +14:00.

For example, the following request might be made by someone in Afghanistan (GMT+04:30):
```
curl --header "Content-Type: application/json" -X POST --data '{"time_zone": "GMT+04:30"}' 'http://127.0.0.1:8000/greetings/'
```
If there is no offset - either 'GMT', 'GMT-00:00' or 'GMT+00:00' can be used.

Also, 'GMT' can be replaced by 'UTC' and both can either be lower or upper case.
