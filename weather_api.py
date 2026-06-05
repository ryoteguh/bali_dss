"""
weather_api.py — Integrasi OpenWeatherMap untuk cuaca Bali real-time.
Fallback ke data mock jika API key tidak tersedia.
"""

import os
import requests
from datetime import datetime


def get_bali_weather() -> dict:
    """
    Ambil cuaca Denpasar/Bali dari OpenWeatherMap API.
    Kembalikan dict standar yang dipakai seluruh aplikasi.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "")

    if not api_key:
        return _mock_weather()

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": "Denpasar,ID",
            "appid": api_key,
            "units": "metric",
            "lang": "id",
        }
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        condition = data["weather"][0]["description"].capitalize()
        temp      = data["main"]["temp"]
        humidity  = data["main"]["humidity"]
        wind_kmh  = round(data["wind"]["speed"] * 3.6, 1)
        is_rainy  = any(
            kw in condition.lower()
            for kw in ["hujan", "rain", "drizzle", "thunderstorm", "shower"]
        )

        return {
            "source": "openweathermap",
            "condition": condition,
            "temp": round(temp, 1),
            "humidity": humidity,
            "wind_kmh": wind_kmh,
            "is_rainy": is_rainy,
            "icon": _weather_icon(condition, is_rainy),
            "outdoor_suitable": temp <= 34 and not is_rainy,
            "fetched_at": datetime.now().strftime("%H:%M WIB"),
        }

    except Exception as e:
        mock = _mock_weather()
        mock["error"] = str(e)
        return mock


def _mock_weather() -> dict:
    """Data cuaca mock — Bali musim kemarau (Jun–Sep)."""
    return {
        "source": "mock",
        "condition": "Cerah berawan",
        "temp": 28.5,
        "humidity": 73,
        "wind_kmh": 14.0,
        "is_rainy": False,
        "icon": "⛅",
        "outdoor_suitable": True,
        "fetched_at": datetime.now().strftime("%H:%M WIB"),
    }


def _weather_icon(condition: str, is_rainy: bool) -> str:
    c = condition.lower()
    if "thunderstorm" in c:      return "⛈️"
    if is_rainy:                  return "🌧️"
    if "cloud" in c or "berawan" in c: return "⛅"
    if "mist" in c or "fog" in c:     return "🌫️"
    return "☀️"


def weather_recommendation(weather: dict) -> str:
    """Kembalikan saran singkat berdasarkan kondisi cuaca."""
    if weather.get("is_rainy"):
        return "🌧️ Hujan terdeteksi. Rekomendasikan kunjungan pura tertutup atau aktivitas indoor."
    temp = weather.get("temp", 28)
    if temp > 33:
        return f"🌡️ Cukup panas ({temp}°C). Bawa air minum & topi. Pantai tetap OK pagi/sore hari."
    return f"☀️ Cuaca bagus ({temp}°C)! Cocok untuk semua jenis wisata outdoor."
