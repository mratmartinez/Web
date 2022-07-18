import unittest
from datetime import date

from context import Post

class MarkdownMock(object):
    class Markdown(object):
        def __init__(self, *args, **kwargs):
            pass

        def convert(self, markdown):
            return markdown

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
    'markdown': ''
}
post = Post.from_metadata(MarkdownMock, metadata)

class TestStringMethods(unittest.TestCase):
    def test_slug(self):
        self.assertEqual(post.slug, 'a-test-post')

if __name__ == '__main__':
    unittest.main()
