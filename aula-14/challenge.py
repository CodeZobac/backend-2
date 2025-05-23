# Enhanced AI Agent with keyword-based responses
import re
from typing import Dict, List

class EnhancedAgent:
    def __init__(self, name: str):
        self.name = name
        self.keyword_responses = {
            "weather": "I can't check the weather right now, but you should check your local weather service!",
            "time": "I don't have access to real-time data, but you can check your system clock.",
            "name": f"My name is {name}, I'm an AI agent designed to help you!",
            "age": "As an AI, I don't have an age in the traditional sense.",
            "programming": "I love talking about programming! Python is a great language to start with.",
            "python": "Python is an excellent programming language! It's readable, versatile, and has great libraries.",
            "ai": "Artificial Intelligence is fascinating! I'm a simple example of AI in action.",
            "help": "I can respond to various topics like weather, time, programming, Python, AI, and more!",
            "joke": "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "math": "I can help with basic math concepts! What would you like to know?",
            "learn": "Learning is great! I recommend starting with fundamentals and practicing regularly.",
        }
        
        # Greetings and farewells
        self.greetings = ["hello", "hi", "hey", "greetings"]
        self.farewells = ["goodbye", "bye", "see you", "farewell"]
        
        self.default_responses = [
            "That's interesting! Tell me more.",
            "I'm not sure about that, but I'm here to help!",
            "Could you rephrase that? I want to understand better.",
            "That's a great question! I'm still learning about that topic."
        ]
    
    def respond(self, query: str) -> str:
        """Enhanced response logic with keyword detection"""
        query_lower = query.lower().strip()
        
        # Check for greetings
        for greeting in self.greetings:
            if greeting in query_lower:
                return f"Hello! I'm {self.name}, your AI assistant. How can I help you today?"
        
        # Check for farewells
        for farewell in self.farewells:
            if farewell in query_lower:
                return "Goodbye! It was great talking with you. Come back anytime!"
        
        # Check for keywords in the query
        for keyword, response in self.keyword_responses.items():
            if keyword in query_lower:
                return response
        
        # Check for questions
        if "?" in query or any(word in query_lower for word in ["what", "how", "why", "when", "where", "who"]):
            return "That's a great question! While I'm still learning, I'm here to help as best I can."
        
        # Default response with some variety
        import random
        return random.choice(self.default_responses)
    
    def get_capabilities(self) -> List[str]:
        """Return a list of topics the agent can discuss"""
        return list(self.keyword_responses.keys())

if __name__ == "__main__":
    # Create and test the enhanced agent
    agent = EnhancedAgent("EnhancedAgent")
    
    # Test different types of queries
    test_queries = [
        "Hello there!",
        "What's the weather like?",
        "Tell me about Python programming",
        "How old are you?",
        "Can you tell me a joke?",
        "What is artificial intelligence?",
        "I want to learn programming",
        "Random text that doesn't match keywords",
        "Why is the sky blue?",
        "Goodbye!"
    ]
    
    print(f"Testing {agent.name}")
    print("=" * 50)
    
    for query in test_queries:
        response = agent.respond(query)
        print(f"Q: {query}")
        print(f"A: {response}")
        print("-" * 30)
    
    print(f"\nAgent capabilities: {', '.join(agent.get_capabilities())}")
