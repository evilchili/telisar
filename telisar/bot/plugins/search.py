import os
import re
import discord
import html2markdown

from telisar.bot.plugins.base import Plugin, message_parts
from telisar import search

SOURCE_PATH_VARIABLE = 'WEBSITE_SOURCE_PATH'
DATA_PATH_VARIABLE = 'SEARCH_INDEX_PATH'
WEBSITE_URL = 'https://telisar.evilchi.li/'


class Search(Plugin):
    """
    Search the campaign website.

    search [N] TERM[ TERM TERM...]...Search the website for the specified term(s) and show N responses.

    By default the top 5 results will be displayed.
    """
    command = 'search'
    help_text = 'serach telisar.evilchi.li'

    is_digits = re.compile(r'^\d+$')

    def __init__(self):
        super().__init__()
        self._searcher = None

    def check_config(self):
        src = os.environ.get(SOURCE_PATH_VARIABLE, None)
        data = os.environ.get(DATA_PATH_VARIABLE, None)
        if not (src and data):
            self.logger.error(f"Both {SOURCE_PATH_VARIABLE} and {DATA_PATH_VARIABLE} must be defined.")
            return False
        return True

    @property
    def searcher(self):
        if not self._searcher:
            self._searcher = search.Searcher(
                os.environ.get(SOURCE_PATH_VARIABLE),
                os.environ.get(DATA_PATH_VARIABLE),
            )
        return self._searcher

    def url(self, result):
        slug = result['filename'].split('/')[-1][:-3]
        return f"{WEBSITE_URL}/posts/{slug}"

    def embed_formatter(self, search_terms, results, count):

        if len(results) < count:
            count = len(results)
        if count == 0:
            return f"Query {search_terms} yielded no results."

        output = [f"Query {search_terms} yielded {len(results)} results. Showing the top {count}:"]
        for result in results[:count]:

            text = result.highlights("content", top=2)
            text = re.sub(r'<b class=".+?">', '<b>', text)
            text = html2markdown.convert(text)

            embed = discord.Embed(color=0x883333)
            embed.title = result['title']
            embed.url = self.url(result)
            embed.description = f'...{text}...'
            output.append(embed)
        return output

    def run(self, message):
        (cmd, args) = message_parts(message)

        if len(args) > 1 and self.is_digits.match(args[0]):
            count = args[0]
            args = args[1:]
        else:
            count = 3

        return self.searcher.search(search_terms=args, count=count, formatter=self.embed_formatter)
