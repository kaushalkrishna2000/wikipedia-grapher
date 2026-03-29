"""constants.py — Project-wide configuration constants for Wiki-Grapher.

Groups:
    - Wikipedia API settings (base URL, timeout).
    - Crawler defaults (word, budget, rate-limit, limits, patience).
    - Grapher defaults (figure size, graph type, node-size multipliers, delays).
    - Node color palette.
    - Output file path.
"""

# Wikipedia API
WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/api/rest_v1/page/related"
API_TIMEOUT = 10  # seconds

# Crawler defaults
DEFAULT_WORD = "Apple"
DEFAULT_ITER_BUDGET = 50
DEFAULT_RATE_LIMIT_DELAY = 0.5  # seconds between API calls
DEFAULT_LIMIT = 10
DEFAULT_LIMIT_V2 = 6
DEFAULT_PATIENCE = 5  # consecutive stuck iterations before stopping early

# Grapher defaults
DEFAULT_GRAPH_SIZE = 50
DEFAULT_GRAPH_TYPE = "graph"
DEFAULT_NODE_SIZE_MULTIPLIER = 150
DEFAULT_LIVE_NODE_SIZE_MULTIPLIER = 50
DEFAULT_LIVE_GRAPH_DELAY = 5  # seconds

# Node colours
COLOR_SEED_NODE = "green"
COLOR_KEY_NODE = "red"
COLOR_DEFAULT_NODE = "blue"
COLOR_WHITE_NODE = "white"

# Output
OUTPUT_FIGURE_PATH = "exploration_map.pdf"
