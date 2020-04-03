import pytz

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta, time


def calculate_greeting(local_time):
    """Helper function that returns a greeting for a given time."""
    if time(hour=6) <= local_time.time() < time(hour=12):
        data = {'greeting': 'good morning!'}
    elif time(hour=12) <= local_time.time() <= time(hour=17):
        data = {'greeting': 'good afternoon!'}
    elif time(hour=17) < local_time.time() <= time(hour=20):
        data = {'greeting': 'good evening!'}
    else:
        data = {'greeting': 'good night!'}
    return data


@api_view(['POST'])
def generate_greeting(request):
    """Generates a greeting based on the time zone posted."""
    if 'time_zone' in request.data:
        tz = request.data['time_zone']
        if tz.lower() in ['gmt', 'utc']:
            local_time = datetime.now(tz=pytz.timezone('GMT'))
            data = calculate_greeting(local_time)
            status = 200
        elif tz[:3].lower() in ['gmt', 'utc'] and tz[3] in ['+', '-']:
            try:
                datetime.strptime(tz[4:], '%H:%M')
            except ValueError:
                return Response(
                    data={
                        'error': 'the time offset format needs to be \'%H:%M\''
                    },
                    status=400
                )
            offset = tz[4:]
            hours = int(offset[:2])
            minutes = int(offset[3:])
            gmt = datetime.now(tz=pytz.timezone('GMT'))
            if tz[3] == '+':
                if hours > 14 or (hours == 14 and minutes > 0):
                    return Response(
                        data={
                            'error': 'the maximum time offset is 14 hours'
                        },
                        status=400
                    )
                local_time = gmt + timedelta(hours=hours, minutes=minutes)
            else:
                if hours > 12 or (hours == 12 and minutes > 0):
                    return Response(
                        data={
                            'error': 'the minimum time offset is -12 hours'
                        },
                        status=400
                    )
                local_time = gmt - timedelta(hours=hours, minutes=minutes)
            data = calculate_greeting(local_time)
            status = 200
        else:
            data = {
                'error': 'the \'time_zone\' format needs to be \'GMT+HH:MM\' '
                         'or \'GMT-HH:MM\''
            }
            status = 400
    else:
        data = {'error': 'please specify a \'time_zone\' value'}
        status = 400
    return Response(data=data, status=status)
