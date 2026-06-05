"""
graph_engine.py — Implementasi Graph berbasis Adjacency List
Algoritma: Dijkstra, BFS, Degree Centrality, Multi-Stop Planning
"""

import heapq
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Optional


class Graph:
    """
    Weighted Undirected Graph menggunakan Adjacency List.
    Setiap edge menyimpan atribut: distance_km, time_minutes,
    transport_cost, dan combined_score (dinormalisasi).
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        # adjacency_list[node_id] = list of edge dicts
        self.adjacency_list: Dict[str, List[dict]] = defaultdict(list)
        self.nodes: Dict[str, dict] = {}

    # ─────────────────────────────────────────────
    # Graph Construction
    # ─────────────────────────────────────────────

    def add_node(self, node_id: str, **attributes):
        """Tambah node dengan atribut bebas."""
        self.nodes[node_id] = attributes
        if node_id not in self.adjacency_list:
            self.adjacency_list[node_id] = []

    def add_edge(self, from_node: str, to_node: str, **attributes):
        """Tambah edge dengan atribut (distance_km, time_minutes, transport_cost, dll)."""
        edge_fw = {"to": to_node, **attributes}
        self.adjacency_list[from_node].append(edge_fw)

        if not self.directed:
            edge_bw = {"to": from_node, **attributes}
            self.adjacency_list[to_node].append(edge_bw)

    def compute_combined_scores(self):
        """
        Normalisasi & hitung combined_score untuk setiap edge.
        combined_score = 0.4*time + 0.3*distance + 0.3*cost  (semua dinormalisasi 0-1)
        Dipanggil sekali setelah semua edge ditambahkan.
        """
        all_edges = [e for edges in self.adjacency_list.values() for e in edges]
        if not all_edges:
            return

        max_dist = max((e.get("distance_km", 0) for e in all_edges), default=1) or 1
        max_time = max((e.get("time_minutes", 0) for e in all_edges), default=1) or 1
        max_cost = max((e.get("transport_cost", 0) for e in all_edges), default=1) or 1

        for edges in self.adjacency_list.values():
            for edge in edges:
                score = (
                    0.4 * edge.get("time_minutes", 0) / max_time
                    + 0.3 * edge.get("distance_km", 0) / max_dist
                    + 0.3 * edge.get("transport_cost", 0) / max_cost
                )
                edge["combined_score"] = round(score * 100, 4)  # skala 0–100

    # ─────────────────────────────────────────────
    # Algoritma Utama 1: Dijkstra
    # ─────────────────────────────────────────────

    def dijkstra(
        self,
        start: str,
        end: str,
        weight_attr: str = "distance_km",
    ) -> Tuple[float, List[str], List[dict]]:
        """
        Dijkstra's Algorithm — cari jalur terpendek/tercepat/termurah.

        Parameters
        ----------
        start, end   : node ID asal dan tujuan
        weight_attr  : atribut edge yang dipakai sebagai bobot
                       ('distance_km' | 'time_minutes' | 'transport_cost' | 'combined_score')

        Returns
        -------
        (total_weight, path_ids, steps)
            total_weight : total bobot jalur terpilih
            path_ids     : list node ID dari start ke end
            steps        : list dict tiap iterasi untuk tampilkan proses
        """
        if start not in self.nodes or end not in self.nodes:
            return float("inf"), [], []

        dist = {n: float("inf") for n in self.nodes}
        dist[start] = 0
        prev: Dict[str, Optional[str]] = {n: None for n in self.nodes}
        visited: set = set()
        pq = [(0.0, start)]
        steps: List[dict] = []

        while pq:
            curr_d, curr = heapq.heappop(pq)

            if curr in visited:
                continue
            visited.add(curr)

            # Simpan step untuk visualisasi proses
            steps.append(
                {
                    "visiting": curr,
                    "cost_so_far": round(curr_d, 2),
                    "visited_count": len(visited),
                }
            )

            if curr == end:
                break

            for edge in self.adjacency_list[curr]:
                nbr = edge["to"]
                if nbr in visited:
                    continue
                w = edge.get(weight_attr, 0)
                new_d = curr_d + w
                if new_d < dist[nbr]:
                    dist[nbr] = new_d
                    prev[nbr] = curr
                    heapq.heappush(pq, (new_d, nbr))

        # Rekonstruksi jalur
        path: List[str] = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()

        if not path or path[0] != start:
            return float("inf"), [], steps

        return round(dist[end], 2), path, steps

    # ─────────────────────────────────────────────
    # Algoritma Pendukung 2: BFS
    # ─────────────────────────────────────────────

    def bfs(self, start: str) -> List[str]:
        """
        Breadth-First Search dari node start.
        Mengembalikan urutan node yang dikunjungi.
        """
        if start not in self.nodes:
            return []
        visited = set([start])
        queue = deque([start])
        order: List[str] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for edge in sorted(self.adjacency_list[node], key=lambda e: e["to"]):
                nbr = edge["to"]
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)
        return order

    def bfs_reachable_within(self, start: str, max_cost: float, weight_attr: str = "transport_cost") -> List[str]:
        """BFS khusus: kembalikan semua node yang bisa dicapai dalam batas biaya/waktu/jarak."""
        if start not in self.nodes:
            return []
        visited = {start: 0.0}
        queue = deque([(start, 0.0)])
        reachable = [start]

        while queue:
            node, curr_cost = queue.popleft()
            for edge in self.adjacency_list[node]:
                nbr = edge["to"]
                new_cost = curr_cost + edge.get(weight_attr, 0)
                if new_cost <= max_cost and (nbr not in visited or new_cost < visited[nbr]):
                    visited[nbr] = new_cost
                    reachable.append(nbr)
                    queue.append((nbr, new_cost))

        return list(set(reachable))

    # ─────────────────────────────────────────────
    # Algoritma Analitik 3: Degree Centrality
    # ─────────────────────────────────────────────

    def degree_centrality(self) -> Dict[str, float]:
        """
        Hitung degree centrality tiap node.
        centrality[v] = degree(v) / (N - 1)
        Nilai tinggi = node "hub" yang paling terhubung.
        """
        n = len(self.nodes)
        if n <= 1:
            return {node: 0.0 for node in self.nodes}

        result = {}
        for node in self.nodes:
            # Undirected: degree = jumlah tetangga unik
            neighbors = set(e["to"] for e in self.adjacency_list[node])
            result[node] = round(len(neighbors) / (n - 1), 4)

        return result

    # ─────────────────────────────────────────────
    # Utility: Detail Jalur
    # ─────────────────────────────────────────────

    def path_details(self, path: List[str]) -> dict:
        """
        Hitung akumulasi jarak, waktu, biaya transport, dan tiket masuk
        untuk satu jalur (list node ID).
        """
        total_dist = 0.0
        total_time = 0
        total_transport = 0
        total_entry = 0
        leg_details = []

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge = self._find_edge(u, v)
            if edge:
                d = edge.get("distance_km", 0)
                t = edge.get("time_minutes", 0)
                c = edge.get("transport_cost", 0)
                total_dist += d
                total_time += t
                total_transport += c
                leg_details.append(
                    {
                        "from": u,
                        "from_name": self.nodes[u].get("name", u),
                        "to": v,
                        "to_name": self.nodes[v].get("name", v),
                        "distance_km": d,
                        "time_minutes": t,
                        "transport_cost": c,
                    }
                )

        for node_id in path:
            total_entry += self.nodes[node_id].get("entry_fee", 0)

        return {
            "total_distance_km": round(total_dist, 2),
            "total_time_minutes": total_time,
            "total_transport_cost": total_transport,
            "total_entry_fee": total_entry,
            "total_cost": total_transport + total_entry,
            "legs": leg_details,
        }

    def _find_edge(self, from_node: str, to_node: str) -> Optional[dict]:
        """Cari edge antara dua node."""
        for edge in self.adjacency_list.get(from_node, []):
            if edge["to"] == to_node:
                return edge
        return None

    # ─────────────────────────────────────────────
    # DSS: Multi-Stop Planning
    # ─────────────────────────────────────────────

    def plan_multi_stop(
        self,
        start: str,
        candidate_nodes: List[str],
        max_total_cost: float,
        weight_attr: str = "transport_cost",
    ) -> Tuple[List[str], dict]:
        """
        Greedy multi-stop planner: pilih urutan destinasi terbaik
        dari candidate_nodes mulai dari start, tanpa melebihi max_total_cost.

        Returns (ordered_path, total_details)
        """
        remaining = list(candidate_nodes)
        if start in remaining:
            remaining.remove(start)

        route = [start]
        total_cost = 0.0

        while remaining:
            best_next = None
            best_w = float("inf")

            for candidate in remaining:
                _, path, _ = self.dijkstra(route[-1], candidate, weight_attr)
                if not path:
                    continue
                details = self.path_details(path)
                w = details.get("total_cost", float("inf"))
                if w < best_w and (total_cost + w) <= max_total_cost:
                    best_w = w
                    best_next = candidate

            if best_next is None:
                break  # tidak ada lagi yang terjangkau

            _, seg_path, _ = self.dijkstra(route[-1], best_next, weight_attr)
            # Append tanpa duplikat node terakhir
            route += seg_path[1:]
            total_cost += best_w
            remaining.remove(best_next)

        return route, self.path_details(route)

    # ─────────────────────────────────────────────
    # Info helpers
    # ─────────────────────────────────────────────

    def get_neighbors(self, node_id: str) -> List[dict]:
        """Kembalikan list edge dari node ini."""
        return self.adjacency_list.get(node_id, [])

    def node_count(self) -> int:
        return len(self.nodes)

    def edge_count(self) -> int:
        """Jumlah edge unik (untuk undirected dibagi 2)."""
        total = sum(len(edges) for edges in self.adjacency_list.values())
        return total if self.directed else total // 2

    def summary(self) -> dict:
        """Statistik ringkas graph."""
        return {
            "nodes": self.node_count(),
            "edges": self.edge_count(),
            "directed": self.directed,
            "avg_degree": round(
                sum(len(e) for e in self.adjacency_list.values()) / max(self.node_count(), 1),
                2,
            ),
        }
