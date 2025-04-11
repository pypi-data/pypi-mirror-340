# click_tracker_library/utils.py

import csv
from datetime import datetime
from user_agents import parse
import requests
import uuid

def init_csv(csv_file):
    try:
        with open(csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Vérifier si le fichier est vide
                writer.writerow([
                    "ID", "Session_ID", "IP", "Timestamp", "Browser", "OS", "Device",
                    "Is Mobile", "Is Tablet", "Is PC", "Is Bot", "Country", "Country Code",
                    "Region", "City", "Zip Code", "Latitude", "Longitude", "Timezone",
                    "ISP", "Organization", "AS", "Referer", "Accept-Language", "Host",
                    "Shodan_Ports", "Shodan_OS", "Shodan_Hostnames", "Shodan_Vulnerabilities"
                ])
        print("Fichier CSV initialisé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation du fichier CSV : {e}")

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

# Autres fonctions (géolocalisation, Shodan, User-Agent, etc.) restent inchangées...