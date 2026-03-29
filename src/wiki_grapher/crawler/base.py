import json
import random
import time
import requests

from wiki_grapher.constants.constants import (
    WIKIPEDIA_BASE_URL,
    API_TIMEOUT,
    DEFAULT_WORD,
    DEFAULT_ITER_BUDGET,
    DEFAULT_RATE_LIMIT_DELAY,
    DEFAULT_LIMIT,
    DEFAULT_PATIENCE,
)


class WikiGraphBase:

    def __init__(self):
        self.word = DEFAULT_WORD
        self.iter_budget = DEFAULT_ITER_BUDGET
        self.word_set = set()
        self.dict_set = {}
        self.base_url = WIKIPEDIA_BASE_URL

    def set_word(self, word=DEFAULT_WORD):
        self.word = word

    def set_iter_budget(self, iter_budget=DEFAULT_ITER_BUDGET):
        self.iter_budget = iter_budget

    def _fetch_related(self, word):
        """Fetch related pages from Wikipedia API. Returns list of titles."""
        base_rel_url = f"{self.base_url}/{word}"
        try:
            resp = requests.get(base_rel_url, timeout=API_TIMEOUT)
            resp.raise_for_status()
            body = resp.json()
        except (requests.RequestException, ValueError) as e:
            print(f"Failed to fetch '{word}': {e}")
            return []
        return [page['title'] for page in body.get('pages', [])]

    def wiki_rel(self, word, random_seed=0, limit=DEFAULT_LIMIT):
        raise NotImplementedError("Subclasses must implement wiki_rel()")

    def wiki_iter(self, random_seed=0, limit=DEFAULT_LIMIT, patience=DEFAULT_PATIENCE):
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
                    print("Patience exhausted — stopping early.")
                    break
                continue

            next_word = self.wiki_rel(word, random_seed=random_seed, limit=limit)
            remaining_patience = patience  # reset on successful crawl
            word = next_word
            time.sleep(DEFAULT_RATE_LIMIT_DELAY)
            print(f"Iteration {iteration + 1} done")

    def display(self):
        print(json.dumps(self.dict_set, indent=4))
