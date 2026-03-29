import random

from wiki_grapher.crawler.base import WikiGraphBase
from wiki_grapher.constants.constants import DEFAULT_LIMIT


class Pathfinder(WikiGraphBase):
    """Sequential crawler — at each hop selects a page from the related list,
    either randomly (random_seed=0) or deterministically (last item)."""

    def wiki_rel(self, word, random_seed=0, limit=DEFAULT_LIMIT):
        self.word_set.add(word)

        all_pages = self._fetch_related(word)
        word_list = all_pages[:limit]

        for title in word_list:
            self.word_set.add(title)
        self.dict_set[word] = word_list

        if not word_list:
            return word

        if random_seed == 0:
            return random.choice(word_list)
        else:
            return word_list[-1]
