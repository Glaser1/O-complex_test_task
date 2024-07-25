import unittest
from unittest.mock import Mock, patch

from app.app import app, WEATHER_FORECAST_API_URL, API_KEY, fetch_weather


class FetchWeatherTestCase(unittest.TestCase):

    @patch('app.requests.get')
    def test_fetch_weather_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_weather('New York')
        self.assertIsNotNone(result)

    @patch('app.requests.get')
    def test_fetch_weather__failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_weather('NonExistentCity')
        self.assertIsNone(result)

    @patch('app.requests.get')
    def test_fetch_weather__wrong_api_key(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result = fetch_weather('NonExistentCity')
        self.assertEqual(result.status_code, 401)

    def tests_weather_api_content_success(self):
        ...



if __name__ == '__main__':
    unittest.main()
