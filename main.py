import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
import logic

API_KEY = os.getenv("API_KEY")
LOC_KEY = os.getenv("LOCATION_IQ_TOKEN")
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

LAT = 36.771297
LONG = 34.569662
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


temp = 0
for i in range(0,8):
    temp += data["list"][i]["main"]["temp"]

temp_24h = temp / 8
temp_24h = round(temp_24h,1)




message = client.messages.create(
    from_='whatsapp:+14155238886',
    body= f"yağmur yağıyor, önümüzdeki 24 saatlik ortalama sıcaklık : {temp_24h}",
    to='whatsapp:+905073519085'
)