import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
from logic import Logic

API_KEY = os.getenv("API_KEY")
LOC_KEY = os.getenv("LOCATION_IQ_TOKEN")
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

LAT = 36.7860908
LONG = 34.5310788
URL = "https://api.openweathermap.org/data/2.5/forecast"
LOCATION = f"https://us1.locationiq.com/v1/reverse?key={LOC_KEY}&lat={LAT}&lon={LONG}&format=json&"

params = {
    "lat": LAT,
    "lon": LONG,
    "appid": API_KEY,
    "units": "metric",
    "lang": "tr",
}

response_weather = requests.get(URL, params=params)
data_weather = response_weather.json()

response_location = requests.get(LOCATION)
data_location = response_location.json()

logic = Logic(data_weather,data_location)
weather = logic.weather_logic()
address = logic.location_logic()
text = (f"Güncel Konumun: {address['small_address']}\n"
        f"Sıcaklık: {weather['temp']}\n"
        f"Hissedilen Sıcaklık: {weather['feels_like']}\n"
        f"Yağmur yağma ihtimali: %{weather['rain_percentage']}\n"
        f"Görüş Mesafesi: {weather['visibility']} km\n"
        f"{address['town']}, {address['province']}")

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body= text,
    to='whatsapp:+905073519085'
)