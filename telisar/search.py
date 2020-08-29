from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.qparser import QueryParser

import textwrap
import html2markdown
import os
import re


class Indexer:
    """
    Create or update the search index.
    """
    schema = Schema(
        filename=ID(stored=True),
        title=TEXT(stored=True),
        content=TEXT(stored=True),
        tags=KEYWORD
    )

    def __init__(self, source_path, data_path):
        self._index = None
        self._source_path = source_path
        self._data_path = data_path

    @property
    def index(self):
        if not self._index:
            if not os.path.exists(self._data_path):
                os.mkdir(self._data_path)
                self._index = index.create_in(self._data_path, self.schema)
                self.build(self._index)
            else:
                self._index = index.open_dir(self._data_path)
        return self._index

    def _add_to_index(self, ix, path):
        writer = ix.writer()
        with open(path) as post:
            writer.add_document(
                filename=path,
                title=path,
                content=post.read(),
                tags='session',
            )
            writer.commit()

    def build(self, index):
        for root, dirs, files in os.walk(self._source_path):
            for filename in files:
                self._add_to_index(index, os.path.join(root, filename))


class Searcher:
    """
    Search the index.
    """

    def __init__(self, source_path, data_path):
        self.ix = Indexer(source_path, data_path)

    def search(self, search_terms, count=5, formatter=None):
        """
        Query the search index and return an array of text output showing highlghted matches.
        """
        parser = QueryParser("content", schema=self.ix.schema)
        query = parser.parse(' '.join(search_terms))

        count = int(count)

        if not formatter:
            formatter = self.markdown_formatter

        with self.ix.index.searcher() as searcher:
            results = searcher.search(query)
            results.fragmenter.maxchars = 300
            results.fragmenter.surround = 50
            return formatter(search_terms, results, count)

    def markdown_formatter(self, search_terms, results, count):
        """
        Prepare an array of text output fromm a result set.
        """
        if len(results) < count:
            count = len(results)

        if count == 0:
            yield f"Your query {search_terms} yielded no results."
            return

        yield f"Your query {search_terms} yielded {count} results. Showing the top {count}:"

        for result in results[:count]:
            text = result.highlights("content", top=2)
            text = re.sub(r'<b class=".+?">', '<b>', text)
            text = html2markdown.convert(text)

            yield result['title'] + '\n' + textwrap.indent(textwrap.fill(f'...{text}...', width=120), prefix='    ')
