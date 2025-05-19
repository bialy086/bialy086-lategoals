from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Tutaj wpisz swój prawdziwy token z API SportMonks
API_TOKEN = "TWOJ_API_TOKEN"
API_URL = f"https://api.sportmonks.com/v3/football/livescores?include=localTeam,visitorTeam&api_token={API_TOKEN}"

@app.route("/")
def home():
    try:
        response = requests.get(API_URL)
        data = response.json()
        mecze = []

        for mecz in data.get("data", []):
            minuta = mecz.get("time", {}).get("minute", 0)
            status = mecz.get("time", {}).get("status")
            if status != "LIVE":
                continue

            # Szukamy meczów w końcówce połów
            if 30 <= minuta <= 45 or 75 <= minuta <= 90:
                mecze.append({
                    "gospodarz": mecz["localTeam"]["data"]["name"],
                    "gosc": mecz["visitorTeam"]["data"]["name"],
                    "minuta": minuta,
                    "wynik": f'{mecz["scores"]["localteam_score"]}-{mecz["scores"]["visitorteam_score"]}'
                })

        return jsonify(mecze)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()


