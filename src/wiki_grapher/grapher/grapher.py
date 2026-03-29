import matplotlib.pyplot as plt
import networkx as nx

from wiki_grapher.constants.constants import (
    DEFAULT_GRAPH_SIZE,
    DEFAULT_GRAPH_TYPE,
    DEFAULT_NODE_SIZE_MULTIPLIER,
    DEFAULT_LIVE_NODE_SIZE_MULTIPLIER,
    DEFAULT_LIVE_GRAPH_DELAY,
    COLOR_SEED_NODE,
    COLOR_KEY_NODE,
    COLOR_DEFAULT_NODE,
    COLOR_WHITE_NODE,
    OUTPUT_FIGURE_PATH,
)


class Grapher:

    def __init__(self, dict_set=None, word=None, monochrome=False, labels=False,
                 size=DEFAULT_GRAPH_SIZE, gtype=DEFAULT_GRAPH_TYPE):
        self.dict_set = dict_set
        self.word = word
        self.monochrome = monochrome
        self.labels = labels
        self.size = size
        self.gtype = gtype

    def _build_graph(self):
        default_color = COLOR_DEFAULT_NODE if not self.monochrome else COLOR_WHITE_NODE
        g = nx.Graph() if self.gtype == 'graph' else nx.DiGraph()
        g.add_node(self.word, color=COLOR_SEED_NODE if not self.monochrome else COLOR_WHITE_NODE)

        for key in self.dict_set:
            if key != self.word:
                g.add_node(key, color=COLOR_KEY_NODE if not self.monochrome else COLOR_WHITE_NODE)
            for value in self.dict_set[key]:
                g.add_node(value)
                g.add_edge(key, value)

        colored_dict = nx.get_node_attributes(g, 'color')
        color_seq = [colored_dict.get(node, default_color) for node in g.nodes()]
        d = dict(g.degree)
        return g, color_seq, d

    def develop_graph(self):
        print(f"Graph mode : {self.gtype} | {self.size}")

        g, color_seq, d = self._build_graph()

        plt.figure(figsize=(self.size, self.size))
        nx.draw(G=g,
                with_labels=self.labels,
                node_color=color_seq,
                nodelist=d.keys(),
                node_size=[v * DEFAULT_NODE_SIZE_MULTIPLIER for v in d.values()],
                pos=nx.spring_layout(g))

        plt.savefig(OUTPUT_FIGURE_PATH)

    def live_graph(self, delay=DEFAULT_LIVE_GRAPH_DELAY):
        print(f"Graph mode : {self.gtype} | {self.size}")

        with plt.ion():
            plt.figure(figsize=(self.size, self.size))

            for key in self.dict_set:
                g, color_seq, d = self._build_graph()

                plt.clf()
                nx.draw(G=g,
                        with_labels=self.labels,
                        node_color=color_seq,
                        nodelist=d.keys(),
                        node_size=[v * DEFAULT_LIVE_NODE_SIZE_MULTIPLIER for v in d.values()],
                        pos=nx.spring_layout(g))

                plt.pause(delay)
