import os
import requests
from pathlib import Path
from dotenv import load_dotenv

class WeatherCommand:
    def __init__(self):
        # Try to load API key from multiple sources
        self.api_key = self._get_api_key()
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    def _get_api_key(self):
        # 1. Check environment variables first (production)
        if api_key := os.getenv("OPENWEATHER_API_KEY"):
            return api_key
        
        # 2. Try to load from .env file in package directory (development)
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            if api_key := os.getenv("OPENWEATHER_API_KEY"):
                return api_key
        
        # 3. Final fallback - check current directory (user installation)
        load_dotenv()  # Try default .env location
        if api_key := os.getenv("OPENWEATHER_API_KEY"):
            return api_key
        
        raise ValueError(
            "Weather API key not found. "
            "Please set OPENWEATHER_API_KEY in environment variables "
            "or create a .env file in the package directory."
        )

    def execute(self, command):
        if not command.startswith("weather "):
            return None
            
        location = command[8:].strip()
        try:
            complete_url = f"{self.base_url}q={location}&appid={self.api_key}&units=metric"
            response = requests.get(complete_url)
            data = response.json()
            
            if data["cod"] != 200:
                return f"Error: {data.get('message', 'Unknown error')}"
                
            return (
                f"\nWeather in {location}:\n"
                f"Conditions: {data['weather'][0]['description'].capitalize()}\n"
                f"Temperature: {data['main']['temp']}°C\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind: {data['wind']['speed']} m/s\n"
            )
        except Exception as e:
            return f"Weather API error: {str(e)}"