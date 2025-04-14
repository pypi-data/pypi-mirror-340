import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file

class WeatherCommand:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")  # Safely reads the key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
    
    def execute(self, command):
        if not command.startswith("weather "):
            return None
        
        location = command[8:].strip()
        if not location:
            return "Please specify a location"
        
        try:
            complete_url = f"{self.base_url}appid={self.api_key}&q={location}"
            response = requests.get(complete_url)
            data = response.json()
            
            if data["cod"] != "404":
                main = data["main"]
                weather = data["weather"][0]
                return (
                    f"Weather in {location}:\n"
                    f"Description: {weather['description']}\n"
                    f"Temperature: {main['temp'] - 273.15:.1f}°C\n"
                    f"Humidity: {main['humidity']}%\n"
                    f"Wind Speed: {data['wind']['speed']} m/s"
                )
            else:
                return "Location not found"
        except Exception as e:
            return f"Weather API error: {str(e)}"