"""grapher.py — Graph visualisation for Wiki-Grapher crawl results.

Builds a NetworkX graph from the crawler's adjacency map and renders it
either as a static PDF figure or as an animated live plot.
"""

import logging

import matplotlib.pyplot as plt
import networkx as nx

logger = logging.getLogger(__name__)

from wiki_grapher.constants.constants import (
    DEFAULT_GRAPH_SIZE,
    DEFAULT_GRAPH_TYPE,
    DEFAULT_NODE_SIZE_MULTIPLIER,
    DEFAULT_LIVE_NODE_SIZE_MULTIPLIER,
    DEFAULT_LIVE_GRAPH_DELAY,
    COLOR_SEED_NODE,
    COLOR_KEY_NODE,
    COLOR_ACTIVE_NODE,
    COLOR_DEFAULT_NODE,
    COLOR_WHITE_NODE,
    OUTPUT_FIGURE_PATH,
    OUTPUT_HTML_PATH,
)


class Grapher:
    """Visualises a Wikipedia crawl as a NetworkX graph.

    Constructs an undirected (or directed) graph from the adjacency map
    produced by a crawler, colour-codes nodes by role, and renders the
    result either to a static PDF or as a live animated plot.

    Attributes:
        dict_set (dict): Adjacency map ``{page_title: [related_titles]}``
            produced by a crawler.
        word (str): Seed page title; rendered as the green (or white) node.
        monochrome (bool): If ``True``, all nodes are drawn white.
        labels (bool): If ``True``, node labels are shown on the plot.
        size (int): Width and height of the figure in inches.
        gtype (str): ``'graph'`` for undirected, ``'digraph'`` for directed.
    """

    def __init__(self, dict_set=None, word=None, monochrome=False, labels=False,
                 size=DEFAULT_GRAPH_SIZE, gtype=DEFAULT_GRAPH_TYPE):
        """Initialise the Grapher.

        Args:
            dict_set (dict | None): Adjacency map from a crawler.
            word (str | None): Seed page title used to colour the root node.
            monochrome (bool): Render all nodes in white when ``True``.
            labels (bool): Show node labels when ``True``.
            size (int): Figure size in inches (square). Defaults to
                ``DEFAULT_GRAPH_SIZE``.
            gtype (str): Graph type — ``'graph'`` (undirected) or
                ``'digraph'`` (directed). Defaults to ``DEFAULT_GRAPH_TYPE``.
        """
        self.dict_set = dict_set
        self.word = word
        self.monochrome = monochrome
        self.labels = labels
        self.size = size
        self.gtype = gtype

    def _build_graph(self, active_node=None):
        """Build the NetworkX graph and compute per-node colors and degrees.

        The seed node (``self.word``) is colored green, the active node is
        yellow, intermediate key nodes are red, and leaf nodes are blue
        (all white in monochrome mode).

        Args:
            active_node (str | None): The node currently being expanded.

        Returns:
            tuple:
                - **g** (``nx.Graph`` | ``nx.DiGraph``): The constructed graph.
                - **color_seq** (list[str]): Color string for each node in
                  ``g.nodes()`` order.
                - **d** (dict): Mapping of ``{node: degree}``.
        """
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
        color_seq = []
        for node in g.nodes():
            if node == active_node and not self.monochrome:
                color_seq.append(COLOR_ACTIVE_NODE)
            else:
                color_seq.append(colored_dict.get(node, default_color))

        d = dict(g.degree)
        return g, color_seq, d

    def develop_graph(self):
        """Render the graph as a static figure and save it to a PDF.

        Draws the full graph using a spring layout, scales node sizes by
        degree, and writes the output to ``OUTPUT_FIGURE_PATH``.
        """
        logger.info(f"Graph mode : {self.gtype} | {self.size}")

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
        """Render the graph as an animated live plot, updating node by node.

        Iterates over each key in ``dict_set``, rebuilds the graph, and
        redraws the figure with a pause between frames.

        Args:
            delay (float): Seconds to pause between frame updates. Defaults
                to ``DEFAULT_LIVE_GRAPH_DELAY``.
        """
        logger.info(f"Graph mode : {self.gtype} | {self.size}")

        with plt.ion():
            plt.figure(figsize=(self.size, self.size))

            for key in self.dict_set:
                g, color_seq, d = self._build_graph(active_node=key)

                plt.clf()
                plt.title(f"Expanding: {key}")
                nx.draw(G=g,
                        with_labels=self.labels,
                        node_color=color_seq,
                        nodelist=d.keys(),
                        node_size=[v * DEFAULT_LIVE_NODE_SIZE_MULTIPLIER for v in d.values()],
                        pos=nx.spring_layout(g))

                plt.pause(delay)

    def animated_graph(self, delay=DEFAULT_LIVE_GRAPH_DELAY):
        """Render the graph as a structured animation starting from an empty state.

        Sequence:
        1. Empty Window: Opens the plot window with a clear canvas.
        2. Seed Phase: Draws only the seed node (green).
        3. Expansion Phase: Gradually adds neighbors node-by-node from the crawl.

        Args:
            delay (float): Seconds to pause between frame updates. Defaults
                to ``DEFAULT_LIVE_GRAPH_DELAY``.
        """
        logger.info(f"Animated Graph mode starting: {self.gtype} | {self.size}")

        with plt.ion():
            plt.figure(figsize=(self.size, self.size))

            # --- Step 1: Initialise with an empty graph window ---
            plt.clf()
            plt.title("Initialising Crawler...")
            plt.pause(delay)

            # --- Step 2: Draw the seed node first ---
            g_init = nx.Graph() if self.gtype == 'graph' else nx.DiGraph()
            g_init.add_node(self.word)

            plt.clf()
            plt.title(f"Starting Seed: {self.word}")
            nx.draw(G=g_init,
                    with_labels=self.labels,
                    node_color=[COLOR_SEED_NODE if not self.monochrome else COLOR_WHITE_NODE],
                    node_size=[DEFAULT_LIVE_NODE_SIZE_MULTIPLIER],
                    pos={self.word: (0, 0)})
            plt.pause(delay)

            # --- Step 3: Run the incremental update loop ---
            processed_data = {}
            for key, neighbors in self.dict_set.items():
                processed_data[key] = neighbors

                # Use a temporary override to reuse internal building logic
                original_dict = self.dict_set
                self.dict_set = processed_data
                g, color_seq, d = self._build_graph(active_node=key)
                self.dict_set = original_dict

                plt.clf()
                plt.title(f"Expanding: {key}")
                nx.draw(G=g,
                        with_labels=self.labels,
                        node_color=color_seq,
                        nodelist=d.keys(),
                        node_size=[v * DEFAULT_LIVE_NODE_SIZE_MULTIPLIER for v in d.values()],
                        pos=nx.spring_layout(g))

                plt.pause(delay)

    def develop_html_graph(self, filename=OUTPUT_HTML_PATH):
        """Render the graph as an interactive, fluid HTML file using Pyvis.

        Args:
            filename (str): Path to save the HTML output. Defaults to
                ``OUTPUT_HTML_PATH``.
        """
        logger.info(f"HTML Graph mode : {self.gtype} | {self.size}")

        from pyvis.network import Network

        # 1. Build the NetworkX graph from our existing internal logic
        g, color_seq, d = self._build_graph()

        # 2. Initialise Pyvis Network
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=(self.gtype == 'digraph'))

        # 3. Load the NetworkX graph
        net.from_nx(g)

        # 4. Apply colors and sizes from our sequence (matching g.nodes() order)
        for i, node in enumerate(g.nodes()):
            # Use the color calculated in _build_graph
            net.get_node(node)['color'] = color_seq[i]
            # Scale node size for visibility in Pyvis
            net.get_node(node)['size'] = d[node] * 10

        # 5. Save and generate the HTML
        logger.info(f"Saving HTML graph to: {filename}")
        try:
            with open(filename, 'w') as f:
                f.write(net.generate_html())
        except Exception as e:
            logger.error(f"Failed to save HTML graph: {e}")
