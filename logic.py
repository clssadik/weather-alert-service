
class Logic():    
    
    def __init__(self, data_weather, data_location):
        self.weather = data_weather
        self.location = data_location
    
    def weather_logic(self):
        temp = feels_like = rain_percentage = visibility = 0
        for i in range(0,8):
            temp += self.weather["list"][i]["main"]["temp"]
            feels_like += self.weather["list"][i]["main"]["feels_like"]
            rain_percentage += self.weather["list"][i]["pop"]
            visibility += self.weather["list"][i]["visibility"]
        
        weather_dict = {
            "temp" : round(temp/8 , 1),
            "feels_like" : round(feels_like/8 , 1),
            "rain_percentage" : int(rain_percentage / 8 * 100),
            "visibility" : round(visibility / 8 / 1000 , 0)
        }
        return weather_dict
        


    def location_logic(self):
        address_dict = {
            "small_address" : self.location["address"]["university"],
            "town" : self.location["address"]["town"],
            "province" : self.location["address"]["province"]
        }
        return address_dict
        
        