from flask import Flask, request
import csv
from datetime import datetime
from user_agents import parse
import requests
import os
import uuid
from .utils import get_real_ip, get_geolocation, get_shodan_data, parse_user_agent, generate_session_id

class ClickTracker:
    def __init__(self, app=None, csv_file="clicks.csv", shodan_api_key=None):
        self.csv_file = csv_file
        self.shodan_api_key = shodan_api_key
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        self.init_csv()
        self.register_routes()
    
    def init_csv(self):
        try:
            with open(self.csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow([
                        "ID", "Session_ID", "IP", "Timestamp", "Browser", "OS", "Device",
                        "Is Mobile", "Is Tablet", "Is PC", "Is Bot", "Country", "Country Code",
                        "Region", "City", "Zip Code", "Latitude", "Longitude", "Timezone",
                        "ISP", "Organization", "AS", "Referer", "Accept-Language", "Host",
                        "Shodan_Ports", "Shodan_OS", "Shodan_Hostnames", "Shodan_Vulnerabilities"
                    ])
            print(f"Fichier CSV initialisé avec succès: {self.csv_file}")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du fichier CSV : {e}")

    def register_routes(self):
        @self.app.route('/track')
        def track_click():
            try:
                visitor_ip = get_real_ip(request)
                user_agent = request.user_agent.string
                self.log_click(visitor_ip, user_agent)
                return {
                    "status": "success",
                    "message": "Click tracked successfully"
                }, 200
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e)
                }, 500

        @self.app.route('/admin/clicks')
        def view_clicks():
            try:
                clicks = []
                with open(self.csv_file, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        clicks.append(row)
                return {
                    "status": "success",
                    "data": clicks
                }, 200
            except FileNotFoundError:
                return {
                    "status": "error",
                    "message": "No clicks recorded yet"
                }, 404
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e)
                }, 500

    def log_click(self, ip_address, user_agent):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_id = generate_session_id()

            parsed_user_agent = parse_user_agent(user_agent)
            geolocation = get_geolocation(ip_address)
            
            shodan_data = {}
            if self.shodan_api_key:
                shodan_data = get_shodan_data(ip_address, self.shodan_api_key)

            referer = request.headers.get("Referer", "Unknown")
            accept_language = request.headers.get("Accept-Language", "Unknown")
            host = request.headers.get("Host", "Unknown")

            data_to_log = {
                "session_id": session_id,
                "ip": ip_address,
                "timestamp": timestamp,
                "browser": parsed_user_agent["browser"],
                "os": parsed_user_agent["os"],
                "device": parsed_user_agent["device"],
                "is_mobile": parsed_user_agent["is_mobile"],
                "is_tablet": parsed_user_agent["is_tablet"],
                "is_pc": parsed_user_agent["is_pc"],
                "is_bot": parsed_user_agent["is_bot"],
                "country": geolocation["country"],
                "country_code": geolocation["country_code"],
                "region": geolocation["region"],
                "city": geolocation["city"],
                "zip_code": geolocation["zip_code"],
                "latitude": geolocation["latitude"],
                "longitude": geolocation["longitude"],
                "timezone": geolocation["timezone"],
                "isp": geolocation["isp"],
                "org": geolocation["org"],
                "as": geolocation["as"],
                "referer": referer,
                "accept_language": accept_language,
                "host": host,
                "shodan_ports": shodan_data.get("ports", []),
                "shodan_os": shodan_data.get("os", "Unknown"),
                "shodan_hostnames": shodan_data.get("hostnames", []),
                "shodan_vulnerabilities": shodan_data.get("vulnerabilities", [])
            }

            last_id = 0
            try:
                with open(self.csv_file, "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                    if len(rows) > 1:
                        last_id = int(rows[-1][0])
            except FileNotFoundError:
                pass

            with open(self.csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    last_id + 1,
                    data_to_log["session_id"],
                    data_to_log["ip"],
                    data_to_log["timestamp"],
                    data_to_log["browser"],
                    data_to_log["os"],
                    data_to_log["device"],
                    data_to_log["is_mobile"],
                    data_to_log["is_tablet"],
                    data_to_log["is_pc"],
                    data_to_log["is_bot"],
                    data_to_log["country"],
                    data_to_log["country_code"],
                    data_to_log["region"],
                    data_to_log["city"],
                    data_to_log["zip_code"],
                    data_to_log["latitude"],
                    data_to_log["longitude"],
                    data_to_log["timezone"],
                    data_to_log["isp"],
                    data_to_log["org"],
                    data_to_log["as"],
                    data_to_log["referer"],
                    data_to_log["accept_language"],
                    data_to_log["host"],
                    data_to_log["shodan_ports"],
                    data_to_log["shodan_os"],
                    data_to_log["shodan_hostnames"],
                    data_to_log["shodan_vulnerabilities"]
                ])

        except Exception as e:
            print(f"Erreur lors de l'enregistrement du clic : {e}")
            raise