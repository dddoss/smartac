import unittest
from unittest.mock import patch, MagicMock
from yolink_outlet import YoLinkOutlet

class TestYoLinkOutlet(unittest.TestCase):
    def setUp(self):
        self.api_key = "fake_api_key"
        self.device_id = "fake_device_id"
        self.outlet = YoLinkOutlet(self.api_key, self.device_id)

    @patch('yolink_outlet.requests.post')
    def test_power_on(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        result = self.outlet.power_on()
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch('yolink_outlet.requests.post')
    def test_power_off(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        result = self.outlet.power_off()
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch('yolink_outlet.requests.post')
    def test_get_status_on(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"state": {"state": "on"}}}
        mock_post.return_value = mock_response
        status = self.outlet.get_status()
        self.assertEqual(status, "on")

    @patch('yolink_outlet.requests.post')
    def test_get_status_none(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        status = self.outlet.get_status()
        self.assertIsNone(status)

if __name__ == "__main__":
    unittest.main()
