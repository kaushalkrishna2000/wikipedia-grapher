import random

from wiki_grapher.crawler.base import WikiGraphBase
from wiki_grapher.constants.constants import DEFAULT_LIMIT_V2


class Wanderer(WikiGraphBase):
    """Random-sampling crawler — at each hop samples a random subset of related
    pages and drifts through topics unpredictably."""

    def wiki_rel(self, word, random_seed=0, limit=DEFAULT_LIMIT_V2):
        self.word_set.add(word)

        all_pages = self._fetch_related(word)

        if not all_pages:
            return word

        sample_size = min(limit, len(all_pages))
        random_sub_list = random.sample(all_pages, sample_size)

        self.dict_set[word] = random_sub_list
        for val in random_sub_list:
            self.word_set.add(val)

        if random_seed == 0:
            return random.choice(random_sub_list)
        else:
            return random_sub_list[-1]
