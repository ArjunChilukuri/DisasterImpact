"""
Tools for geocoding and feed fetching
"""

import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from .logger import log_message

def geo_encode(location: str) -> Dict[str, Any]:
    """Geocode a location using Nominatim OpenStreetMap API"""
    if not location or len(location.strip()) < 3:
        return {'coordinates': None, 'description': 'Location too short'}
    url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(location)}&format=json&limit=1"
    try:
        r = requests.get(url, headers={'User-Agent': 'ADK-Geocoder/1.0'}, timeout=8)
        r.raise_for_status()
        data = r.json()
        if data:
            d0 = data[0]
            return {'coordinates': {'lat': float(d0['lat']), 'lon': float(d0['lon']), 'accuracy': d0.get('type', 'unknown')}, 'description': d0.get('display_name')}
        return {'coordinates': None, 'description': 'No result'}
    except Exception as e:
        log_message(f"Geo encode error: {e}")
        return {'coordinates': None, 'description': str(e)}

def feed_fetch_tool(limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch alerts from Sachet NDMA feed"""
    url = "https://sachet.ndma.gov.in"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.select("a[href$='.xml']")
        return [{'text': f"Alert: {link.get_text(strip=True)}", 'source': 'sachet_ndma'} for link in links[:limit]]
    except Exception as e:
        log_message(f"feed fetch error: {e}")
        return []
