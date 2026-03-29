"""base.py — Abstract base class for Wiki-Grapher crawlers.

Defines the shared state, Wikipedia API fetching logic, and the main
iteration loop used by all concrete crawler implementations.
"""

import json
import logging
import random
import time
import requests

logger = logging.getLogger(__name__)

from wiki_grapher.constants.constants import (
    WIKIPEDIA_BASE_URL,
    API_TIMEOUT,
    API_USER_AGENT,
    DEFAULT_WORD,
    DEFAULT_ITER_BUDGET,
    DEFAULT_RATE_LIMIT_DELAY,
    DEFAULT_LIMIT,
    DEFAULT_PATIENCE,
)


class WikiGraphBase:
    """Base class for Wikipedia graph crawlers.

    Manages shared crawler state (visited words, adjacency mapping, budget)
    and provides the core iteration loop ``wiki_iter``. Subclasses must
    implement ``wiki_rel`` to define their traversal strategy.

    Attributes:
        word (str): The current / starting Wikipedia page title.
        iter_budget (int): Maximum number of crawl iterations to perform.
        word_set (set): All page titles discovered during crawling.
        dict_set (dict): Adjacency map ``{page_title: [related_titles]}``.
        base_url (str): Wikipedia REST API base URL.
    """

    def __init__(self):
        """Initialise crawler with default constants."""
        self.word = DEFAULT_WORD
        self.iter_budget = DEFAULT_ITER_BUDGET
        self.word_set = set()
        self.dict_set = {}
        self.base_url = WIKIPEDIA_BASE_URL

    def set_word(self, word=DEFAULT_WORD):
        """Set the seed Wikipedia page title.

        Args:
            word (str): Wikipedia page title to start crawling from.
                Defaults to ``DEFAULT_WORD``.
        """
        self.word = word

    def set_iter_budget(self, iter_budget=DEFAULT_ITER_BUDGET):
        """Set the maximum number of crawl iterations.

        Args:
            iter_budget (int): Upper bound on iterations. Defaults to
                ``DEFAULT_ITER_BUDGET``.
        """
        self.iter_budget = iter_budget

    def _fetch_related(self, word):
        """Fetch related pages for *word* from the Wikipedia REST API.

        Args:
            word (str): Wikipedia page title to look up.

        Returns:
            list[str]: Titles of related pages, or an empty list on failure.
        """
        base_rel_url = f"{self.base_url}/{word}"
        try:
            resp = requests.get(base_rel_url, timeout=API_TIMEOUT, headers={"User-Agent": API_USER_AGENT})
            resp.raise_for_status()
            body = resp.json()
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Failed to fetch '{word}': {e}")
            return []
        return [page['title'] for page in body.get('pages', [])]

    def wiki_rel(self, word, random_seed=0, limit=DEFAULT_LIMIT):
        """Crawl one hop from *word* and return the next page title.

        Subclasses must override this method to implement their specific
        traversal strategy (e.g. sequential, random-sample).

        Args:
            word (str): Current Wikipedia page title.
            random_seed (int): ``0`` for random next-hop selection,
                any other value for deterministic selection.
            limit (int): Maximum number of related pages to consider.

        Returns:
            str: Title of the next page to visit.

        Raises:
            NotImplementedError: Always, unless overridden by a subclass.
        """
        raise NotImplementedError("Subclasses must implement wiki_rel()")

    def wiki_iter(self, random_seed=0, limit=DEFAULT_LIMIT, patience=DEFAULT_PATIENCE):
        """Run the main crawl loop up to ``iter_budget`` iterations.

        At each iteration the crawler calls ``wiki_rel`` on the current page.
        If the page has already been visited, the loop picks an unvisited page
        from ``word_set`` at random. When no unvisited pages remain, the
        patience counters decrements; once exhausted, the loop stops early.

        Args:
            random_seed (int): Passed through to ``wiki_rel`` to control
                next-hop selection. ``0`` = random, other = deterministic.
            limit (int): Maximum related pages per hop. Defaults to
                ``DEFAULT_LIMIT``.
            patience (int): Consecutive stuck iterations are allowed before
                stopping early. Defaults to ``DEFAULT_PATIENCE``.
        """
        word = self.word
        remaining_patience = patience

        for iteration in range(self.iter_budget):
            if word in self.dict_set:
                unvisited = [w for w in self.word_set if w not in self.dict_set]
                if unvisited:
                    word = random.choice(unvisited)
                    continue
                remaining_patience -= 1
                if remaining_patience == 0:
                    logger.warning("Patience exhausted — stopping early.")
                    break
                continue

            next_word = self.wiki_rel(word, random_seed=random_seed, limit=limit)
            remaining_patience = patience  # reset on successful crawl
            word = next_word
            time.sleep(DEFAULT_RATE_LIMIT_DELAY)
            logger.info(f"Iteration {iteration + 1} done")

    def display(self):
        """Pretty-print the adjacency map ``dict_set`` as formatted JSON."""
        logger.debug(json.dumps(self.dict_set, indent=4))
