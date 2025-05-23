# Advanced AI Agent with complex query handling and API data enrichment
import requests
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

class AdvancedIntelligentAgent:
    def __init__(self, name: str):
        self.name = name
        self.history = []
        self.context = {}
        
        # API endpoints for different services
        self.apis = {
            "weather": "https://api.open-meteo.com/v1/forecast",
            "geocoding": "https://geocoding-api.open-meteo.com/v1/search",
            "currency": "https://api.exchangerate-api.com/v4/latest/",
            "facts": "https://uselessfacts.jsph.pl/random.json",
        }
    
    def parse_structured_query(self, query: str) -> Dict[str, Any]:
        """Parse structured queries to extract intent and entities"""
        query_lower = query.lower().strip()
        
        # Define patterns for different query types
        patterns = {
            "weather": {
                "pattern": r"weather|temperature|forecast|climate",
                "entities": {"location": r"in\s+([a-zA-Z\s]+)(?:\?|$)"}
            },
            "currency": {
                "pattern": r"currency|exchange|convert|rate",
                "entities": {
                    "from_currency": r"(\w{3})\s+to\s+\w{3}",
                    "to_currency": r"\w{3}\s+to\s+(\w{3})"
                }
            },
            "fact": {
                "pattern": r"fact|interesting|tell me something|random",
                "entities": {}
            },
            "calculation": {
                "pattern": r"calculate|compute|math|\+|\-|\*|\/",
                "entities": {"expression": r"calculate\s+(.+)"}
            },
            "time": {
                "pattern": r"time|date|today|now",
                "entities": {}
            }
        }
        
        result = {"intent": "unknown", "entities": {}, "confidence": 0.0}
        
        for intent, config in patterns.items():
            if re.search(config["pattern"], query_lower):
                result["intent"] = intent
                result["confidence"] = 0.8
                
                # Extract entities
                for entity_name, entity_pattern in config["entities"].items():
                    match = re.search(entity_pattern, query_lower)
                    if match:
                        result["entities"][entity_name] = match.group(1).strip()
                
                break
        
        return result
    
    def get_weather_data(self, location: str) -> str:
        """Get weather data for a location"""
        try:
            # Get coordinates
            geocoding_response = requests.get(
                self.apis["geocoding"],
                params={"name": location, "count": 1, "format": "json"},
                timeout=5
            )
            geocoding_data = geocoding_response.json()
            
            if not geocoding_data.get("results"):
                return f"I couldn't find weather data for '{location}'. Please check the location name."
            
            coords = geocoding_data["results"][0]
            
            # Get weather data
            weather_response = requests.get(
                self.apis["weather"],
                params={
                    "latitude": coords["latitude"],
                    "longitude": coords["longitude"],
                    "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"],
                    "timezone": "auto"
                },
                timeout=5
            )
            weather_data = weather_response.json()
            
            current = weather_data.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            humidity = current.get("relative_humidity_2m", "N/A")
            wind_speed = current.get("wind_speed_10m", "N/A")
            
            return (f"🌤️ Weather in {coords['name']}, {coords.get('country', '')}:\n"
                   f"🌡️ Temperature: {temp}°C\n"
                   f"💧 Humidity: {humidity}%\n"
                   f"💨 Wind Speed: {wind_speed} km/h")
        
        except Exception as e:
            return f"Sorry, I couldn't fetch weather data: {str(e)}"
    
    def get_currency_rate(self, from_currency: str, to_currency: str) -> str:
        """Get currency exchange rate"""
        try:
            response = requests.get(f"{self.apis['currency']}{from_currency.upper()}", timeout=5)
            data = response.json()
            
            to_currency_upper = to_currency.upper()
            if to_currency_upper in data.get("rates", {}):
                rate = data["rates"][to_currency_upper]
                return f"💱 1 {from_currency.upper()} = {rate:.4f} {to_currency_upper}"
            else:
                return f"Sorry, I couldn't find the exchange rate for {to_currency.upper()}"
        
        except Exception as e:
            return f"Sorry, I couldn't fetch currency data: {str(e)}"
    
    def get_random_fact(self) -> str:
        """Get a random interesting fact"""
        try:
            response = requests.get(self.apis["facts"], timeout=5)
            data = response.json()
            return f"🧠 Interesting fact: {data.get('text', 'No fact available at the moment.')}"
        
        except Exception as e:
            return "Here's a fact: Python was named after Monty Python's Flying Circus! 🐍"
    
    def calculate_expression(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Basic safety: only allow numbers, operators, and parentheses
            safe_expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            if not safe_expression:
                return "Please provide a valid mathematical expression."
            
            result = eval(safe_expression)
            return f"🧮 {expression} = {result}"
        
        except Exception as e:
            return f"Sorry, I couldn't calculate that expression: {str(e)}"
    
    def get_current_time(self) -> str:
        """Get current date and time"""
        now = datetime.now()
        return f"🕐 Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def respond(self, query: str) -> str:
        """Advanced response logic with structured query processing"""
        self.history.append(query)
        query_lower = query.lower().strip()
        
        # Handle history requests
        if "history" in query_lower:
            if len(self.history) > 1:
                return f"📋 Your recent queries:\n" + "\n".join(f"{i+1}. {q}" for i, q in enumerate(self.history[-6:-1]))
            else:
                return "No previous queries found."
        
        # Handle greetings
        if any(greeting in query_lower for greeting in ["hello", "hi", "hey"]):
            return (f"👋 Hello! I'm {self.name}, your advanced AI assistant. "
                   f"I can help with weather, currency rates, facts, calculations, and more!")
        
        # Handle help requests
        if "help" in query_lower:
            return ("🤖 I can help you with:\n"
                   "🌤️ Weather: 'weather in London'\n"
                   "💱 Currency: 'USD to EUR rate'\n"
                   "🧠 Facts: 'tell me a fact'\n"
                   "🧮 Math: 'calculate 15 * 8'\n"
                   "🕐 Time: 'what time is it?'\n"
                   "📋 History: 'show my history'")
        
        # Parse the structured query
        parsed_query = self.parse_structured_query(query)
        intent = parsed_query["intent"]
        entities = parsed_query["entities"]
        
        # Route to appropriate handler based on intent
        if intent == "weather":
            location = entities.get("location")
            if not location:
                # Try to extract location from the entire query
                words = query.split()
                for i, word in enumerate(words):
                    if word.lower() in ["in", "for", "at"] and i + 1 < len(words):
                        location = " ".join(words[i+1:]).strip("?.,!")
                        break
            
            if location:
                return self.get_weather_data(location)
            else:
                return "Please specify a location. Example: 'weather in Paris'"
        
        elif intent == "currency":
            from_currency = entities.get("from_currency")
            to_currency = entities.get("to_currency")
            if from_currency and to_currency:
                return self.get_currency_rate(from_currency, to_currency)
            else:
                return "Please specify currencies. Example: 'USD to EUR rate'"
        
        elif intent == "fact":
            return self.get_random_fact()
        
        elif intent == "calculation":
            expression = entities.get("expression")
            if not expression:
                # Try to extract mathematical expression
                math_match = re.search(r'[\d+\-*/().\s]+', query)
                if math_match:
                    expression = math_match.group(0)
            
            if expression:
                return self.calculate_expression(expression)
            else:
                return "Please provide a mathematical expression. Example: 'calculate 5 + 3'"
        
        elif intent == "time":
            return self.get_current_time()
        
        else:
            # Try to be helpful even with unknown queries
            return ("🤔 I'm not sure how to help with that specific request, but I can assist with:\n"
                   "Weather forecasts, currency rates, interesting facts, calculations, and current time.\n"
                   "Type 'help' to see examples!")

if __name__ == "__main__":
    # Create and test the advanced agent
    agent = AdvancedIntelligentAgent("AdvancedAgent")
    
    # Test complex queries
    test_queries = [
        "Hello there!",
        "What's the weather in Tokyo?",
        "USD to EUR exchange rate",
        "Tell me an interesting fact",
        "Calculate 25 * 4 + 10",
        "What time is it?",
        "Weather in New York City",
        "Convert 100 USD to GBP",
        "Random interesting information",
        "Show me my history",
        "Help me understand what you can do",
        "This is a complex query about something unknown"
    ]
    
    print(f"🤖 Testing {agent.name}")
    print("=" * 60)
    
    for query in test_queries:
        print(f"❓ Query: {query}")
        response = agent.respond(query)
        print(f"🤖 Response: {response}")
        print("-" * 40)
