# Simple AI Agent that returns predefined messages
class SimpleAgent:
    def __init__(self, name: str):
        self.name = name
        self.responses = {
            "hello": "Hello! I'm a simple AI agent. How can I help you today?",
            "goodbye": "Goodbye! Have a great day!",
            "help": "I can respond to 'hello', 'goodbye', and 'help' commands.",
            "default": "I'm sorry, I don't understand that command. Try 'help' for available commands."
        }
    
    def respond(self, query: str) -> str:
        """Respond to a query with a predefined message"""
        query_lower = query.lower().strip()
        
        if "hello" in query_lower or "hi" in query_lower:
            return self.responses["hello"]
        elif "goodbye" in query_lower or "bye" in query_lower:
            return self.responses["goodbye"]
        elif "help" in query_lower:
            return self.responses["help"]
        else:
            return self.responses["default"]

if __name__ == "__main__":
    # Create and test the agent
    agent = SimpleAgent("SimpleAgent")
    
    # Test different inputs
    test_queries = ["Hello", "help", "goodbye", "unknown command"]
    
    for query in test_queries:
        response = agent.respond(query)
        print(f"Query: '{query}' -> Response: '{response}'")
