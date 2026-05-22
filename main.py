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
text = (
    f"Güncel Konumun: {address['small_address']}\n"
    f"\n"
    f"Önümüzdeki 24 Saatlik Hava Özeti\n"
    f"Sıcaklık Ortalaması: {weather['avg_temp']}°C\n"
    f"Hissedilen Sıcaklık Ortalaması: {weather['avg_feels_like']}°C\n"
    f"Ortalama Yağmur İhtimali: %{weather['avg_rain_percentage']}\n"
    f"En Yüksek Yağmur İhtimali: %{weather['max_rain_percentage']}\n"
    f"Toplam Beklenen Yağış: {weather['total_rain_mm']} mm\n"
    f"Ortalama Görüş Mesafesi: {weather['avg_visibility_km']} km\n"
    f"En Düşük Görüş Mesafesi: {weather['min_visibility_km']} km\n"
    f"Maksimum Rüzgar Hızı: {weather['max_wind_speed']} m/s\n"
    f"Maksimum Ani Rüzgar: {weather['max_wind_gust']} m/s\n"
    f"\n"
    f"Yağışın En Olası Olduğu Zaman: {weather['rainiest_time']}\n"
    f"Durum: {weather['rainiest_description']}"
)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body= text,
    to='whatsapp:+905073519085'
)

print(message.status)