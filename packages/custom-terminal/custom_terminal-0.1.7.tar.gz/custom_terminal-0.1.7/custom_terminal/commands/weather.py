import requests

class WeatherCommand:
    def __init__(self):
        # Replace this with your actual OpenWeatherMap API key
        self.api_key = "e9c40d3e641444e896021ba7c8d35d9c"  # ← Direct key insertion
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def execute(self, command):
        if not command.startswith("weather "):
            return None
            
        location = command[8:].strip()
        try:
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return (
                f"\nWeather in {location}:\n"
                f"Conditions: {data['weather'][0]['description'].capitalize()}\n"
                f"Temperature: {data['main']['temp']}°C\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind: {data['wind']['speed']} m/s"
            )
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                return "Error: The hardcoded API key is invalid. Contact package maintainer."
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Weather lookup failed: {str(e)}"