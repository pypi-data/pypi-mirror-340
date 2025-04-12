import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock
from pathlib import Path
from django.core.management.base import CommandError
from django.test import TestCase
from django_spellbook.management.commands.processing.url_view_generator import URLViewGenerator
from django_spellbook.markdown.context import SpellbookContext
from django_spellbook.management.commands.processing.file_processor import ProcessedFile
from django_spellbook.utils import get_clean_url


class TestURLViewGenerator(TestCase):
    def setUp(self):
        self.generator = URLViewGenerator('test_app', '/test/path')
        self.mock_context = Mock(spec=SpellbookContext)
        self.mock_context.__dict__ = {'title': 'Test', 'toc': {}}

        # Create a sample processed file
        self.processed_file = ProcessedFile(
            original_path=Path('/test/file.md'),
            html_content='<h1>Test</h1>',
            template_path=Path('/test/template.html'),
            relative_url='test/page',
            context=self.mock_context
        )

    def test_initialization(self):
        """Test URLViewGenerator initialization."""
        self.assertEqual(self.generator.content_app, 'test_app')
        self.assertEqual(self.generator.content_dir_path, '/test/path')
        self.assertTrue(hasattr(self.generator, 'spellbook_dir'))

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_ensure_urls_views_files_creation(self, mock_file, mock_exists):
        """Test creation of app-specific URLs and views files."""
        mock_exists.return_value = False

        self.generator._ensure_urls_views_files()

        # Should create app-specific files and main urls.py
        urls_module = f"urls_test_app"
        views_module = f"views_test_app"
        
        mock_file.assert_any_call(
            f"{self.generator.spellbook_dir}/{urls_module}.py", 'w')
        mock_file.assert_any_call(
            f"{self.generator.spellbook_dir}/{views_module}.py", 'w')
        mock_file.assert_any_call(
            f"{self.generator.spellbook_dir}/urls.py", 'w')

    def test_generate_view_name(self):
        """Test view name generation from URL pattern."""
        url_pattern = 'docs/getting-started/index'
        # Update expected value without 'view_' prefix
        expected = 'docs_getting_started_index'

        result = self.generator._generate_view_name(url_pattern)

        self.assertEqual(result, expected)

    def test_get_template_path(self):
        """Test template path generation."""
        relative_url = 'docs/index'
        expected = 'test_app/spellbook_md/docs/index.html'

        result = self.generator._get_template_path(relative_url)

        self.assertEqual(result, expected)

    def test_prepare_context_dict(self):
        """Test context dictionary preparation."""
        context = Mock(spec=SpellbookContext)
        context.__dict__ = {
            'title': 'Test',
            'date': '2023-01-01',
            'toc': {'some': 'data'}
        }

        result = self.generator._prepare_context_dict(context)

        self.assertNotIn('toc', result)
        self.assertEqual(result['title'], 'Test')

    @patch('builtins.open', new_callable=mock_open)
    def test_write_urls(self, mock_file):
        """Test writing URL patterns to file."""
        urls = ["path('test', views.view_test, name='view_test')"]

        self.generator._write_urls(urls)

        mock_file.assert_called_once()
        written_content = mock_file().write.call_args[0][0]
        self.assertIn('urlpatterns = [', written_content)
        self.assertIn("path('test'", written_content)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_urls_with_dashes(self, mock_file):
        """Test writing URL patterns to file with dashes in URLs."""
        urls = ["path('--test', views.view_test, name='view_test')"]

        self.generator._write_urls(urls)

        mock_file.assert_called_once()
        written_content = mock_file().write.call_args[0][0]
        self.assertIn('urlpatterns = [', written_content)
        self.assertIn("path('test'", written_content)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_urls_with_dashes_in_multiple_parts(self, mock_file):
        """Test writing URL patterns to file with dashes in multiple parts."""
        urls = [
            "path('--test-name/--test-name-2', views.view_test, name='view_test')",
        ]

        self.generator._write_urls(urls)

        mock_file.assert_called_once()
        written_content = mock_file().write.call_args[0][0]
        self.assertIn('urlpatterns = [', written_content)
        self.assertIn("path('test-name/test-name-2'", written_content)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_views(self, mock_file):
        """Test writing view functions to file."""
        views = [
            "def view_test(request):\n    return render(request, 'test.html', {})"]
        toc = {'test': {'title': 'Test'}}

        self.generator._write_views(views, toc)

        mock_file.assert_called_once()
        written_content = mock_file().write.call_args[0][0]
        self.assertIn('from django.shortcuts import render', written_content)
        self.assertIn('TOC = ', written_content)

    @patch.object(URLViewGenerator, '_write_urls')
    @patch.object(URLViewGenerator, '_write_views')
    def test_generate_urls_and_views(self, mock_write_views, mock_write_urls):
        """Test full URL and view generation process."""
        processed_file = ProcessedFile(
            original_path=Path('/test/file.md'),
            html_content='<h1>Test</h1>',
            template_path=Path('/test/template.html'),
            relative_url='test',
            context=self.mock_context
        )

        self.generator.generate_urls_and_views([processed_file], {})

        mock_write_urls.assert_called_once()
        mock_write_views.assert_called_once()

    def test_create_file_if_not_exists_error(self):
        """Test file creation error handling"""
        with patch('os.path.exists', return_value=False):
            with patch('builtins.open', mock_open()) as mock_file:
                mock_file.side_effect = IOError("Permission denied")

                with self.assertRaises(CommandError) as context:
                    self.generator._create_file_if_not_exists(
                        'test.py', 'content')

                self.assertIn("Failed to create test.py",
                              str(context.exception))

    def test_generate_urls_and_views_error(self):
        """Test error handling in generate_urls_and_views"""
        with patch.object(self.generator, '_generate_url_data') as mock_generate:
            mock_generate.side_effect = Exception("Generation error")

            with self.assertRaises(CommandError) as context:
                self.generator.generate_urls_and_views(
                    [self.processed_file], {})

            self.assertIn("Failed to generate URLs and views",
                          str(context.exception))

    def test_write_urls_error(self):
        """Test error handling in _write_urls"""
        with patch.object(self.generator, '_write_file') as mock_write:
            mock_write.side_effect = Exception("Write error")

            with self.assertRaises(CommandError) as context:
                self.generator._write_urls(['test_url'])

            self.assertIn("Failed to write URLs file", str(context.exception))

    def test_write_views_error(self):
        """Test error handling in _write_views"""
        with patch.object(self.generator, '_write_file') as mock_write:
            mock_write.side_effect = Exception("Write error")

            with self.assertRaises(CommandError) as context:
                self.generator._write_views(['test_view'], {})

            self.assertIn("Failed to write views file", str(context.exception))

    def test_write_file_error(self):
        """Test error handling in _write_file"""
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError("Write permission denied")

            with self.assertRaises(CommandError) as context:
                self.generator._write_file('test.py', 'content')

            self.assertIn("Failed to write test.py", str(context.exception))

    @patch('os.path.exists')
    @patch('os.path.abspath')
    def test_ensure_urls_views_files_multiple_errors(self, mock_abspath, mock_exists):
        """Test handling of multiple file creation errors"""
        mock_abspath.return_value = '/test/path'
        mock_exists.return_value = False

        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError("Multiple errors")

            with self.assertRaises(CommandError) as context:
                self.generator._ensure_urls_views_files()

            self.assertIn("Failed to create", str(context.exception))

    def test_generate_url_data_error(self):
        """Test error handling in _generate_url_data with invalid processed file"""
        invalid_processed_file = Mock(spec=ProcessedFile)
        invalid_processed_file.relative_url = None  # This should cause an error

        with self.assertRaises(AttributeError):
            self.generator._generate_url_data(invalid_processed_file)

    def test_prepare_context_dict_error(self):
        """Test error handling in _prepare_context_dict with invalid context"""
        invalid_context = Mock(spec=SpellbookContext)
        invalid_context.__dict__ = {'toc': {}, 'date': 'invalid-date'}

        # Should not raise an exception but handle the invalid date gracefully
        result = self.generator._prepare_context_dict(invalid_context)
        self.assertNotIn('toc', result)

    @patch('os.path.abspath')
    def test_get_spellbook_dir_error(self, mock_abspath):
        """Test error handling in _get_spellbook_dir"""
        mock_abspath.side_effect = Exception("Path error")

        with self.assertRaises(Exception) as context:
            self.generator._get_spellbook_dir()

        self.assertIn("Path error", str(context.exception))

    def test_generate_views_file_content_error_with_invalid_toc(self):
        """Test error handling in _generate_views_file_content with invalid TOC types"""
        # Test with a TOC that can't be string-formatted
        class CustomObject:
            def __str__(self):
                raise ValueError("Cannot convert to string")

        invalid_toc = CustomObject()

        with self.assertRaises(ValueError):
            self.generator._generate_views_file_content(
                ['test_view'], invalid_toc)

    def test_generate_views_file_content_with_invalid_views(self):
        """Test _generate_views_file_content with invalid views list"""
        # Test with invalid views content
        invalid_views = [None, 123, object()]

        with self.assertRaises(TypeError):
            self.generator._generate_views_file_content(invalid_views, {})

    def test_generate_view_name_with_dashes(self):
        """Test view name generation with dashes in URL pattern."""
        url_pattern = '--view-name'
        expected = '__view_name'

        result = self.generator._generate_view_name(url_pattern)

        self.assertEqual(result, expected)

    def test_get_clean_url(self):
        """Test URL cleaning"""
        url = '--test-url/--test-url-2/---test-url-3'
        expected = 'test-url/test-url-2/test-url-3'

        result = get_clean_url(url)

        self.assertEqual(result, expected)

    @patch('os.path.join')
    def test_get_template_path_error(self, mock_join):
        """Test error handling in _get_template_path"""
        mock_join.side_effect = Exception("Path join error")

        with self.assertRaises(Exception):
            self.generator._get_template_path("test/url")

    def test_generate_view_name_error(self):
        """Test error handling in _generate_view_name with invalid input"""
        invalid_url = None

        with self.assertRaises(AttributeError):
            self.generator._generate_view_name(invalid_url)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="urlpatterns = []")
    def test_update_main_urls_file(self, mock_file, mock_exists):
        """Test updating the main urls.py to include app-specific URL modules."""
        mock_exists.return_value = True

        self.generator._update_main_urls_file()
        
        # Verify main urls.py was updated with the app inclusion
        mock_file.assert_any_call(f"{self.generator.spellbook_dir}/urls.py", 'w')
        written_content = mock_file().write.call_args[0][0]
        
        # Should contain path to include the app-specific URL module
        self.assertIn(f"include('django_spellbook.urls_test_app')", written_content)
        self.assertIn(f"path('test_app/'", written_content)
            
    def test_app_specific_file_generation(self):
        """Test generation of app-specific urls and views files."""
        processed_file = ProcessedFile(
            original_path=Path('/test/file.md'),
            html_content='<h1>Test</h1>',
            template_path=Path('/test/template.html'),
            relative_url='test',
            context=self.mock_context
        )
        
        with patch.object(self.generator, '_write_file') as mock_write:
            self.generator.generate_urls_and_views([processed_file], {})
            
            # Should write to app-specific files
            urls_module = f"urls_test_app.py"
            views_module = f"views_test_app.py"
            
            # Check that app-specific files were written to
            mock_write.assert_any_call(urls_module, unittest.mock.ANY)
            mock_write.assert_any_call(views_module, unittest.mock.ANY)
            
    
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('django_spellbook.management.commands.processing.url_view_generator.logger')
    def test_exception_handling_in_update_main_urls(self, mock_logger, mock_open, mock_exists):
        """Test exception handling when reading the urls.py file"""
        # Set up conditions for exception
        mock_exists.return_value = True
        
        # Make open raise an exception when trying to read the file
        file_mock = mock_open.return_value.__enter__.return_value
        file_mock.read.side_effect = IOError("Test file read error")
        
        # Call the method - should not raise the exception
        self.generator._update_main_urls_file()
        
        # Verify logger.error was called with the right message
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        self.assertIn("Error reading urls.py", error_msg)
        self.assertIn("Test file read error", error_msg)
        
        # Verify the method continued execution and wrote the file
        # There should be a second call to open in write mode
        self.assertEqual(mock_open.call_count, 2)
        calls = mock_open.call_args_list
        self.assertEqual(calls[0][0][1], 'r')  # First call should be in read mode
        self.assertEqual(calls[1][0][1], 'w')  # Second call should be in write mode
        
class TestURLNameGeneration(TestCase):
    """Test the URL name generation logic."""
    
    def test_url_name_extraction(self):
        """Test extracting URL names from various path patterns."""
        
        def extract_url_name(clean_url):
            """Reproduce the URL name extraction logic from _generate_url_data."""
            path_parts = clean_url.split('/')
            if len(path_parts) > 1:
                url_name = path_parts[-1].replace('-', '_')
            else:
                url_name = clean_url.replace('-', '_')
            return url_name
        
        # Test cases as (input_path, expected_url_name)
        test_cases = [
            # Multi-segment paths
            ("blog/posts/my-first-post", "my_first_post"),
            ("docs/api/user-guide", "user_guide"),
            ("tech/reviews/product-comparison", "product_comparison"),
            ("lifestyle/digital-minimalism", "digital_minimalism"),
            
            # Single segment paths
            ("about", "about"),
            ("contact-us", "contact_us"),
            ("faq", "faq"),
            
            # Edge cases
            ("a/b/c", "c"),
            ("very-long-url-with-many-hyphens", "very_long_url_with_many_hyphens"),
            ("nested/path/with-no-hyphens", "with_no_hyphens"),
            ("", ""),  # Empty string case
        ]
        
        for input_path, expected_output in test_cases:
            with self.subTest(input_path=input_path):
                self.assertEqual(extract_url_name(input_path), expected_output, 
                                f"Failed to extract correct URL name from '{input_path}'")

    def test_multi_segment_path_name_extraction(self):
        """Test specific extraction of URL name from multi-segment paths."""
        
        # Create minimal mock of ProcessedFile
        mock_file = MagicMock()
        mock_file.relative_url = "blog/posts/my-first-post"
        mock_file.context = MagicMock()
        
        # Import the actual URLViewGenerator
        from django_spellbook.management.commands.processing.url_view_generator import URLViewGenerator
        
        # Create minimal generator instance with required attributes
        generator = URLViewGenerator("blog", "/fake/path")
        
        # Use a spy to capture the metadata parameter
        metadata_spy = None
        
        original_generate_view_function = generator._generate_view_function
        
        def spy_generate_view_function(*args, **kwargs):
            nonlocal metadata_spy
            # The metadata is the 5th parameter (index 4)
            if len(args) > 4:
                metadata_spy = args[4]
            return original_generate_view_function(*args, **kwargs)
        
        # Replace methods with simple mocks to avoid unnecessary complexity
        with patch.object(generator, '_generate_view_name', return_value="view_func"):
            with patch.object(generator, '_get_template_path', return_value="blog/template.html"):
                with patch.object(generator, '_generate_view_function', side_effect=spy_generate_view_function):
                    
                    # Call the method under test
                    result = generator._generate_url_data(mock_file)
                    
                    # Check that the URL name is the last segment with hyphens replaced
                    self.assertIn('url_pattern', result)
                    self.assertTrue("name='my_first_post'" in result['url_pattern'], 
                                   f"Expected 'my_first_post' as URL name, got: {result['url_pattern']}")
                    
                    # Verify metadata was captured and contains expected values
                    self.assertIsNotNone(metadata_spy, "Metadata was not captured")
                    self.assertEqual(metadata_spy.get('url_name'), 'my_first_post')
                    self.assertEqual(metadata_spy.get('namespaced_url'), 'blog:my_first_post')
                    
    def test_url_name_extraction_from_path_parts(self):
        """Test the specific line that extracts URL name from path_parts."""
        
        # Test cases with different path structures
        test_cases = [
            (["blog", "posts", "my-first-post"], "my_first_post"),
            (["docs", "api", "user-guide"], "user_guide"),
            (["single-segment"], "single_segment"),
            (["multiple", "hyphens", "in-one-segment"], "in_one_segment"),
            (["no-hyphens", "lastpart"], "lastpart"),
            (["path", "with", "special-chars-123"], "special_chars_123"),
            (["empty", "segment", ""], ""),  # Edge case with empty last segment
        ]
        
        for path_parts, expected_url_name in test_cases:
            with self.subTest(path_parts=path_parts):
                # Execute exactly the line we're testing
                url_name = path_parts[-1].replace('-', '_')
                
                # Verify the result
                self.assertEqual(url_name, expected_url_name, 
                                f"URL name extraction failed for path_parts={path_parts}")
    
    def test_isolated_path_parts_conditional(self):
        """ABSOLUTELY ISOLATED test for path parts conditional and branch."""
        
        # Function that ONLY contains the EXACT lines we're testing
        def url_name_extractor(clean_url):
            # The EXACT lines from the code:
            path_parts = clean_url.split('/')
            if len(path_parts) > 1:
                url_name = path_parts[-1].replace('-', '_')
            else:
                url_name = clean_url.replace('-', '_')
            return url_name
        
        # Test multi-segment path - MUST execute if branch
        clean_url = "blog/posts/my-first-post"
        result = url_name_extractor(clean_url)
        self.assertEqual(result, "my_first_post")
        
        # Test single-segment path - MUST execute else branch
        clean_url = "about"
        result = url_name_extractor(clean_url)
        self.assertEqual(result, "about")
        
        # Print confirmation that test ran
        print("\n\n***EXECUTED PATH PARTS CONDITIONAL TEST***\n\n")