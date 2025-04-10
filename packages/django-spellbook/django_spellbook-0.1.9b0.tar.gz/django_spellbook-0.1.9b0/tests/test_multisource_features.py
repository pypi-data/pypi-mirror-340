import datetime
import tempfile
import shutil
import os
from unittest.mock import Mock, patch, mock_open, ANY
from pathlib import Path
from django.core.management.base import CommandError
from django.test import TestCase
from django_spellbook.management.commands.spellbook_md import Command
from django_spellbook.management.commands.processing.url_view_generator import URLViewGenerator
from django_spellbook.markdown.context import SpellbookContext
from django_spellbook.management.commands.processing.file_processor import ProcessedFile

class TestMultiSourceFeatures(TestCase):
    """Test the multi-source functionality with focused tests"""
    
    def setUp(self):
        """Set up test environment"""
        # Create basic directory paths for testing
        self.docs_dir = '/test/docs_dir'
        self.blog_dir = '/test/blog_dir'
        
        # Initialize URL generators for each app
        self.docs_generator = URLViewGenerator('docs_app', self.docs_dir)
        self.blog_generator = URLViewGenerator('blog_app', self.blog_dir)
        
        # Create test datetime
        self.now = datetime.datetime.now()
    
    def test_app_specific_url_modules(self):
        """Test that each app gets its own URL module"""
        # Verify module names are app-specific
        self.assertEqual(self.docs_generator.urls_module, 'urls_docs_app')
        self.assertEqual(self.docs_generator.views_module, 'views_docs_app')
        self.assertEqual(self.blog_generator.urls_module, 'urls_blog_app')
        self.assertEqual(self.blog_generator.views_module, 'views_blog_app')
    
    def test_app_specific_url_patterns(self):
        """Test that URL patterns include app-specific prefixes"""
        # Create doc context and file
        docs_context = SpellbookContext(
            title='Documentation',
            created_at=self.now,
            updated_at=self.now,
            url_path='docs/guide',
            raw_content='# Documentation\nThis is documentation.'
        )
        
        docs_file = ProcessedFile(
            original_path=Path('/test/docs_dir/guide.md'),
            html_content='<h1>Documentation</h1>',
            template_path=Path('/test/docs_app/templates/docs_app/spellbook_md/guide.html'),
            relative_url='guide',
            context=docs_context
        )
        
        # Create blog context and file
        blog_context = SpellbookContext(
            title='Blog Post',
            created_at=self.now,
            updated_at=self.now,
            url_path='blog/post',
            raw_content='# Blog\nThis is a blog post.'
        )
        
        blog_file = ProcessedFile(
            original_path=Path('/test/blog_dir/post.md'),
            html_content='<h1>Blog Post</h1>',
            template_path=Path('/test/blog_app/templates/blog_app/spellbook_md/post.html'),
            relative_url='post',
            context=blog_context
        )
        
        # Generate URL data for both files
        with patch.object(self.docs_generator, '_write_file'):
            with patch.object(self.blog_generator, '_write_file'):
                docs_url_data = self.docs_generator._generate_url_data(docs_file)
                blog_url_data = self.blog_generator._generate_url_data(blog_file)
        
        # Verify app-specific URL patterns
        self.assertIn("name='docs_app_guide'", docs_url_data['url_pattern'])
        self.assertIn("name='blog_app_post'", blog_url_data['url_pattern'])
        
        # Verify app-specific template paths
        self.assertIn("'docs_app/spellbook_md/guide.html'", docs_url_data['view_content'])
        self.assertIn("'blog_app/spellbook_md/post.html'", blog_url_data['view_content'])
    
    def test_main_urls_includes_multiple_apps(self):
        """Test that URLs file content properly includes multiple apps"""
        # Create a dictionary of modules and prefixes like our implementation would use
        includes = {
            'urls_docs_app': 'docs_app',
            'urls_blog_app': 'blog_app'
        }
        
        # Generate the includes string directly
        includes_str = ',\n    '.join([
            f"path('{prefix}/', include('django_spellbook.{module}'))" 
            for module, prefix in includes.items()
        ])
        
        # Create the final content using the template
        content = self.docs_generator.MAIN_URLS_TEMPLATE.format(includes=includes_str)
        
        # Verify the content includes both apps
        self.assertIn("include('django_spellbook.urls_docs_app')", content)
        self.assertIn("include('django_spellbook.urls_blog_app')", content)
        self.assertIn("path('docs_app/'", content)
        self.assertIn("path('blog_app/'", content)
        
    class TestURLPrefixHandling(TestCase):
        """Test proper handling of URL prefixes in URL generation"""
        
        def setUp(self):
            self.generator = URLViewGenerator('test_app', '/test/path')
        
        @patch('os.path.exists')
        def test_no_duplicate_slashes(self, mock_exists):
            """Test that URL paths don't accumulate duplicate slashes"""
            mock_exists.return_value = True
            
            # Create a mock file with pre-existing URLs that have trailing slashes
            initial_content = """
from django.urls import path, include

urlpatterns = [
    path('test_app/', include('django_spellbook.urls_test_app'))
]
"""
            # Create an open mock that tracks writes
            file_contents = {'urls.py': initial_content}
            
            def mock_open_with_tracking(file_path, mode):
                nonlocal file_contents
                mock = mock_open(read_data=file_contents.get(file_path, ''))()
                original_write = mock.write
                
                def write_with_tracking(content):
                    file_contents[file_path] = content
                    return original_write(content)
                
                mock.write = write_with_tracking
                return mock
            
            # First update - should maintain one slash
            with patch('builtins.open', side_effect=mock_open_with_tracking):
                self.generator._update_main_urls_file()
                result1 = file_contents.get('urls.py', '')
                self.assertIn("path('test_app/", result1)
                self.assertNotIn("path('test_app//", result1)
            
            # Second update - should still maintain one slash
            with patch('builtins.open', side_effect=mock_open_with_tracking):
                self.generator._update_main_urls_file()
                result2 = file_contents.get('urls.py', '')
                self.assertIn("path('test_app/", result2)
                self.assertNotIn("path('test_app//", result2)