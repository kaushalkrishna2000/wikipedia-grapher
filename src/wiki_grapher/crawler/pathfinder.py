"""pathfinder.py — Sequential Wikipedia crawler.

At each hop the Pathfinder selects a single page from the related-pages list
(randomly or deterministically) and follows it, building a chain-like graph.
"""

import logging
import random

from wiki_grapher.crawler.base import WikiGraphBase
from wiki_grapher.constants.constants import DEFAULT_LIMIT


logger = logging.getLogger(__name__)


class Pathfinder(WikiGraphBase):
    """Sequential Wikipedia crawler.

    At each hop ``wiki_rel`` fetches the related pages for the current title,
    stores up to *limit* of them in ``dict_set``, then returns one as the next
    hop — chosen randomly when ``random_seed=0``, or as the last item
    otherwise.

    Inherits all shared state and the iteration loop from ``WikiGraphBase``.
    """

    def wiki_rel(self, word, random_seed=0, limit=DEFAULT_LIMIT):
        """Crawl one hop from *word* using a sequential selection strategy.

        Fetches related pages, stores the first *limit* titles in ``dict_set``
        keyed by *word*, then picks the next hop.

        Args:
            word (str): Current Wikipedia page title.
            random_seed (int): ``0`` to pick the next hop randomly from
                *word_list*; any other value to pick the last item.
            limit (int): Maximum number of related pages to store per node.
                Defaults to ``DEFAULT_LIMIT``.

        Returns:
            str: Title of the next page to visit. Returns *word* unchanged
                if no related pages are found.
        """
        self.word_set.add(word)

        all_pages = self._fetch_related(word)
        word_list = all_pages[:limit]

        for title in word_list:
            self.word_set.add(title)
        self.dict_set[word] = word_list
        logger.debug(f"Added {len(word_list)} nodes to database for '{word}': {word_list}")

        if not word_list:
            return word

        if random_seed == 0:
            return random.choice(word_list)
        else:
            return word_list[-1]
