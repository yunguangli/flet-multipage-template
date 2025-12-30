"""
main.py - Main application entry point and router
"""

import flet as ft
from shared_singleton import SharedSingleton
from homepage import HomePage
from page1 import Page1
from page2 import Page2
from page3 import Page3

def main(page: ft.Page):
    """
    Main application entry point
    Sets up the page properties and handles routing between views
    """
    # Configure page properties
    page.title = "Flet Routing Template"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 700
    page.padding = 0
    
    # Initialize shared singleton and store in page session
    if not page.session.store.get("shared_singleton"):
        page.session.store.set("shared_singleton", SharedSingleton())
    
    # Initialize session data for our app
    if not page.session.store.get("app_data"):
        page.session.store.set("app_data", {
            "user_preferences": {},
            "navigation_history": ["/"],
            "page_data": {}
        })
    
    def route_change():
        """
        Handles navigation between different pages/views
        """
        page.views.clear()
        
        # Always add homepage as base view
        homepage_view = HomePage(page)
        page.views.append(homepage_view)
        
        # Add additional views based on route
        if page.route == "/page1":
            page.views.append(Page1(page))
        elif page.route == "/page2":
            page.views.append(Page2(page))
        elif page.route == "/page3":
            page.views.append(Page3(page))
        elif page.route != "/":  # Unknown route
            page.route = "/"
            route_change()
            return
        
        # Update navigation history in session
        app_data = page.session.store.get("app_data") or {}
        nav_history = app_data.get("navigation_history", [])
        if page.route not in nav_history:
            nav_history.append(page.route)
            app_data["navigation_history"] = nav_history
            page.session.store.set("app_data", app_data)
        
        page.update()
    
    async def view_pop(e):
        """
        Handles back navigation when user clicks back button
        """
        if e.view is not None and len(page.views) > 1:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)
    
    # Register event handlers for routing
    page.route = "/"
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initial route setup
    route_change()

# Entry point - runs when script is executed directly
if __name__ == "__main__":
    ft.run(main)