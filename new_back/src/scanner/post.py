import re
from datetime import date

from unidecode import unidecode

class Post(object):
    def __init__(self, markdown_lib):
        self._markdown_lib = markdown_lib
        self._markdown_parser = self._markdown_lib.Markdown()
        # Properties
        self._markdown = ''
        self._html = ''
        # To not break repr
        self._date = date.today()
        self._category = ''
        self._title = ''
        return

    def __repr__(self):
        formatted_date = self.date.strftime('%Y/%m/%d')
        return f'{self.category}/{formatted_date}/{self.slug}'

    @staticmethod
    def slugify(text):
        """
        Returns a slug string valid for URLs.
        """
        ascii_text = unidecode(text)
        return re.sub(r'[-\s]+', '-',
                      (re.sub(r'[^\w\s-]', '', ascii_text).strip().lower()))

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec):
        if (spec != 0.1): # We don't have a different version yet
            raise Exception('Invalid Spec version')
        self._spec = spec
        self._markdown_parser = self._markdown_lib.Markdown(
            extensions=[],
            extensions_config={},
            output_format='html',
            tab_length=4
        )
        return

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self.spec = header['Spec']
        self._date = header['Date']
        self._title = header['Title']
        self._description = header['Description']
        self._category = header['Category']
        self._tags = header['Tags']
        self._header = header
        return

    @property
    def date(self):
        return self._date

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def category(self):
        return self._category

    @property
    def tags(self):
        return self._tags

    @property
    def markdown(self):
        return self._markdown

    @markdown.setter
    def markdown(self, markdown):
        self._markdown = markdown
        self._html = self._markdown_parser.convert(self._markdown)
        return

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, *args):
        raise Exception('This property isn\'t writable.')

    @property
    def slug(self):
        return self.slugify(self.title)

    @classmethod
    def from_metadata(cls, markdown_parser, metadata):
        post = cls(markdown_parser)
        post.header = metadata['header']
        post.markdown = metadata['markdown']
        post.full = metadata['full']
        return post


class PostList(object):
    def __init__(self, markdown_lib):
        self._markdown_lib = markdown_lib
        self._posts = []

    def __repr__(self):
        return repr(self.posts)

    @property
    def posts(self):
        return self._posts

    @posts.setter
    def posts(self, post_list):
        self._posts = [Post.from_metadata(self._markdown_lib, metadata) for metadata in post_list]
        return

    @classmethod
    def from_list(cls, markdown_lib, post_list):
        instance = cls(markdown_lib)
        instance.posts = post_list
        return instance

