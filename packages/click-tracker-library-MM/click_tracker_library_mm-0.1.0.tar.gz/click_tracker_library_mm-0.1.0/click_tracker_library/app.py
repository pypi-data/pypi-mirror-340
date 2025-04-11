# click_tracker_library/app.py

from flask import request, redirect
from .utils import get_real_ip, parse_user_agent, get_geolocation, get_shodan_data, log_click

def track_click():
    try:
        visitor_ip = get_real_ip()  # Récupérer l'adresse IP réelle
        user_agent = request.headers.get("User-Agent", "Unknown")
        log_click(visitor_ip, user_agent)
        return """
        <h1>Merci d'avoir visité cette page !</h1>
        <p>Votre clic a été enregistré.</p>
        <p>Vous allez être redirigé vers Google dans quelques secondes...</p>
        <script>
            setTimeout(function() {
                window.location.href = "https://www.google.com";
            }, 100);
        </script>
        """
    except Exception as e:
        return f"Une erreur est survenue : {e}", 500

def view_clicks():
    try:
        html = "<h1>Liste des clics enregistrés</h1><table border='1'>"
        html += """
        <tr>
            <th>ID</th><th>Session ID</th><th>IP</th><th>Date</th><th>Navigateur</th><th>OS</th><th>Appareil</th>
            <th>Mobile ?</th><th>Tablette ?</th><th>PC ?</th><th>Bot ?</th><th>Pays</th><th>Code Pays</th><th>Région</th>
            <th>Ville</th><th>Code Postal</th><th>Latitude</th><th>Longitude</th><th>Fuseau Horaire</th><th>ISP</th>
            <th>Organisation</th><th>AS</th><th>Référent</th><th>Langue Acceptée</th><th>Hôte</th>
            <th>Shodan Ports</th><th>Shodan OS</th><th>Shodan Hostnames</th><th>Shodan Vulnerabilities</th>
        </tr>
        """
        try:
            with open(app.config['CSV_FILE'], "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Ignorer l'en-tête
                for row in reader:
                    html += f"""
                    <tr>
                        <td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td>
                        <td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td><td>{row[9]}</td><td>{row[10]}</td><td>{row[11]}</td>
                        <td>{row[12]}</td><td>{row[13]}</td><td>{row[14]}</td><td>{row[15]}</td><td>{row[16]}</td><td>{row[17]}</td>
                        <td>{row[18]}</td><td>{row[19]}</td><td>{row[20]}</td><td>{row[21]}</td><td>{row[22]}</td><td>{row[23]}</td>
                        <td>{row[24]}</td><td>{row[25]}</td><td>{row[26]}</td><td>{row[27]}</td><td>{row[28]}</td>
                    </tr>
                    """
        except FileNotFoundError:
            html += "<tr><td colspan='29'>Aucun clic enregistré.</td></tr>"
        html += "</table>"
        return html
    except Exception as e:
        return f"Erreur lors de la récupération des logs : {e}", 500