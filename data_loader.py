"""
data_loader.py — Muat dataset JSON dan bangun Graph.
"""

import json
import os
from graph_engine import Graph


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_graph() -> Graph:
    """Muat nodes.json + edges.json, bangun Graph, kembalikan objek Graph."""
    nodes_path = os.path.join(DATA_DIR, "nodes.json")
    edges_path = os.path.join(DATA_DIR, "edges.json")

    with open(nodes_path, encoding="utf-8") as f:
        nodes_data = json.load(f)

    with open(edges_path, encoding="utf-8") as f:
        edges_data = json.load(f)

    graph = Graph(directed=False)

    for node in nodes_data:
        node_id = node.pop("id")
        graph.add_node(node_id, **node)

    for edge in edges_data:
        graph.add_edge(
            edge["from"],
            edge["to"],
            distance_km=edge["distance_km"],
            time_minutes=edge["time_minutes"],
            transport_cost=edge["transport_cost"],
        )

    graph.compute_combined_scores()
    return graph


def get_node_options(graph: Graph, exclude_categories: list = None) -> dict:
    """
    Kembalikan dict {display_name: node_id} untuk dropdown Streamlit.
    exclude_categories: list kategori yang tidak ditampilkan.
    """
    exclude = exclude_categories or []
    options = {}
    for node_id, attrs in graph.nodes.items():
        if attrs.get("category") in exclude:
            continue
        icon = attrs.get("icon", "📍")
        name = attrs.get("name", node_id)
        display = f"{icon} {name}"
        options[display] = node_id
    return options


def get_categories(graph: Graph) -> list:
    """Daftar kategori unik yang ada di graph."""
    cats = set(attrs.get("category", "other") for attrs in graph.nodes.values())
    cats.discard("transport")
    return sorted(cats)


CATEGORY_LABELS = {
    "beach":   "🏖️ Pantai",
    "temple":  "🛕 Pura & Budaya",
    "nature":  "🌿 Alam & Petualangan",
    "culture": "🎨 Seni & Budaya",
    "transport": "✈️ Transportasi",
    "club":     "🪩 Club",
}

WEIGHT_OPTIONS = {
    "Jarak Terdekat (km)":         "distance_km",
    "Waktu Tercepat (menit)":      "time_minutes",
    "Biaya Termurah (IDR)":        "transport_cost",
    "Skor Terbaik (Gabungan)":     "combined_score",
}
