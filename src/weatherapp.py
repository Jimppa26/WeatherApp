# /// script
# dependencies = [
#       "requests",
#       "plyer",
# ]
# ///

import requests
from plyer import notification

city = input("Kaupunki: ")
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {"name": city, "count": 1} # Sanakirja missä on hakuehdot (kaupungin nimi, tulosten lukumäärä)
geo_res = requests.get(geo_url, params=geo_params).json() # Lähettää 'GET' pyynnön geocoding API:lle hakuehdoilla ja kääntää API:n vastauksen JSON formattiin

if "results" in geo_res:
    # Lat & Lon ottaa leveyspiirin ja pituuspiirin API:n vastauksesta
    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    # Sisältää koordinaatit ja kertoo API:lle että palauttaa vain tämän hetkisen sään
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        	"current": ["snowfall", "rain", "temperature_2m", "cloud_cover", "wind_speed_10m"]
    }
    weather_res = requests.get(weather_url, params=weather_params).json() # Hakee säätiedot vain kyseisestä kaupungista

    if "current" in weather_res:
        while True:
            action = input("Mitä haluat tietää? (Kirjoita 'exit' lopettaaksesi): ")
            weather_info = None

            if action == "-help":
                print(f"lämpötila, tuuli, sade, pilvisyys")
            elif action == "lämpötila":
                temp = weather_res["current"]["temperature_2m"]
                weather_info = f"{city}: {temp}°C"
            elif action == "tuuli":
                wind = weather_res["current"]["wind_speed_10m"]
                weather_info = f"{city}: Tuuli {wind} km/h"
            elif action == "pilvisyys":
                cloud = weather_res["current"]["cloud_cover"]
                weather_info = f"{city}: Pilvisyys {cloud}%"
            elif action == "sade":
                rain = weather_res["current"]["rain"]
                snow = weather_res["current"]["snowfall"]
                if snow > 0 and rain > 0:
                    weather_info = f"{city}: Sataa räntää (Vettä {rain} mm, Lunta {snow} cm)"
                elif snow > 0:
                    weather_info = f"{city}: Lumisade ({snow} cm)"
                elif rain > 0:
                    weather_info = f"{city}: Vesisade ({rain} mm)"
                else:
                    weather_info = f"{city}: Ei sada."
            elif action == "exit":
                print("Lopetetaan...")
                break

            else:
                print("Virheellinen valinta. Käytä -help")

            if weather_info:
                print("Weather:", weather_info)

                # Tekee popup-ilmoituksen näytölle
                notification.notify(
                    title = "Säätiedotus",
                    message = weather_info,
                    # Popup näkyy 5s ajan
                    timeout = 5
                )
    else:
        print("Säätiedotusta ei saatavilla.")
else:
    print("Kaupunkia ei löytynyt.")