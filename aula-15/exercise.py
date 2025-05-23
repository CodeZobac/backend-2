# AI Agent that fetches weather data from an external API
import requests
import json
from typing import Dict, Optional

class WeatherAgent:
    def __init__(self, name: str):
        self.name = name
        self.history = []
        # Using a free weather API that doesn't require authentication
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_coordinates(self, city: str) -> Optional[Dict]:
        """Get coordinates for a city using geocoding API"""
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        try:
            response = requests.get(geocoding_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                return {
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "name": result["name"],
                    "country": result.get("country", "Unknown")
                }
        except Exception as e:
            print(f"Error getting coordinates: {e}")
        
        return None
    
    def fetch_weather(self, city: str) -> str:
        """Fetch current weather data for a city"""
        try:
            # Get coordinates for the city
            coords = self.get_coordinates(city)
            if not coords:
                return f"Sorry, I couldn't find the city '{city}'. Please check the spelling."
            
            # Fetch weather data
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
                "timezone": "auto"
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            humidity = current.get("relative_humidity_2m", "N/A")
            wind_speed = current.get("wind_speed_10m", "N/A")
            
            return (f"Weather in {coords['name']}, {coords['country']}:\n"
                   f"Temperature: {temp}°C\n"
                   f"Humidity: {humidity}%\n"
                   f"Wind Speed: {wind_speed} km/h")
        
        except requests.exceptions.RequestException as e:
            return f"Sorry, I couldn't fetch weather data due to a network error: {e}"
        except Exception as e:
            return f"Sorry, there was an error processing your request: {e}"
    
    def respond(self, query: str) -> str:
        """Process queries and return appropriate responses"""
        self.history.append(query)
        query_lower = query.lower().strip()
        
        # Check if user wants to see history
        if "history" in query_lower:
            if len(self.history) > 1:  # Exclude the current history query
                return f"Your recent queries: {', '.join(self.history[:-1])}"
            else:
                return "No previous queries found."
        
        # Check for weather-related queries
        weather_keywords = ["weather", "temperature", "forecast", "climate"]
        if any(keyword in query_lower for keyword in weather_keywords):
            # Try to extract city name from the query
            words = query.split()
            city_candidates = []
            
            # Look for words after "in", "for", or common prepositions
            for i, word in enumerate(words):
                if word.lower() in ["in", "for", "at"] and i + 1 < len(words):
                    city_candidates.extend(words[i+1:])
                    break
            
            # If no preposition found, assume last few words might be the city
            if not city_candidates:
                # Remove common weather words to find city name
                filtered_words = [w for w in words if w.lower() not in weather_keywords + ["the", "what", "is", "today", "current"]]
                if filtered_words:
                    city_candidates = filtered_words[-2:]  # Take last 1-2 words
            
            if city_candidates:
                city = " ".join(city_candidates).strip("?.,!")
                return self.fetch_weather(city)
            else:
                return "Please specify a city. For example: 'What's the weather in London?'"
        
        # Default responses for non-weather queries
        if "hello" in query_lower or "hi" in query_lower:
            return f"Hello! I'm {self.name}, your weather assistant. Ask me about the weather in any city!"
        
        if "help" in query_lower:
            return ("I can help you get weather information for any city. "
                   "Try asking: 'What's the weather in [city name]?' or 'Temperature in [city]'")
        
        return ("I'm a weather agent. I can help you get current weather information for any city. "
               "Try asking about the weather in a specific location!")

if __name__ == "__main__":
    # Create and test the weather agent
    agent = WeatherAgent("WeatherAgent")
    
    # Test queries
    test_queries = [
        "Hello",
        "What's the weather in London?",
        "Temperature in New York",
        "Weather in Tokyo",
        "Help me",
        "Show me my history",
        "Random query"
    ]
    
    print(f"Testing {agent.name}")
    print("=" * 50)
    
    for query in test_queries:
        print(f"Query: {query}")
        response = agent.respond(query)
        print(f"Response: {response}")
        print("-" * 30)
