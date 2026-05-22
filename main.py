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
SECRET = os.getenv("SECRET")
client = Client(account_sid, auth_token)

URL_GOOGLE = "https://script.google.com/macros/s/AKfycbxljEgcza_him96DBguVI-3w6h7N9n4rJ5DI6gFP6_ntg0t5pLvg_aEzCEs_Ivds1Hi/exec"

response_google = requests.get(URL_GOOGLE, params={
    "secret": SECRET
})
data_google = response_google.json()
LAT = data_google["lat"]
LONG = data_google["lon"]

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
print(response_weather.status_code)

response_location = requests.get(LOCATION)
data_location = response_location.json()
print(response_location.status_code)

logic = Logic(data_weather,data_location)
weather = logic.weather_logic()
address = logic.location_logic()
text = (f"Güncel Konumun: {address['small_address']}\n"
        f"Sıcaklık: {weather['temp']}\n"
        f"Hissedilen Sıcaklık: {weather['feels_like']}\n"
        f"Yağmur yağma ihtimali: %{weather['rain_percentage']}\n"
        f"Görüş Mesafesi: {weather['visibility']} km")

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body= text,
    to='whatsapp:+905073519085'
)

print(message.status)