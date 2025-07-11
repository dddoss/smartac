import unittest
from unittest.mock import patch, MagicMock
from yolink_thermometer import YoLinkThermometer

class TestYoLinkThermometer(unittest.TestCase):
    def setUp(self):
        self.api_key = "fake_api_key"
        self.device_id = "fake_device_id"
        self.thermometer = YoLinkThermometer(self.api_key, self.device_id)

    @patch('yolink_thermometer.requests.post')
    def test_get_temperature_success(self, mock_post):
        # Mock a successful API response with temperature in Celsius
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"state": {"temperature": 25.0}}
        }
        mock_post.return_value = mock_response
        temp_f = self.thermometer.get_temperature()
        self.assertAlmostEqual(temp_f, 77.0)  # 25C = 77F

    @patch('yolink_thermometer.requests.post')
    def test_get_temperature_no_temp(self, mock_post):
        # Mock a response with no temperature
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"state": {}}}
        mock_post.return_value = mock_response
        self.assertIsNone(self.thermometer.get_temperature())

    @patch('yolink_thermometer.requests.post')
    def test_get_temperature_api_error(self, mock_post):
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        self.assertIsNone(self.thermometer.get_temperature())

if __name__ == "__main__":
    unittest.main()
