"""
main.py - Main application entry point and router

This is the core routing system that manages navigation between pages.
It handles:
- Route changes between different views/pages
- Session data management for sharing state
- Singleton object initialization
"""

import flet as ft
from shared_singleton import SharedSingleton  # Our shared singleton object

def main(page: ft.Page):
    """
    Main application entry point
    Sets up the page properties and handles routing between views
    """
    # Configure page properties
    page.title = "Flet Routing Template"
    page.theme_mode = ft.ThemeMode.LIGHT  # Light theme by default
    page.window_width = 1000
    page.window_height = 700
    page.padding = 0
    
    # Initialize shared singleton and store in page session
    # This object will be shared across all pages
    if not page.session.get("shared_singleton"):
        shared_singleton = SharedSingleton()
        page.session.set("shared_singleton", shared_singleton)
    
    # Initialize session data for our app
    # Session data persists across page navigations
    if not page.session.get("app_data"):
        page.session.set("app_data", {
            "user_preferences": {},
            "navigation_history": ["/"],
            "page_data": {}
        })
    
    def route_change(event):
        """
        Handles navigation between different pages/views
        
        This function is called whenever the route changes (e.g., page.go("/page1"))
        It clears existing views and creates the new view based on the route
        
        Routes:
        - "/": Homepage
        - "/page1": First content page
        - "/page2": Second content page
        - "/page3": Third content page
        """
        # Get the current route string from the page
        current_route = page.route
        print(f"Route changed to: {current_route}")
        
        # Clear existing views to start fresh
        page.views.clear()
        
        # Home page
        if current_route == "/":
            from homepage import HomePage
            homepage_view = HomePage(page)
            page.views.append(homepage_view)
            
        # Page 1
        elif current_route == "/page1":
            from page1 import Page1
            page1_view = Page1(page)
            page.views.append(page1_view)
            
        # Page 2
        elif current_route == "/page2":
            from page2 import Page2
            page2_view = Page2(page)
            page.views.append(page2_view)
            
        # Page 3
        elif current_route == "/page3":
            from page3 import Page3
            page3_view = Page3(page)
            page.views.append(page3_view)
            
        # If route doesn't match any known route, go to homepage
        else:
            print(f"Unknown route: {current_route}, redirecting to homepage")
            page.go("/")
            return
        
        # Update navigation history in session
        app_data = page.session.get("app_data") or {}
        if "navigation_history" not in app_data:
            app_data["navigation_history"] = []
        if current_route not in app_data["navigation_history"]:
            app_data["navigation_history"].append(current_route)
        page.session.set("app_data", app_data)
        
        # Update the page to show the new view
        page.update()
    
    def view_pop(view):
        """
        Handles back navigation when user clicks back button
        
        This function:
        1. Removes current view from stack
        2. Navigates to previous view in stack
        3. If no views left, goes to homepage
        """
        page.views.pop()  # Remove current view
        
        if page.views:
            # Go to previous view
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            # No views left, go to homepage
            page.go("/")
    
    # Register event handlers for routing
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Start the app at homepage
    page.go("/")

# Entry point - runs when script is executed directly
if __name__ == "__main__":
    # Start the Flet application
    ft.app(target=main)