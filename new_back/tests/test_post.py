import unittest

from context import Post

class MarkdownMock(object):
    class Markdown(object):
        def __init__(self):
            pass

post = Post(MarkdownMock)
print(post)
