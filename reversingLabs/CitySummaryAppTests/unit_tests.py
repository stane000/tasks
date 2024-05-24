
"""
Unit tests for the TestCityInfoService class.

These tests use mocking to simulate API responses and exceptions,
ensuring that no actual connection to the API is required and no real
data is used. By using mocks, we can create controlled test scenarios
for different response statuses and errors, providing reliable and 
predictable tests.

Each test case focuses on a specific scenario:
- Unauthorized access (HTTP 401)
- Forbidden access (HTTP 403)
- City not found (HTTP 404)
- Generic HTTP errors (e.g., HTTP 500)
- Connection errors
- Timeout errors
- General request errors

This approach ensures that:
- The service's error handling is correctly implemented.
- Different types of exceptions are properly raised and handled.
- The service's behavior remains consistent regardless of actual API availability.

Dependencies:
- unittest: Python's built-in unit testing framework.
- unittest.mock: For creating mock objects and patching.

Example usage:
Run the tests with a command such as `python -m unittest test_city_info_service.py`

"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from requests import HTTPError, RequestException, Timeout
from requests.models import Response

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CitySummaryApp.city_info_service import API_KEY, CityInfoService

class TestCityInfoService(unittest.TestCase):

    def setUp(self):
        self.city = "Zagreb"
        self.service = CityInfoService(self.city)
        self.mock_response = MagicMock(spec=Response)

    @patch.object(CityInfoService, '_CityInfoService__send_get_request')
    def test_get_city_temp(self, mock_send_get_request):

        self.mock_response.json.return_value = {'main': {'temp': '22'}}
        
        # Mock the __send_get_request method
        mock_send_get_request.return_value = self.mock_response
        
        # Call the method and assert the result
        temp = self.service.get_city_temp()
        self.assertEqual(temp, '22', msg=f"Method get_cit_temp returned wrong value: expected 22, actual: {temp}")
        mock_send_get_request.assert_called_once_with(f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric")

    @patch.object(CityInfoService, '_CityInfoService__send_get_request')
    def test_get_city_summary(self, mock_send_get_request):

        self.mock_response.json.return_value = {'extract': 'A summary about the Zagreb'}
        
        # Mock the __send_get_request method
        mock_send_get_request.return_value = self.mock_response
        
        # Call the method and assert the results
        summary = self.service.get_city_summary()
        self.assertEqual(summary, 'A summary about the Zagreb', msg="Method get_city_summary returned wrong value: " + \
                                                                      f"expected 'A summary about the Zagreb', actual: {summary}")
        mock_send_get_request.assert_called_once_with("https://en.wikipedia.org/api/rest_v1/page/summary/" + self.city)

    @patch('requests.get')
    def test_unauthorized_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPError) as context:
            self.service.get_city_summary()
        self.assertEqual(str(context.exception), "Error: Unauthorized. The API key is invalid or expired.")

    @patch('requests.get')
    def test_forbidden_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPError) as context:
            self.service.get_city_summary()
        self.assertEqual(str(context.exception), "Error: Forbidden. The API key does not have the necessary permissions.")

    @patch('requests.get')
    def test_not_found_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPError) as context:
            self.service.get_city_summary()
        self.assertEqual(str(context.exception), 'City Zagreb not exists in database')

    @patch('requests.get')
    def test_generic_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("A generic HTTP error")
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPError) as context:
            self.service.get_city_summary()
        self.assertEqual(str(context.exception), "HTTP error occurred: A generic HTTP error")

    @patch('requests.get')
    def test_timeout_error(self, mock_get):
        mock_get.side_effect = Timeout()

        with self.assertRaises(Timeout) as context:
            self.service.get_city_summary()
        self.assertEqual(str(context.exception), "Error: Timeout. The request took too long to complete.")

    @patch('requests.get')
    def test_generic_request_error(self, mock_get):
        mock_get.side_effect = RequestException("A generic request error")

        with self.assertRaises(RequestException) as context:
            self.service.get_city_summary()
        self.assertEqual(str(context.exception), "Error: An error occurred. A generic request error")

if __name__ == '__main__':
    unittest.main()
