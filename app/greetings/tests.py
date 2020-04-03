import pytz

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta

from greetings.views import calculate_greeting


class GreetingsTests(TestCase):
    """Testing the Greetings API."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('generate')

    def calculate_tz(self, greeting):
        """
        Helper function that calculates a valid time zone for a given greeting.
        """
        gmt = datetime.now(tz=pytz.timezone('GMT'))
        for hours in range(-12, 15):
            local_time = gmt + timedelta(hours=hours)
            data = calculate_greeting(local_time)
            if data['greeting'] == greeting:
                break
        if len(str(abs(hours))) == 1:
            offset = '0{}:00'.format(abs(hours))
        else:
            offset = '{}:00'.format(abs(hours))
        if hours > 0:
            return 'GMT+{}'.format(offset)
        else:
            return 'GMT-{}'.format(offset)

    def test_gmt(self):
        """Test with a time_zone value of 'GMT'."""
        payload = {'time_zone': 'GMT'}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_not_gmt_or_utc(self):
        """Test with a time_zone that is not 'GMT' or 'UTC'."""
        payload = {'time_zone': 'EST'}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['error'],
            'the \'time_zone\' format needs to be \'GMT+HH:MM\' '
            'or \'GMT-HH:MM\''
        )

    def test_no_tz(self):
        """Test with no time_zone."""
        payload = {}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['error'], 'please specify a \'time_zone\' value'
        )

    def test_invalid_offset_format(self):
        """Test with an invalid offset format."""
        payload = {'time_zone': 'GMT+1'}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['error'], 'the time offset format needs to be \'%H:%M\''
        )

    def test_offset_gt_maximum(self):
        """Test with an offset that is greater than the maximum."""
        payload = {'time_zone': 'GMT+14:30'}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['error'], 'the maximum time offset is 14 hours'
        )

    def test_offset_lt_maximum(self):
        """Test with an offset that is less than the minimum."""
        payload = {'time_zone': 'GMT-12:30'}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['error'], 'the minimum time offset is -12 hours'
        )

    def test_greetings(self):
        """Test with a different time zone for each expected greeting."""
        for greeting in [
            'good morning!', 'good afternoon!', 'good evening!', 'good night!'
        ]:
            tz = self.calculate_tz(greeting)
            payload = {'time_zone': tz}
            res = self.client.post(self.url, payload)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data['greeting'], greeting)
