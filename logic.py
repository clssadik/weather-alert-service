
class Logic():    
    
    def __init__(self, data_weather, data_location):
        self.weather = data_weather
        self.location = data_location
    
    def weather_logic(self):
        temp = feels_like = rain_percentage = visibility = 0
        for i in range(0,8):
            temp += self.weather["list"][i]["main"]["temp"]
            feels_like += self.weather["list"][i]["main"]["feels_like"]
            rain_percentage += self.weather["list"][i]["wind"]["pop"]
            visibility += self.weather["list"][i]["wind"]["visibility"]
        
        temp = round(temp/8 , 1)
        feels_like = round(feels_like/8 , 1)
        rain_percentage = (rain_percentage / 8) * 100
        visibility = visibility / 8
        


    def location_logic(self):
        