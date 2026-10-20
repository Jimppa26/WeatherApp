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
        "current_weather": True
    }
    weather_res = requests.get(weather_url, params=weather_params).json() # Hakee säätiedot vain kyseisestä kaupungista

    if "current_weather" in weather_res:
        # Hakee lämpötilan, tuulennopeuden sekä pistää ne hienoon järjestykseen
        temp = weather_res["current_weather"]["temperature"]
        wind = weather_res["current_weather"]["windspeed"]
        weather_info = f"{city}: {temp}°C, Tuuli {wind} km/h"

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