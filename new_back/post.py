from datetime import date

class Post(object):
    def __init__(self, markdown_parser):
        self._markdown_parser = markdown_parser
        # Properties
        self._spec = 0.1
        self.author = ''
        self.date = date.fromisoformat('2022-07-13')
        self.title = ''
        self.description = ''
        self.category = ''
        self.tags = []
        self.markdown = ''
        return

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec):
        if (spec != 0.1): # We don't have a different version yet
            raise Exception('Invalid Spec version')
        self._spec = spec
        return

    @classmethod
    def from_metadata(cls, markdown_parser, metadata):
        post = cls(markdown_parser)
        header = metadata['header']
        post.markdown = metadata['markdown']
        post.spec = header['Spec']
        post.date = header['Date']
        post.title = header['Title']
        post.description = header['Description']
        post.category = header['Category']
        post.tags = header['Tags']
        return post


class PostList(object):
    def __init__(self, markdown_parser):
        self._markdown_parser = markdown_parser
        self._posts = []

    def __repr__(self):
        return repr([post.title for post in self.posts])

    @property
    def posts(self):
        return self._posts

    @posts.setter
    def posts(self, post_list):
        self._posts = [Post.from_metadata(self._markdown_parser, metadata) for metadata in post_list]
        return

    @classmethod
    def from_list(cls, markdown_parser, post_list):
        instance = cls(markdown_parser)
        instance.posts = post_list
        return instance


