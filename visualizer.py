"""
visualizer.py — Visualisasi Graph menggunakan Plotly.
Dua mode: Geographic (lat/lon asli) dan Abstract (spring layout via networkx).
"""

import plotly.graph_objects as go
from typing import List, Optional
from graph_engine import Graph

# ── Palet warna per kategori ──────────────────────────────────────────────
CATEGORY_COLORS = {
    "beach":     "#2196F3",   # biru laut
    "temple":    "#FF9800",   # emas pura
    "nature":    "#4CAF50",   # hijau alam
    "culture":   "#9C27B0",   # ungu seni
    "transport": "#607D8B",   # abu bandara
}
CATEGORY_SIZES = {
    "beach": 22, "temple": 22, "nature": 20,
    "culture": 24, "transport": 18,
}
PATH_COLOR   = "#E53935"   # merah rute dipilih
EDGE_COLOR   = "rgba(120,120,120,0.35)"
HLIGHT_COLOR = "#FF5722"


def _get_positions(graph: Graph, mode: str = "geo") -> dict:
    """
    mode='geo'      : pakai lat/lon (koordinat Bali sesungguhnya)
    mode='abstract' : pakai spring layout networkx
    """
    if mode == "geo":
        pos = {}
        for nid, attrs in graph.nodes.items():
            # Plotly: x = lon, y = lat
            pos[nid] = (attrs.get("lon", 115.2), attrs.get("lat", -8.6))
        return pos
    else:
        try:
            import networkx as nx
            G = nx.Graph()
            for nid in graph.nodes:
                G.add_node(nid)
            for nid, edges in graph.adjacency_list.items():
                for e in edges:
                    G.add_edge(nid, e["to"])
            raw = nx.spring_layout(G, seed=42, k=0.5)
            return {n: (xy[0], xy[1]) for n, xy in raw.items()}
        except ImportError:
            return _get_positions(graph, mode="geo")


def build_graph_figure(
    graph: Graph,
    highlight_path: Optional[List[str]] = None,
    mode: str = "geo",
    title: str = "Graf Wisata Bali",
) -> go.Figure:
    """
    Bangun figure Plotly dengan semua node & edge.
    highlight_path : list node ID jalur Dijkstra yang akan diwarnai merah.
    """
    pos = _get_positions(graph, mode)
    fig = go.Figure()

    # ── 1. Semua edge (abu, tipis) ──────────────────────────────────────
    highlight_set = set()
    if highlight_path and len(highlight_path) > 1:
        highlight_set = set(zip(highlight_path, highlight_path[1:]))

    for nid, edges in graph.adjacency_list.items():
        x0, y0 = pos.get(nid, (0, 0))
        for edge in edges:
            nbr = edge["to"]
            # Hindari duplikat (undirected)
            if nid > nbr:
                continue
            x1, y1 = pos.get(nbr, (0, 0))
            is_path_edge = (nid, nbr) in highlight_set or (nbr, nid) in highlight_set
            if is_path_edge:
                continue  # Gambar terpisah agar ada di atas

            hover = (
                f"<b>{graph.nodes[nid]['name']} → {graph.nodes[nbr]['name']}</b><br>"
                f"📏 {edge.get('distance_km', '?')} km<br>"
                f"⏱️ {edge.get('time_minutes', '?')} mnt<br>"
                f"💰 Rp {edge.get('transport_cost', 0):,}"
            ).replace(",", ".")

            fig.add_trace(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode="lines",
                    line=dict(color=EDGE_COLOR, width=1.5),
                    hoverinfo="text",
                    hovertext=hover,
                    showlegend=False,
                )
            )

    # ── 2. Highlighted path (merah, tebal) ─────────────────────────────
    if highlight_path and len(highlight_path) > 1:
        hx, hy = [], []
        for nid in highlight_path:
            x, y = pos.get(nid, (0, 0))
            hx.append(x)
            hy.append(y)
            hx.append(None)
            hy.append(None)

        # Path lines
        fig.add_trace(
            go.Scatter(
                x=hx, y=hy,
                mode="lines",
                line=dict(color=PATH_COLOR, width=4, dash="solid"),
                name="Rute Optimal",
                hoverinfo="skip",
            )
        )

        # Arrow dots at each stop
        for i, nid in enumerate(highlight_path):
            x, y = pos.get(nid, (0, 0))
            fig.add_trace(
                go.Scatter(
                    x=[x], y=[y],
                    mode="markers+text",
                    marker=dict(symbol="circle", size=16, color=HLIGHT_COLOR,
                                line=dict(color="white", width=2)),
                    text=[str(i + 1)],
                    textfont=dict(color="white", size=10, family="Arial Black"),
                    textposition="middle center",
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    # ── 3. Semua node ──────────────────────────────────────────────────
    categories = list(CATEGORY_COLORS.keys())
    for cat in categories:
        cat_nodes = {nid: attrs for nid, attrs in graph.nodes.items()
                     if attrs.get("category") == cat}
        if not cat_nodes:
            continue

        xs, ys, texts, hovers = [], [], [], []
        for nid, attrs in cat_nodes.items():
            x, y = pos.get(nid, (0, 0))
            xs.append(x)
            ys.append(y)
            texts.append(attrs.get("name", nid))

            neighbors = [e["to"] for e in graph.adjacency_list.get(nid, [])]
            n_names = ", ".join(graph.nodes[n].get("name", n) for n in neighbors[:4])
            hovers.append(
                f"<b>{attrs.get('icon','')} {attrs.get('name', nid)}</b><br>"
                f"⭐ Rating: {attrs.get('rating', '?')}/5<br>"
                f"🎟️ Tiket: Rp {attrs.get('entry_fee', 0):,}<br>"
                f"⏰ Durasi: {attrs.get('duration_hours', '?')} jam<br>"
                f"🔗 Terhubung ke: {n_names or '-'}<br>"
                f"<i>{attrs.get('description', '')[:80]}...</i>"
            )

        label_position = "top center" if cat != "transport" else "bottom center"
        fig.add_trace(
            go.Scatter(
                x=xs, y=ys,
                mode="markers+text",
                marker=dict(
                    size=CATEGORY_SIZES.get(cat, 20),
                    color=CATEGORY_COLORS[cat],
                    line=dict(color="white", width=2),
                    symbol="circle",
                ),
                text=texts,
                textposition=label_position,
                textfont=dict(size=9, color="#1a1a2e"),
                name=_cat_label(cat),
                hoverinfo="text",
                hovertext=hovers,
            )
        )

    # ── 4. Layout ──────────────────────────────────────────────────────
    _apply_layout(fig, mode, title)
    return fig


def _cat_label(cat: str) -> str:
    labels = {
        "beach": "🏖️ Pantai", "temple": "🛕 Pura",
        "nature": "🌿 Alam", "culture": "🎨 Budaya",
        "transport": "✈️ Transport",
    }
    return labels.get(cat, cat.capitalize())


def _apply_layout(fig: go.Figure, mode: str, title: str):
    axis_common = dict(showgrid=False, zeroline=False, showticklabels=False)
    if mode == "geo":
        x_range = [114.95, 115.70]
        y_range = [-8.95, -8.15]
        x_title = "Longitude"
        y_title = "Latitude"
    else:
        x_range = None
        y_range = None
        x_title = ""
        y_title = ""

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="#1a1a2e"), x=0.5),
        paper_bgcolor="#f0f4f8",
        plot_bgcolor="#e8f4f8",
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="right", x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray", borderwidth=1,
        ),
        xaxis=dict(**axis_common, title=x_title, range=x_range),
        yaxis=dict(**axis_common, title=y_title, range=y_range),
        hovermode="closest",
        height=560,
    )


# ── Centrality Bar Chart ──────────────────────────────────────────────────
def build_centrality_chart(centrality: dict, graph_nodes: dict) -> go.Figure:
    sorted_items = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    names  = [f"{graph_nodes[k].get('icon','')} {graph_nodes[k].get('name', k)}"
              for k, _ in sorted_items]
    values = [v for _, v in sorted_items]
    colors = [CATEGORY_COLORS.get(graph_nodes[k].get("category", ""), "#90A4AE")
              for k, _ in sorted_items]

    fig = go.Figure(
        go.Bar(
            x=values, y=names,
            orientation="h",
            marker=dict(color=colors, line=dict(color="white", width=0.5)),
            text=[f"{v:.3f}" for v in values],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Centrality: %{x:.4f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="📊 Degree Centrality — Node Terpenting dalam Graf",
        xaxis_title="Degree Centrality",
        yaxis=dict(autorange="reversed"),
        paper_bgcolor="#f0f4f8",
        plot_bgcolor="#f0f4f8",
        margin=dict(l=180, r=80, t=50, b=40),
        height=480,
    )
    return fig


# ── BFS Traversal Chart ───────────────────────────────────────────────────
def build_bfs_chart(bfs_order: list, graph_nodes: dict) -> go.Figure:
    names  = [f"{graph_nodes[n].get('icon','')} {graph_nodes[n].get('name', n)}"
              for n in bfs_order if n in graph_nodes]
    levels = list(range(1, len(names) + 1))

    fig = go.Figure(
        go.Bar(
            x=levels, y=names,
            orientation="h",
            marker=dict(
                color=levels,
                colorscale="Teal",
                showscale=True,
                colorbar=dict(title="Urutan BFS"),
            ),
            text=[f"Step {l}" for l in levels],
            textposition="inside",
            hovertemplate="<b>%{y}</b><br>Dikunjungi urutan ke-%{x}<extra></extra>",
        )
    )
    fig.update_layout(
        title="🔍 BFS Traversal — Urutan Eksplorasi Graf",
        xaxis_title="Urutan Kunjungan",
        yaxis=dict(autorange="reversed"),
        paper_bgcolor="#f0f4f8",
        plot_bgcolor="#f0f4f8",
        margin=dict(l=180, r=50, t=50, b=40),
        height=480,
    )
    return fig
