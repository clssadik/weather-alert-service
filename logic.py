class Logic:

    def __init__(self, data_weather, data_location):
        self.weather = data_weather
        self.location = data_location

    def weather_logic(self):
        items = self.weather["list"][:8]  # Önümüzdeki 24 saat

        temp = 0
        feels_like = 0
        rain_percentage = 0
        visibility = 0

        max_rain_percentage = 0
        total_rain_mm = 0
        min_visibility = float("inf")
        max_wind_speed = 0
        max_wind_gust = 0

        rainiest_item = None

        for item in items:
            temp += item["main"]["temp"]
            feels_like += item["main"]["feels_like"]

            pop = item.get("pop", 0)
            rain_percentage += pop
            max_rain_percentage = max(max_rain_percentage, pop)

            visibility_value = item.get("visibility", 10000)
            visibility += visibility_value
            min_visibility = min(min_visibility, visibility_value)

            rain_mm = item.get("rain", {}).get("3h", 0)
            total_rain_mm += rain_mm

            wind_speed = item.get("wind", {}).get("speed", 0)
            wind_gust = item.get("wind", {}).get("gust", 0)

            max_wind_speed = max(max_wind_speed, wind_speed)
            max_wind_gust = max(max_wind_gust, wind_gust)

            if rainiest_item is None or pop > rainiest_item.get("pop", 0):
                rainiest_item = item

        weather_dict = {
            "avg_temp": round(temp / len(items), 1),
            "avg_feels_like": round(feels_like / len(items), 1),

            "avg_rain_percentage": int(rain_percentage / len(items) * 100),
            "max_rain_percentage": int(max_rain_percentage * 100),

            "avg_visibility_km": round(visibility / len(items) / 1000, 1),
            "min_visibility_km": round(min_visibility / 1000, 1),

            "total_rain_mm": round(total_rain_mm, 1),

            "max_wind_speed": round(max_wind_speed, 1),
            "max_wind_gust": round(max_wind_gust, 1),
        }

        if rainiest_item:
            weather_dict["rainiest_time"] = rainiest_item["dt_txt"]
            weather_dict["rainiest_description"] = rainiest_item["weather"][0]["description"]

        return weather_dict

    def location_logic(self):
        address_dict = {
            "small_address": self.location["display_name"],
        }
        return address_dict