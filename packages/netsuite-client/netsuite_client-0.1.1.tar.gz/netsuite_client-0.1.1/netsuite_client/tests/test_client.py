import unittest
from unittest.mock import Mock, patch, call
from requests.exceptions import HTTPError, Timeout, RequestException
from netsuite_client import NetSuiteClient, NetSuiteError

class TestNetSuiteClient(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = Mock()
        self.mock_response = Mock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {"items": []}
        self.mock_session.request.return_value = self.mock_response

        with patch('requests.Session', return_value=self.mock_session):
            self.client = NetSuiteClient(
                realm="test_realm",
                account="test_account",
                consumer_key="test_consumer_key",
                consumer_secret="test_consumer_secret",
                token_id="test_token_id",
                token_secret="test_token_secret",
                logger=Mock(),
                timeout=30
            )

    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.realm, "test_realm")
        self.assertEqual(self.client.account, "test_account")
        self.assertEqual(self.client.consumer_key, "test_consumer_key")
        self.assertEqual(self.client.consumer_secret, "test_consumer_secret")
        self.assertEqual(self.client.token_id, "test_token_id")
        self.assertEqual(self.client.token_secret, "test_token_secret")
        self.assertEqual(self.client.timeout, 30)

    def test_get_success(self):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        self.mock_session.request.return_value = mock_response
        
        result = self.client.get("https://test.com", {"param": "value"})
        self.assertEqual(result, {"success": True})
        self.mock_session.request.assert_called_once()

    def test_get_failure(self):
        """Test failed GET request."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        self.mock_session.request.return_value = mock_response
        
        with self.assertRaises(NetSuiteError):
            self.client.get("https://test.com", {"param": "value"})

    def test_post_success(self):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        self.mock_session.request.return_value = mock_response
        
        result = self.client.post("https://test.com", {"data": "value"})
        self.assertEqual(result, {"success": True})
        self.mock_session.request.assert_called_once()

    def test_post_failure(self):
        """Test failed POST request."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        self.mock_session.request.return_value = mock_response
        
        with self.assertRaises(NetSuiteError):
            self.client.post("https://test.com", {"data": "value"})

    def test_get_suiteql_query(self):
        """Test SuiteQL query execution."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": 1}]}
        self.mock_session.request.return_value = mock_response
        
        query = "SELECT * FROM transaction"
        result = self.client.get_suiteql_query(query)
        self.assertEqual(result, {"items": [{"id": 1}]})
        self.mock_session.request.assert_called_once()

    def test_get_scriptlet(self):
        """Test scriptlet execution."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        self.mock_session.request.return_value = mock_response
        
        params = {"script": "123", "deploy": "1"}
        result = self.client.get_scriptlet(params)
        self.assertEqual(result, {"success": True})
        self.mock_session.request.assert_called_once()

    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_retry_logic(self, mock_sleep):
        """Test retry logic for failed requests."""
        # Create mock responses
        error_response = Mock()
        error_response.status_code = 500
        error_response.text = "Internal Server Error"

        success_response = Mock()
        success_response.status_code = 200
        success_response.json.return_value = {"success": True}
        
        # Set up the sequence of responses
        self.mock_session.request.side_effect = [
            error_response,
            error_response,
            success_response
        ]
        
        result = self.client.get("https://test.com")
        
        # Verify the result
        self.assertEqual(result, {"success": True})
        self.assertEqual(self.mock_session.request.call_count, 3)
        
        # Verify sleep was called with exponential backoff
        mock_sleep.assert_has_calls([
            call(2),  # 2^1
            call(4),  # 2^2
        ])

    def test_timeout(self):
        """Test request timeout."""
        self.mock_session.request.side_effect = Timeout("Request timed out")
        with self.assertRaises(NetSuiteError) as context:
            self.client.get("https://test.com")
        self.assertIn("Request timed out", str(context.exception))

if __name__ == '__main__':
    unittest.main() 