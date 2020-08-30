from telisar import search
from io import StringIO
import pytest


@pytest.fixture
def hugo_article():
    return StringIO("""
---
title: "Episode 63: Madame Elethi's Ledger, Part III"
date: 2020-08-23T19:36:37-07:00
campaigndate: Mimdag, 2nd of the Fox, 3207 ME
tags: ['session', 'vampire']
---

Here is some text.

And here is some more!

""")


def test_parse_hugo_article(hugo_article):
    (metadata, content) = search.Indexer(None, None).parse_hugo_article(hugo_article)
    assert metadata['title'] == "Episode 63: Madame Elethi's Ledger, Part III"
    assert metadata['tags'] == ['session', 'vampire']
