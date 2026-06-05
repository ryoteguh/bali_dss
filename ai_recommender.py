"""
ai_recommender.py — Integrasi Gemini API untuk rekomendasi perjalanan berbasis Graph.
Fallback ke rekomendasi berbasis aturan jika API key tidak tersedia.
"""

import os
from typing import Optional


def _format_idr(amount: int) -> str:
    return f"Rp {amount:,}".replace(",", ".")


def _build_prompt(user_profile: dict, path_result: dict, graph_nodes: dict, weather: dict) -> str:
    """Buat prompt Gemini yang kaya konteks dari hasil analisis graph."""
    path_ids = path_result.get("path", [])
    path_names = [
        f"{graph_nodes[n].get('icon','📍')} {graph_nodes[n].get('name', n)}"
        for n in path_ids
        if n in graph_nodes
    ]

    legs = path_result.get("details", {}).get("legs", [])
    leg_text = "\n".join(
        f"  {i+1}. {l['from_name']} → {l['to_name']}: "
        f"{l['distance_km']} km | {l['time_minutes']} mnt | {_format_idr(l['transport_cost'])}"
        for i, l in enumerate(legs)
    )

    dest_details = ""
    for nid in path_ids:
        if nid in graph_nodes:
            n = graph_nodes[nid]
            dest_details += (
                f"\n  • {n.get('icon','')} {n.get('name', nid)} "
                f"[Rating: {n.get('rating','?')}/5 | "
                f"Tiket: {_format_idr(n.get('entry_fee',0))} | "
                f"Durasi: {n.get('duration_hours','?')} jam]\n"
                f"    Tips: {n.get('tips','')}\n"
            )

    total_cost = path_result.get("details", {}).get("total_cost", 0)
    sisa_budget = user_profile.get("budget", 0) - total_cost

    prompt = f"""
Kamu adalah sistem AI dalam sebuah DSS (Decision Support System) berbasis Graf untuk rekomendasi wisata Bali.
Berikan rekomendasi wisata yang personal, informatif, dan praktis dalam Bahasa Indonesia yang hangat.

=== PROFIL WISATAWAN ===
- Nama       : {user_profile.get('name', 'Wisatawan')}
- Asal       : {user_profile.get('origin', '-')}
- Budget     : {_format_idr(user_profile.get('budget', 0))}
- Durasi     : {user_profile.get('duration', '?')} jam
- Kategori   : {', '.join(user_profile.get('categories', []))}
- Optimasi   : {user_profile.get('optimization_label', 'Terbaik')}

=== HASIL ANALISIS GRAF — Algoritma Dijkstra ===
- Rute Optimal  : {' → '.join(path_names)}
- Total Jarak   : {path_result.get('details', {}).get('total_distance_km', 0)} km
- Total Waktu   : {path_result.get('details', {}).get('total_time_minutes', 0)} mnt ({path_result.get('details', {}).get('total_time_minutes', 0)//60} jam {path_result.get('details', {}).get('total_time_minutes', 0)%60} mnt)
- Biaya Transport : {_format_idr(path_result.get('details', {}).get('total_transport_cost', 0))}
- Tiket Masuk   : {_format_idr(path_result.get('details', {}).get('total_entry_fee', 0))}
- Total Biaya   : {_format_idr(total_cost)}
- Sisa Budget   : {_format_idr(max(sisa_budget, 0))} {'⚠️ MELEBIHI BUDGET' if sisa_budget < 0 else '✅'}

=== DETAIL SEGMEN PERJALANAN ===
{leg_text or '  (tidak ada segmen)'}

=== DESTINASI DALAM RUTE ===
{dest_details}

=== CUACA BALI SAAT INI ===
- Kondisi  : {weather.get('condition', 'Tidak diketahui')}
- Suhu     : {weather.get('temp', '?')}°C
- Kelembaban: {weather.get('humidity', '?')}%
- Cocok untuk: {'aktivitas outdoor' if not weather.get('is_rainy', False) else 'kunjungan pura/indoor'}

=== INSTRUKSI OUTPUT ===
Tulis rekomendasi dengan format BERIKUT PERSIS (gunakan heading markdown):

## 👋 Halo, {user_profile.get('name', 'Traveler')}!
(Sambutan hangat 2-3 kalimat, mention asal kota & kenapa Bali cocok)

## 🗺️ Itinerary Harian
(Buat jadwal per jam berdasarkan durasi {user_profile.get('duration', 8)} jam.
Format: **[Waktu]** — [Tempat] — Aktivitas — *Tips lokal*)

## 🔬 Mengapa Rute Ini Optimal?
(Jelaskan dalam 3-4 kalimat: bagaimana algoritma Dijkstra memilih rute ini,
apa keunggulannya, kenapa lebih baik dari rute alternatif)

## 💰 Rincian Biaya
(Tabel atau list: transport, tiket masuk, estimasi makan, total, sisa budget)

## 🌤️ Tips Cuaca & Waktu Terbaik
(Saran berdasarkan kondisi cuaca saat ini: {weather.get('condition','?')} {weather.get('temp','?')}°C)

## ✨ Bonus Rekomendasi
(2-3 tempat tambahan yang layak dikunjungi jika waktu & budget masih ada)

Gunakan bahasa yang hangat dan personal. Tambahkan emoji relevan di setiap poin.
Jangan ulangi data mentah yang sudah ada di atas — olah menjadi narasi yang berguna.
"""
    return prompt.strip()


def get_ai_recommendation(
    user_profile: dict,
    path_result: dict,
    graph_nodes: dict,
    weather: dict,
) -> str:
    """
    Kirim prompt ke Gemini API dan kembalikan teks rekomendasi.
    Fallback ke rekomendasi rule-based jika API key tidak ada / error.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        return _rule_based_recommendation(user_profile, path_result, graph_nodes, weather)

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        prompt = _build_prompt(user_profile, path_result, graph_nodes, weather)
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return (
            f"⚠️ **Gemini API tidak tersedia** ({e})\n\n"
            + _rule_based_recommendation(user_profile, path_result, graph_nodes, weather)
        )


def _rule_based_recommendation(
    user_profile: dict, path_result: dict, graph_nodes: dict, weather: dict
) -> str:
    """Rekomendasi fallback berbasis aturan tanpa AI."""
    path_ids = path_result.get("path", [])
    details  = path_result.get("details", {})
    name     = user_profile.get("name", "Wisatawan")
    budget   = user_profile.get("budget", 0)
    duration = user_profile.get("duration", 8)

    path_names = [
        f"{graph_nodes[n].get('icon','📍')} {graph_nodes[n].get('name', n)}"
        for n in path_ids if n in graph_nodes
    ]

    total_cost = details.get("total_cost", 0)
    sisa       = budget - total_cost
    time_min   = details.get("total_time_minutes", 0)

    # Susun itinerary sederhana
    current_hour = 8
    itinerary_lines = []
    for nid in path_ids:
        if nid not in graph_nodes:
            continue
        n = graph_nodes[nid]
        dur = n.get("duration_hours", 1)
        itinerary_lines.append(
            f"**{current_hour:02d}.00** — {n.get('icon','')} {n.get('name', nid)} "
            f"({dur} jam) — {', '.join(n.get('activities', [])[:2])}"
        )
        current_hour += int(dur) + 1  # +1 untuk transit

    weather_tip = (
        "☀️ Cuaca cerah, cocok untuk aktivitas outdoor!"
        if not weather.get("is_rainy", False)
        else "🌧️ Cuaca mendung/hujan. Prioritaskan kunjungan pura atau aktivitas indoor."
    )

    return f"""
## 👋 Halo, {name}!
Selamat datang di sistem rekomendasi wisata Bali berbasis Graf! Berikut itinerary optimal untukmu.

## 🗺️ Itinerary Harian
{chr(10).join(itinerary_lines)}

## 🔬 Mengapa Rute Ini Optimal?
Algoritma **Dijkstra** menganalisis semua kemungkinan jalur di antara {len(graph_nodes)} destinasi
dan menemukan rute **{' → '.join(path_names)}** sebagai yang paling efisien berdasarkan
kriteria {user_profile.get('optimization_label','yang dipilih')}.
Total jarak tempuh hanya **{details.get('total_distance_km', 0)} km**
dalam waktu sekitar **{time_min // 60} jam {time_min % 60} menit** perjalanan.

## 💰 Rincian Biaya
- 🚗 Transport    : {_format_idr(details.get('total_transport_cost', 0))}
- 🎟️ Tiket Masuk  : {_format_idr(details.get('total_entry_fee', 0))}
- 🍽️ Est. Makan   : {_format_idr(100000 * len(path_ids))}
- **Total         : {_format_idr(total_cost + 100000 * len(path_ids))}**
- Sisa Budget     : {_format_idr(max(sisa, 0))} {'✅' if sisa >= 0 else '⚠️ Melebihi budget!'}

## 🌤️ Tips Cuaca
{weather_tip} Suhu saat ini {weather.get('temp','?')}°C.

## ✨ Bonus Rekomendasi
Jika waktu & budget masih ada, pertimbangkan: 🌅 Sunset di Tanah Lot, 🐒 Monkey Forest Ubud,
atau 💧 Tirta Gangga untuk pengalaman taman air kerajaan yang unik.
""".strip()
