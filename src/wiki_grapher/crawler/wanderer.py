"""wanderer.py — Random-sampling Wikipedia crawler.

At each hop the Wanderer draws a random subset of related pages rather than
following a fixed chain, producing a broader, more exploratory graph.
"""

import logging
import random

from wiki_grapher.crawler.base import WikiGraphBase
from wiki_grapher.constants.constants import DEFAULT_LIMIT_V2


logger = logging.getLogger(__name__)


class Wanderer(WikiGraphBase):
    """Random-sampling Wikipedia crawler.

    At each hop ``wiki_rel`` fetches all related pages for the current title,
    draws a random sample of up to *limit* titles, stores them in ``dict_set``,
    then returns one as the next hop — chosen randomly when ``random_seed=0``,
    or as the last item in the sample otherwise.

    Compared to ``Pathfinder``, Wanderer explores a wider neighbourhood
    because the sampled subset is not constrained to the first *limit* items.

    Inherits all shared state and the iteration loop from ``WikiGraphBase``.
    """

    def wiki_rel(self, word, random_seed=0, limit=DEFAULT_LIMIT_V2):
        """Crawl one hop from *word* using a random-sampling strategy.

        Fetches all related pages, draws a random sample of size
        ``min(limit, len(all_pages))``, stores the sample in ``dict_set``
        keyed by *word*, then picks the next hop.

        Args:
            word (str): Current Wikipedia page title.
            random_seed (int): ``0`` to pick the next hop randomly from the
                sample; any other value to pick the last item in the sample.
            limit (int): Maximum sample size per node. Defaults to
                ``DEFAULT_LIMIT_V2``.

        Returns:
            str: Title of the next page to visit. Returns *word* unchanged
                if no related pages are found.
        """
        self.word_set.add(word)

        all_pages = self._fetch_related(word)

        if not all_pages:
            self.dict_set[word] = []
            return word

        sample_size = min(limit, len(all_pages))
        random_sub_list = random.sample(all_pages, sample_size)

        self.dict_set[word] = random_sub_list
        for val in random_sub_list:
            self.word_set.add(val)
        logger.debug(f"Added {len(random_sub_list)} nodes to database for '{word}': {random_sub_list}")

        if random_seed == 0:
            return random.choice(random_sub_list)
        else:
            return random_sub_list[-1]
