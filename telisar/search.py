from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.qparser import MultifieldParser

import yaml
import textwrap
import html2markdown
import os
import re


class Indexer:
    """
    Create or update the search index.
    """
    schema = Schema(
        path=ID(stored=True),
        title=TEXT(stored=True, field_boost=3.0),
        content=TEXT(stored=True),
        tags=KEYWORD(stored=True, lowercase=True, field_boost=2.0),
    )

    def __init__(self, source_path, data_path):
        self._index = None
        self._writer = None
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

    def parse_hugo_article(self, path):
        in_metadata = False
        metadata = ''
        content = ''
        with open(path) as fh:
            for line in fh:
                if line == '---\n':
                    in_metadata = not in_metadata
                    continue
                if in_metadata:
                    metadata = metadata + line
                else:
                    content = content + line
        doc = yaml.safe_load(metadata)
        doc['path'] = path
        doc['content'] = content
        doc = {k: doc[k] for (k, v) in self.schema.items()}
        return doc

    def build(self, index):
        with self.index.writer() as w:
            for root, dirs, files in os.walk(self._source_path):
                for filename in files:
                    path = os.path.join(root, filename)
                    print(path)
                    w.add_document(**self.parse_hugo_article(path))


class Searcher:
    """
    Search the index.
    """

    def __init__(self, source_path, data_path):
        self._ix = Indexer(source_path, data_path)

    def build(self):
        self._ix.build(self._ix.index)

    def search(self, search_terms, count=5, formatter=None):
        """
        Query the search index and return an array of text output showing highlghted matches.
        """
        parser = MultifieldParser(["title", "tags", "content"], schema=self._ix.schema)
        query = parser.parse(' '.join(search_terms))

        count = int(count)

        if not formatter:
            formatter = Searcher._markdown_formatter

        with self._ix.index.searcher() as searcher:
            results = searcher.search(query)
            results.fragmenter.maxchars = 300
            results.fragmenter.surround = 50
            return formatter(search_terms, results, count)

    @staticmethod
    def _markdown_formatter(search_terms, results, count):
        """
        Prepare an array of text output fromm a result set.
        """
        if len(results) < count:
            count = len(results)

        if count == 0:
            return [f"Your query {search_terms} yielded no results."]

        output = [f"Your query {search_terms} yielded {count} results. Showing the top {count}:"]

        for result in results[:count]:
            text = result.highlights("content", top=2)
            text = re.sub(r'<b class=".+?">', '<b>', text)
            text = html2markdown.convert(text)

            output.append(result['title'] + '\n' +
                          textwrap.indent(textwrap.fill(f'...{text}...', width=120), prefix='    '))

        return output
