"""
app.py — Main Streamlit Application
Bali Tourism Decision Support System (DSS) berbasis Graph
Algoritma: Dijkstra + BFS + Degree Centrality
AI: Gemini API  |  Weather: OpenWeatherMap API
"""

import streamlit as st
import pandas as pd
import time

from graph_engine import Graph
from data_loader import load_graph, get_node_options, get_categories, WEIGHT_OPTIONS, CATEGORY_LABELS
from ai_recommender import get_ai_recommendation
from weather_api import get_bali_weather, weather_recommendation
from visualizer import build_graph_figure, build_centrality_chart, build_bfs_chart

# ─────────────────────────────────────────────
# Page Config & Custom CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bali Tourism DSS",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Font & Base */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    color: white;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] p { color: #e0e0e0 !important; }
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #64b5f6 !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #2196F3;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 8px 18px;
    font-weight: 600;
}

/* Custom cards */
.card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.card-danger  { border-left: 5px solid #E53935; }
.card-success { border-left: 5px solid #43A047; }
.card-info    { border-left: 5px solid #1E88E5; }
.card-warn    { border-left: 5px solid #FB8C00; }

/* Path step */
.step-badge {
    display: inline-block;
    background: #E53935; color: white;
    border-radius: 50%; width: 28px; height: 28px;
    text-align: center; line-height: 28px;
    font-weight: bold; margin-right: 10px;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
    color: white;
    padding: 24px 32px;
    border-radius: 16px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "graph" not in st.session_state:
    st.session_state.graph = load_graph()
if "weather" not in st.session_state:
    st.session_state.weather = get_bali_weather()
if "dijkstra_result" not in st.session_state:
    st.session_state.dijkstra_result = None
if "ai_text" not in st.session_state:
    st.session_state.ai_text = None
if "multi_path" not in st.session_state:
    st.session_state.multi_path = None
if "viz_mode" not in st.session_state:
    st.session_state.viz_mode = "geo"

graph: Graph = st.session_state.graph
weather       = st.session_state.weather


# ─────────────────────────────────────────────
# SIDEBAR — User Preferences
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌴 Bali Tourism DSS")
    st.markdown("*Decision Support System berbasis Graf*")
    st.divider()

    st.markdown("### 👤 Profil Wisatawan")
    user_name   = st.text_input("Nama",   value="Wisatawan", key="u_name")
    user_origin = st.text_input("Asal Kota", value="Denpasar", key="u_origin")

    st.divider()
    st.markdown("### 🎯 Preferensi Wisata")

    # Node options (exclude transport for destination selection)
    all_opts   = get_node_options(graph)
    dest_opts  = get_node_options(graph, exclude_categories=["transport"])

    start_disp  = st.selectbox("✈️ Titik Keberangkatan", list(all_opts.keys()), index=0)
    start_node  = all_opts[start_disp]

    budget      = st.number_input("💰 Budget Total (IDR)", min_value=100_000,
                                   max_value=10_000_000, value=1_500_000, step=50_000)
    duration    = st.slider("⏰ Durasi Tersedia (jam)", 2, 14, 8)

    cat_options = {v: k for k, v in CATEGORY_LABELS.items() if k != "transport"}
    selected_cat_labels = st.multiselect(
        "🏷️ Kategori Favorit",
        list(cat_options.keys()),
        default=list(cat_options.keys())[:3],
    )
    selected_cats = [cat_options[l] for l in selected_cat_labels]

    st.divider()
    st.markdown("### ⚙️ Algoritma")
    weight_label = st.radio(
        "Kriteria Optimasi Dijkstra",
        list(WEIGHT_OPTIONS.keys()),
        index=0,
    )
    weight_attr = WEIGHT_OPTIONS[weight_label]
    max_stops   = st.slider("Maks. Destinasi (Multi-Stop)", 2, 8, 4)

    st.divider()
    run_analysis = st.button("🚀 Analisis & Rekomendasikan", use_container_width=True, type="primary")
    if st.button("🔄 Refresh Cuaca", use_container_width=True):
        st.session_state.weather = get_bali_weather()
        weather = st.session_state.weather


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1 style="margin:0;font-size:2rem;">🌴 Bali Tourism DSS</h1>
  <p style="margin:4px 0 0;opacity:0.8;font-size:1rem;">
    Decision Support System berbasis Graph — Dijkstra + BFS + AI Gemini
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Run Analysis on Button Click
# ─────────────────────────────────────────────
if run_analysis:
    with st.spinner("⚙️ Menjalankan algoritma Dijkstra & analisis graf..."):
        # Filter candidate nodes berdasarkan kategori
        candidates = [
            nid for nid, attrs in graph.nodes.items()
            if attrs.get("category") in selected_cats
        ]
        if not candidates:
            candidates = [n for n in graph.nodes if n != start_node]

        # Multi-stop planning
        route, route_details = graph.plan_multi_stop(
            start=start_node,
            candidate_nodes=candidates[:max_stops],
            max_total_cost=budget,
            weight_attr=weight_attr,
        )

        st.session_state.multi_path = {
            "path": route,
            "details": route_details,
        }

        # Simpan juga untuk tab rute single
        if len(route) >= 2:
            w, path_ids, steps = graph.dijkstra(route[0], route[-1], weight_attr)
            st.session_state.dijkstra_result = {
                "weight": w,
                "path": path_ids,
                "steps": steps,
                "weight_attr": weight_attr,
                "weight_label": weight_label,
                "details": graph.path_details(path_ids),
            }

    # AI recommendation
    with st.spinner("🤖 Meminta rekomendasi dari Gemini AI..."):
        user_profile = {
            "name":               user_name,
            "origin":             user_origin,
            "budget":             budget,
            "duration":           duration,
            "categories":         selected_cat_labels,
            "optimization_label": weight_label,
        }
        path_result_for_ai = st.session_state.multi_path or {}
        st.session_state.ai_text = get_ai_recommendation(
            user_profile, path_result_for_ai, graph.nodes, weather
        )

    st.success("✅ Analisis selesai! Lihat hasil di tab-tab di bawah.")


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard",
    "🗺️ Visualisasi Graf",
    "🔍 Pencarian Rute",
    "🤖 Rekomendasi AI",
    "📊 Analisis Graf",
])


# ══════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════
with tab1:
    # Metric row 1 — Graph stats
    g_summary = graph.summary()
    centrality = graph.degree_centrality()
    top_hub    = max(centrality, key=centrality.get)
    top_hub_name = graph.nodes[top_hub].get("name", top_hub)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📍 Total Node",   g_summary["nodes"])
    col2.metric("🔗 Total Edge",   g_summary["edges"])
    col3.metric("📐 Rata-rata Degree", g_summary["avg_degree"])
    col4.metric("⭐ Hub Utama",    top_hub_name)
    avg_rating = round(
        sum(a.get("rating", 0) for a in graph.nodes.values()) / len(graph.nodes), 2
    )
    col5.metric("⭐ Avg Rating",   avg_rating)

    st.divider()

    # Weather card + info
    col_w, col_info = st.columns([1, 2])
    with col_w:
        st.markdown("### 🌤️ Cuaca Bali Saat Ini")
        wicon = weather.get("icon", "🌡️")
        temp  = weather.get("temp", "?")
        hum   = weather.get("humidity", "?")
        cond  = weather.get("condition", "?")
        wind  = weather.get("wind_kmh", "?")
        src   = weather.get("source", "mock")
        badge = "🔴 Mock" if src == "mock" else "🟢 Live"

        st.markdown(f"""
        <div class="card card-info">
          <h1 style="margin:0;text-align:center;font-size:3rem;">{wicon}</h1>
          <h3 style="text-align:center;margin:4px 0;">{cond}</h3>
          <p style="text-align:center;color:#555;margin:0;">
            🌡️ {temp}°C &nbsp;|&nbsp; 💧 {hum}% &nbsp;|&nbsp; 💨 {wind} km/h
          </p>
          <p style="text-align:center;margin-top:8px;font-size:0.8rem;color:#888;">
            Sumber: {badge} &nbsp;|&nbsp; {weather.get('fetched_at','')}
          </p>
        </div>
        """, unsafe_allow_html=True)

        outdoor = weather.get("outdoor_suitable", True)
        if outdoor:
            st.success("✅ Kondisi bagus untuk wisata outdoor!")
        else:
            st.warning("⚠️ " + weather_recommendation(weather))

    with col_info:
        st.markdown("### 📋 Semua Destinasi")
        node_rows = []
        for nid, attrs in graph.nodes.items():
            if attrs.get("category") == "transport":
                continue
            deg = graph.degree_centrality().get(nid, 0)
            node_rows.append({
                "Ikon": attrs.get("icon", "📍"),
                "Nama": attrs.get("name", nid),
                "Kategori": CATEGORY_LABELS.get(attrs.get("category",""), attrs.get("category","")),
                "Rating": f"{'⭐' * int(attrs.get('rating',0))} {attrs.get('rating','')}",
                "Tiket (IDR)": f"Rp {attrs.get('entry_fee', 0):,}".replace(",","."),
                "Durasi": f"{attrs.get('duration_hours','?')} jam",
                "Centrality": f"{deg:.3f}",
            })
        df = pd.DataFrame(node_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Multi-path result summary if exists
    if st.session_state.multi_path:
        st.divider()
        st.markdown("### 🗺️ Hasil Rute Multi-Stop Terakhir")
        mp = st.session_state.multi_path
        path_ids = mp["path"]
        path_names = [
            f"{graph.nodes[n].get('icon','📍')} {graph.nodes[n].get('name', n)}"
            for n in path_ids if n in graph.nodes
        ]
        st.markdown(" **→** ".join(path_names))
        d = mp["details"]
        ca, cb, cc, cd = st.columns(4)
        ca.metric("📏 Jarak", f"{d['total_distance_km']} km")
        cb.metric("⏱️ Waktu Transport", f"{d['total_time_minutes']} mnt")
        cc.metric("🚗 Biaya Transport", f"Rp {d['total_transport_cost']:,}".replace(",","."))
        cd.metric("🎟️ Tiket Masuk", f"Rp {d['total_entry_fee']:,}".replace(",","."))


# ══════════════════════════════════════════════
# TAB 2 — VISUALISASI GRAF
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### 🗺️ Visualisasi Graf Wisata Bali")

    col_vm, col_ph = st.columns([1, 3])
    with col_vm:
        viz_mode = st.radio("Mode Tampilan", ["🌍 Geografis (Lat/Lon)", "🔵 Abstrak (Spring Layout)"], index=0)
        mode_key = "geo" if "Geografis" in viz_mode else "abstract"
        st.session_state.viz_mode = mode_key

    # Get highlight path from last result
    h_path = None
    if st.session_state.multi_path:
        h_path = st.session_state.multi_path["path"]
    elif st.session_state.dijkstra_result:
        h_path = st.session_state.dijkstra_result["path"]

    with col_ph:
        if h_path:
            path_disp = " → ".join(
                f"{graph.nodes[n].get('icon','')} {graph.nodes[n].get('name',n)}"
                for n in h_path if n in graph.nodes
            )
            st.info(f"🔴 Rute disorot: {path_disp}")

    fig = build_graph_figure(
        graph,
        highlight_path=h_path,
        mode=mode_key,
        title="Graf Destinasi Wisata Bali — Weighted Undirected Graph",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "💡 **Klik node untuk detail** | Merah = rute Dijkstra optimal | "
        "Ukuran titik ∝ kategori destinasi | Warna edge = koneksi antar destinasi"
    )

    # Node detail lookup
    st.divider()
    st.markdown("### 🔎 Detail Node")
    sel_disp = st.selectbox("Pilih destinasi untuk detail:", list(dest_opts.keys()))
    sel_id   = dest_opts[sel_disp]
    attrs    = graph.nodes[sel_id]
    neighbors = graph.get_neighbors(sel_id)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"## {attrs.get('icon','')} {attrs.get('name','')}")
        st.markdown(f"**Kategori:** {CATEGORY_LABELS.get(attrs.get('category',''), '')}")
        st.markdown(f"**Rating:** {'⭐' * int(attrs.get('rating',0))} ({attrs.get('rating')})")
        st.markdown(f"**Tiket Masuk:** Rp {attrs.get('entry_fee', 0):,}".replace(",","."))
        st.markdown(f"**Durasi Ideal:** {attrs.get('duration_hours','?')} jam")
        st.markdown(f"**Waktu Terbaik:** {attrs.get('best_time','?').capitalize()}")
        st.markdown(f"**Degree Centrality:** `{graph.degree_centrality().get(sel_id, 0):.4f}`")

    with c2:
        st.markdown(f"_{attrs.get('description','')}_")
        st.markdown(f"**Aktivitas:** {', '.join(attrs.get('activities', []))}")
        st.markdown(f"💡 **Tips:** {attrs.get('tips','')}")
        st.markdown("**Destinasi Terdekat:**")
        if neighbors:
            nbr_df = pd.DataFrame([
                {
                    "Destinasi": f"{graph.nodes[e['to']].get('icon','')} {graph.nodes[e['to']].get('name', e['to'])}",
                    "Jarak (km)": e.get("distance_km","?"),
                    "Waktu (mnt)": e.get("time_minutes","?"),
                    "Biaya (IDR)": f"Rp {e.get('transport_cost', 0):,}".replace(",","."),
                }
                for e in neighbors if e["to"] in graph.nodes
            ])
            st.dataframe(nbr_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 3 — PENCARIAN RUTE
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### 🔍 Pencarian Rute Optimal — Algoritma Dijkstra")

    col_s, col_e, col_w = st.columns(3)
    with col_s:
        s_disp = st.selectbox("🟢 Titik Awal",    list(all_opts.keys()),  key="route_start")
        s_id   = all_opts[s_disp]
    with col_e:
        e_disp = st.selectbox("🔴 Titik Tujuan",  list(dest_opts.keys()), key="route_end")
        e_id   = dest_opts[e_disp]
    with col_w:
        w_lbl  = st.selectbox("⚙️ Optimasi",      list(WEIGHT_OPTIONS.keys()), key="route_w")
        w_attr = WEIGHT_OPTIONS[w_lbl]

    if st.button("🔎 Cari Rute Dijkstra", use_container_width=True, type="primary"):
        if s_id == e_id:
            st.warning("Titik awal dan tujuan sama!")
        else:
            with st.spinner("Menjalankan Dijkstra..."):
                total_w, path_ids, steps = graph.dijkstra(s_id, e_id, w_attr)

            if not path_ids:
                st.error("❌ Tidak ada jalur yang ditemukan antara kedua node ini.")
            else:
                details = graph.path_details(path_ids)
                st.session_state.dijkstra_result = {
                    "weight": total_w, "path": path_ids, "steps": steps,
                    "weight_attr": w_attr, "weight_label": w_lbl, "details": details,
                }
                st.success(f"✅ Jalur ditemukan! {len(path_ids)} node, {len(steps)} iterasi Dijkstra.")

    res = st.session_state.dijkstra_result
    if res:
        path_ids = res["path"]
        details  = res["details"]

        # Path visualization
        st.markdown("#### 🗺️ Visualisasi Rute")
        route_fig = build_graph_figure(
            graph,
            highlight_path=path_ids,
            mode=st.session_state.viz_mode,
            title=f"Rute Optimal: {graph.nodes[path_ids[0]].get('name','')} → {graph.nodes[path_ids[-1]].get('name','')}",
        )
        st.plotly_chart(route_fig, use_container_width=True)

        # Metrics
        st.markdown("#### 📊 Ringkasan Rute")
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("🏁 Jumlah Stop",   len(path_ids))
        mc2.metric("📏 Jarak",          f"{details['total_distance_km']} km")
        mc3.metric("⏱️ Waktu",          f"{details['total_time_minutes']} mnt")
        mc4.metric("🚗 Transport",       f"Rp {details['total_transport_cost']:,}".replace(",","."))
        mc5.metric("🎟️ Tiket",          f"Rp {details['total_entry_fee']:,}".replace(",","."))

        # Step-by-step path
        st.markdown("#### 🛣️ Detail Perjalanan Per Segmen")
        for i, leg in enumerate(details["legs"]):
            c_leg1, c_leg2 = st.columns([3, 2])
            with c_leg1:
                f_icon = graph.nodes.get(leg['from'],{}).get('icon','📍')
                t_icon = graph.nodes.get(leg['to'],{}).get('icon','📍')
                st.markdown(
                    f"<span class='step-badge'>{i+1}</span>"
                    f"{f_icon} **{leg['from_name']}** &nbsp;→&nbsp; {t_icon} **{leg['to_name']}**",
                    unsafe_allow_html=True,
                )
            with c_leg2:
                st.markdown(
                    f"📏 `{leg['distance_km']} km` &nbsp;"
                    f"⏱️ `{leg['time_minutes']} mnt` &nbsp;"
                    f"💰 `Rp {leg['transport_cost']:,}`".replace(",",".")
                )
            st.divider()

        # Total cost card
        total = details["total_cost"]
        sisa  = budget - total
        color = "card-success" if sisa >= 0 else "card-danger"
        st.markdown(f"""
        <div class="card {color}">
          <b>💰 Total Pengeluaran: Rp {total:,}</b>
          &nbsp;&nbsp;&nbsp;
          {'✅ Sisa Budget: Rp ' + f"{sisa:,}" if sisa >= 0 else '⚠️ Melebihi Budget: Rp ' + f"{abs(sisa):,}"}
        </div>
        """.replace(",","."), unsafe_allow_html=True)

        # Dijkstra step trace
        with st.expander("🔬 Lihat Proses Algoritma Dijkstra (Step-by-step)"):
            st.markdown(f"**Atribut bobot:** `{res['weight_attr']}` | **Total bobot:** `{res['weight']}`")
            steps_df = pd.DataFrame(res["steps"])
            steps_df["node_name"] = steps_df["visiting"].map(
                lambda n: f"{graph.nodes[n].get('icon','')} {graph.nodes[n].get('name',n)}" if n in graph.nodes else n
            )
            steps_df = steps_df[["visiting", "node_name", "cost_so_far", "visited_count"]]
            steps_df.columns = ["Node ID", "Nama Node", "Cost Kumulatif", "Sudah Dikunjungi"]
            st.dataframe(steps_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 4 — REKOMENDASI AI
# ══════════════════════════════════════════════
with tab4:
    st.markdown("### 🤖 Rekomendasi AI Berbasis Gemini")

    if not st.session_state.ai_text:
        st.info(
            "👈 Isi preferensi di sidebar, lalu klik **🚀 Analisis & Rekomendasikan** "
            "untuk mendapatkan rekomendasi dari Gemini AI."
        )
        st.markdown("""
        **Bagaimana AI Recommendation bekerja?**
        1. 🔬 Sistem menjalankan **algoritma Dijkstra** untuk mencari rute optimal
        2. 📊 Hasil analisis graf (rute, jarak, biaya, centrality) dikemas sebagai konteks
        3. 🤖 Konteks + profil wisatawan dikirim ke **Gemini 2.0 Flash** API
        4. ✍️ Gemini menghasilkan itinerary personal dalam Bahasa Indonesia
        5. 🌤️ Kondisi cuaca real-time turut mempengaruhi saran

        > *Graph bukan hanya teori — ia menjadi backbone pengambilan keputusan yang cerdas.*
        """)
    else:
        mp  = st.session_state.multi_path or {}
        det = mp.get("details", {})

        # Summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("🗺️ Destinasi", len(mp.get("path", [])))
        m2.metric("💰 Total Biaya", f"Rp {det.get('total_cost', 0):,}".replace(",","."))
        m3.metric("📏 Total Jarak", f"{det.get('total_distance_km', 0)} km")

        st.divider()
        st.markdown(st.session_state.ai_text)

        st.divider()
        st.caption("🤖 Ditenagai oleh Gemini 2.0 Flash | 🗺️ Berbasis Analisis Graf Dijkstra | 🌤️ Data cuaca OpenWeatherMap")


# ══════════════════════════════════════════════
# TAB 5 — ANALISIS GRAF
# ══════════════════════════════════════════════
with tab5:
    st.markdown("### 📊 Analisis Graf — Struktur & Properti")

    # Graph properties
    g_sum = graph.summary()
    centrality = graph.degree_centrality()

    col_props, col_alg = st.columns([1, 2])
    with col_props:
        st.markdown("#### ℹ️ Properti Graph")
        props = {
            "Jenis Graf":       "Weighted Undirected",
            "Representasi":     "Adjacency List",
            "Jumlah Node (V)":  g_sum["nodes"],
            "Jumlah Edge (E)":  g_sum["edges"],
            "Rata-rata Degree": g_sum["avg_degree"],
            "Directed":         "❌ Tidak (Undirected)",
        }
        for k, v in props.items():
            st.markdown(f"**{k}:** {v}")

        st.markdown("#### 🏆 Top 5 Node (Centrality)")
        top5 = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        for rank, (nid, val) in enumerate(top5, 1):
            icon = graph.nodes[nid].get("icon","📍")
            name = graph.nodes[nid].get("name", nid)
            st.markdown(f"`#{rank}` {icon} **{name}** — `{val:.4f}`")

    with col_alg:
        st.markdown("#### 🎓 Kompleksitas Algoritma")
        algo_df = pd.DataFrame([
            {
                "Algoritma":     "Dijkstra",
                "Time":          "O((V+E) log V)",
                "Space":         "O(V)",
                "Digunakan Untuk":"Rute optimal (jarak/waktu/biaya)",
                "Status":        "✅ Implementasi"
            },
            {
                "Algoritma":     "BFS",
                "Time":          "O(V+E)",
                "Space":         "O(V)",
                "Digunakan Untuk":"Eksplorasi semua node dari satu sumber",
                "Status":        "✅ Implementasi"
            },
            {
                "Algoritma":     "Degree Centrality",
                "Time":          "O(V+E)",
                "Space":         "O(V)",
                "Digunakan Untuk":"Identifikasi node hub/terpenting",
                "Status":        "✅ Implementasi"
            },
            {
                "Algoritma":     "Greedy Multi-Stop",
                "Time":          "O(K · Dijkstra)",
                "Space":         "O(V)",
                "Digunakan Untuk":"Perencanaan rute multi-destinasi",
                "Status":        "✅ Implementasi"
            },
        ])
        st.dataframe(algo_df, use_container_width=True, hide_index=True)

        # Adjacency list display
        with st.expander("📋 Lihat Adjacency List"):
            for nid, edges in graph.adjacency_list.items():
                icon = graph.nodes[nid].get("icon","📍")
                name = graph.nodes[nid].get("name", nid)
                nbrs = [f"{graph.nodes[e['to']].get('name',e['to'])} ({e.get('distance_km','?')}km)"
                        for e in edges]
                st.markdown(f"**{icon} {name}** → {', '.join(nbrs) or '—'}")

    st.divider()

    # Centrality chart
    st.markdown("#### 📊 Degree Centrality per Node")
    cent_fig = build_centrality_chart(centrality, graph.nodes)
    st.plotly_chart(cent_fig, use_container_width=True)

    st.markdown("""
    **📖 Interpretasi Degree Centrality:**
    Node dengan centrality tinggi = **hub strategis** yang paling banyak terhubung.
    Dalam konteks wisata Bali, node hub adalah destinasi yang paling mudah dicapai dari banyak tempat lain,
    sehingga cocok dijadikan titik transit atau tengah itinerary.
    """)

    st.divider()

    # BFS Traversal
    st.markdown("#### 🔍 BFS Traversal")
    bfs_start_disp = st.selectbox("Pilih node awal BFS:", list(all_opts.keys()), key="bfs_start")
    bfs_start_id   = all_opts[bfs_start_disp]

    if st.button("▶️ Jalankan BFS", key="run_bfs"):
        bfs_order = graph.bfs(bfs_start_id)
        bfs_fig   = build_bfs_chart(bfs_order, graph.nodes)
        st.plotly_chart(bfs_fig, use_container_width=True)

        st.markdown("**Urutan Kunjungan BFS:**")
        bfs_names = [
            f"{graph.nodes[n].get('icon','')} {graph.nodes[n].get('name', n)}"
            for n in bfs_order if n in graph.nodes
        ]
        st.markdown(" → ".join(bfs_names))


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<p style="text-align:center;color:#888;font-size:0.85rem;">
  🌴 <b>Bali Tourism DSS</b> — Project Struktur Data | Implementasi Graf sebagai DSS<br>
  Stack: Python · Streamlit · Plotly · Dijkstra · BFS · Gemini AI · OpenWeatherMap
</p>
""", unsafe_allow_html=True)
