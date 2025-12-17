"""
shared_singleton.py - Singleton class for sharing data between pages

This demonstrates how to create a singleton that can be accessed from all pages.
In a real application, this could be:
- A database connection
- An AI model instance
- Configuration settings
- User session data
"""

class SharedSingleton:
    """
    A singleton class that maintains shared state across all pages.
    
    Singleton Pattern: Ensures only one instance exists throughout the app.
    This is stored in page.session for easy access from any page.
    
    Usage Example:
        # Get the singleton from page session
        shared_obj = page.session.get("shared_singleton")
        # Use it
        shared_obj.increment_counter()
    """
    
    def __init__(self):
        """
        Initialize the singleton with default values
        """
        self.counter = 0  # Example: A counter to demonstrate state persistence
        self.data_store = {}  # Example: A dictionary to store arbitrary data
        self.config = {
            "app_name": "Flet Routing Template",
            "version": "1.0.0",
            "debug_mode": True
        }
        
        print("SharedSingleton initialized")
    
    def increment_counter(self):
        """
        Example method to demonstrate state modification
        """
        self.counter += 1
        return self.counter
    
    def get_counter(self):
        """
        Example method to demonstrate state retrieval
        """
        return self.counter
    
    def store_data(self, key, value):
        """
        Store data in the singleton's data store
        """
        self.data_store[key] = value
    
    def get_data(self, key):
        """
        Retrieve data from the singleton's data store
        """
        return self.data_store.get(key)
    
    def get_config(self):
        """
        Get configuration
        """
        return self.config.copy()
    
    def to_dict(self):
        """
        Convert singleton state to dictionary for debugging
        """
        return {
            "counter": self.counter,
            "data_store": self.data_store,
            "config": self.config
        }