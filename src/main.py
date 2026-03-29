import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from wiki_grapher.crawler.pathfinder import Pathfinder
from wiki_grapher.crawler.wanderer import Wanderer
from wiki_grapher.grapher.grapher import Grapher

if __name__ == '__main__':
    print('Hi User')

    # Uncomment the crawler you want to use:
    # - Pathfinder: follows a sequential / random-choice chain of related pages
    # - Wanderer: randomly samples a subset of related pages at each hop
    wiki_obj = Pathfinder()
    # wiki_obj = Wanderer()

    wiki_obj.set_word("Shah_Rukh_Khan")
    wiki_obj.set_iter_budget(iter_budget=240)
    wiki_obj.wiki_iter(random_seed=0, limit=3, patience=5)

    g = Grapher(dict_set=wiki_obj.dict_set,
                word=wiki_obj.word,
                monochrome=False,
                labels=False,
                size=40)

    # Uncomment if you want a live graph; delay is in seconds.
    # g.live_graph(delay=2)
    g.develop_graph()
