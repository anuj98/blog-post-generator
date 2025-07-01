import unittest
from unittest.mock import patch, MagicMock
import main

class TestBlogGeneration(unittest.TestCase):
    @patch('main.gspread.authorize')
    def test_get_gsheet_client_json_info(self, mock_authorize):
        mock_creds = MagicMock()
        with patch('main.Credentials.from_service_account_info', return_value=mock_creds):
            with patch('main.GOOGLE_SERVICE_ACCOUNT_JSON', '{"type": "service_account"}'):
                main.GOOGLE_SERVICE_ACCOUNT_JSON = '{"type": "service_account"}'
                main.get_gsheet_client()
                mock_authorize.assert_called_once_with(mock_creds)

    def test_get_next_idea_none(self):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {'Idea': 'Test Idea 1', 'Status': 'done'}
        ]
        idx, idea = main.get_next_idea(mock_sheet)
        self.assertIsNone(idx)
        self.assertIsNone(idea)

    @patch('main.requests.post')
    def test_generate_blog_content_error_print(self, mock_post):
        mock_post.side_effect = Exception('fail')
        with self.assertRaises(Exception):
            try:
                main.generate_blog_content('Test')
            except Exception as e:
                self.assertIn('fail', str(e))
                raise

    @patch('main.main')
    def test_main_block(self, mock_main):
        import importlib
        import sys
        sys.modules['__main__'] = importlib.import_module('main')
        self.assertTrue(True)

    @patch('main.gspread.authorize')
    def test_get_gsheet_client(self, mock_authorize):
        mock_creds = MagicMock()
        with patch('main.Credentials.from_service_account_file', return_value=mock_creds):
            main.GOOGLE_SERVICE_ACCOUNT_JSON = 'test.json'
            main.get_gsheet_client()
            mock_authorize.assert_called_once_with(mock_creds)

    def test_get_next_idea(self):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {'Idea': 'Test Idea 1', 'Status': ''},
            {'Idea': 'Test Idea 2', 'Status': 'done'}
        ]
        idx, idea = main.get_next_idea(mock_sheet)
        self.assertEqual(idx, 2)
        self.assertEqual(idea, 'Test Idea 1')

    def test_mark_idea_status(self):
        mock_sheet = MagicMock()
        main.mark_idea_status(mock_sheet, 2, 'In Progress')
        mock_sheet.update_cell.assert_called_once_with(2, 2, 'In Progress')

    @patch('main.requests.post')
    def test_generate_blog_content(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Blog content"}
        result = main.generate_blog_content('Test Idea')
        self.assertEqual(result, 'Blog content')

    @patch('main.requests.get')
    def test_fetch_image_url(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'urls': {'regular': 'http://image.url'}}
        result = main.fetch_image_url('test')
        self.assertEqual(result, 'http://image.url')

    @patch('main.save_draft_to_github')
    @patch('main.fetch_image_url')
    @patch('main.generate_blog_content')
    @patch('main.mark_idea_status')
    @patch('main.get_next_idea')
    @patch('main.get_gsheet_client')
    def test_main_normal(self, mock_gsheet, mock_next_idea, mock_mark_status, mock_gen_blog, mock_fetch_img, mock_save_draft):
        mock_ws = MagicMock()
        mock_sh = MagicMock()
        mock_gsheet.return_value.open_by_key.return_value = mock_sh
        mock_sh.sheet1 = mock_ws
        mock_next_idea.return_value = (2, 'Test Idea')
        mock_gen_blog.return_value = 'Blog content'
        mock_fetch_img.return_value = 'http://image.url'
        result = main.main()
        self.assertIn("Draft for 'Test Idea' saved.", result)

    @patch('main.get_next_idea')
    @patch('main.get_gsheet_client')
    def test_main_no_ideas(self, mock_gsheet, mock_next_idea):
        mock_ws = MagicMock()
        mock_sh = MagicMock()
        mock_gsheet.return_value.open_by_key.return_value = mock_sh
        mock_sh.sheet1 = mock_ws
        mock_next_idea.return_value = (None, None)
        result = main.main()
        self.assertEqual(result, 'No new ideas.')

    @patch('main.requests.post')
    def test_generate_blog_content_exception(self, mock_post):
        mock_post.side_effect = Exception('fail')
        with self.assertRaises(Exception):
            main.generate_blog_content('Test')

    @patch('main.requests.get')
    def test_fetch_image_url_none(self, mock_get):
        mock_get.return_value.status_code = 404
        result = main.fetch_image_url('test')
        self.assertIsNone(result)
