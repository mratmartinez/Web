import unittest
from datetime import date

from context import Post

class MarkdownMock(object):
    class Markdown(object):
        def __init__(self, *args, **kwargs):
            pass

        def convert(self, markdown):
            return markdown.upper()

metadata = {
    'header': {
        'Spec': 0.1,
        'Date': date.today(),
        'Title': 'A test post',
        'Description': 'A test description',
        'Category': 'test',
        'Tags': ['test', 'example']
    },
    'full': '',
    'markdown': '# A test title'
}
post = Post.from_metadata(MarkdownMock, metadata)

class TestStringMethods(unittest.TestCase):
    def test_slug(self):
        self.assertEqual(post.slug, 'a-test-post')

    # should call Markdown.convert()
    def test_html(self):
        self.assertEqual(post.html, '# A TEST TITLE')

if __name__ == '__main__':
    unittest.main()
