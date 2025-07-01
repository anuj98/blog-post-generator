import unittest
from unittest.mock import patch
import publish_to_devto

class TestPublishToDevto(unittest.TestCase):
    @patch('publish_to_devto.requests.post')
    def test_publish_to_devto_success(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'url': 'http://dev.to/article'}
        with patch('builtins.print') as mock_print:
            publish_to_devto.publish_to_devto('Title', 'Content', 'key')
            mock_print.assert_any_call('Published to dev.to:', 'http://dev.to/article')

    @patch('publish_to_devto.requests.post')
    def test_publish_to_devto_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = 'Bad Request'
        with patch('builtins.print') as mock_print:
            publish_to_devto.publish_to_devto('Title', 'Content', 'key')
            mock_print.assert_any_call('Failed to publish to dev.to:', 'Bad Request')

    @patch('publish_to_devto.publish_to_devto')
    def test_main(self, mock_publish):
        with patch('builtins.open', unittest.mock.mock_open(read_data='# Title\nContent')):
            with patch.dict('os.environ', {'BLOG_FILE': 'file.md', 'DEVTO_API_KEY': 'key'}):
                publish_to_devto.main()
        self.assertTrue(mock_publish.called)
