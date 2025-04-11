import uuid
import requests
from user_agents import parse

def generate_session_id():
    return str(uuid.uuid4())

def get_real_ip(request):
    try:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
            ip = ip.split(",")[0].strip()
        else:
            ip = request.remote_addr

        if ip.startswith("::ffff:"):
            ip = ip[7:]

        return ip
    except Exception as e:
        print(f"Erreur lors de la récupération de l'adresse IP : {e}")
        return "Unknown"

def get_geolocation(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "zip_code": data.get("zip", "Unknown"),
                    "latitude": data.get("lat", "Unknown"),
                    "longitude": data.get("lon", "Unknown"),
                    "timezone": data.get("timezone", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "org": data.get("org", "Unknown"),
                    "as": data.get("as", "Unknown")
                }
        print(f"Erreur de l'API de géolocalisation : {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"Erreur lors de la récupération des données de géolocalisation : {e}")
    return {
        "country": "Unknown",
        "country_code": "Unknown",
        "region": "Unknown",
        "city": "Unknown",
        "zip_code": "Unknown",
        "latitude": "Unknown",
        "longitude": "Unknown",
        "timezone": "Unknown",
        "isp": "Unknown",
        "org": "Unknown",
        "as": "Unknown"
    }

def get_shodan_data(ip_address, api_key):
    try:
        response = requests.get(f"https://api.shodan.io/shodan/host/{ip_address}?key={api_key}")
        if response.status_code == 200:
            data = response.json()
            return {
                "ports": data.get("ports", []),
                "os": data.get("os", "Unknown"),
                "hostnames": data.get("hostnames", []),
                "vulnerabilities": data.get("vulns", [])
            }
        print(f"Erreur de l'API Shodan : {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de la récupération des données Shodan : {e}")
    return {
        "ports": [],
        "os": "Unknown",
        "hostnames": [],
        "vulnerabilities": []
    }

def parse_user_agent(user_agent):
    try:
        ua = parse(user_agent)
        return {
            "browser": f"{ua.browser.family} {ua.browser.version_string}",
            "os": f"{ua.os.family} {ua.os.version_string}",
            "device": ua.device.family,
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_pc": ua.is_pc,
            "is_bot": ua.is_bot
        }
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'en-tête User-Agent : {e}")
        return {
            "browser": "Unknown",
            "os": "Unknown",
            "device": "Unknown",
            "is_mobile": False,
            "is_tablet": False,
            "is_pc": False,
            "is_bot": False
        }