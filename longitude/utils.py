import math
import requests

def haversine_distance(lat1, lon1, lat2, lon2):
  
    R = 6371.0 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c
    distance_miles = distance_km * 0.621371
    return distance_miles

def reverse_geocode(lat, lon):
   
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1,
        }
        headers = {
            "User-Agent": "location-app/1.0"
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "")
        else:
            return ""
    except Exception as e:
        return ""