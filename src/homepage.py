"""
homepage.py - Home page with welcome message and navigation

This demonstrates:
- Basic page layout with Flet controls
- Navigation to other pages using page.go()
- Accessing session data and singleton
"""

import flet as ft

def HomePage(page: ft.Page):
    """
    Creates the homepage view
    
    Args:
        page: The Flet page object containing session and navigation methods
    
    Returns:
        ft.View: The homepage view with welcome message and navigation button
    """
    
    # Access the shared singleton from session
    shared_singleton = page.session.get("shared_singleton")
    
    def go_to_page1(e):
        """
        Navigation function - triggered when button is clicked
        
        Uses page.go() to navigate to a new route
        The route_change handler in main.py will handle the actual navigation
        """
        print("Navigating to Page 1")
        page.go("/page1")
    
    def update_counter(e):
        """
        Demonstrates modifying the shared singleton
        """
        new_count = shared_singleton.increment_counter()
        counter_text.value = f"Shared Counter: {new_count}"
        
        # Show feedback
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Counter incremented to {new_count}!"),
            bgcolor=ft.Colors.GREEN_600
        )
        page.snack_bar.open = True
        page.update()
    
    def show_session_info(e):
        """
        Demonstrates accessing and displaying session data
        """
        # Get app data from session
        app_data = page.session.get("app_data") or {}
        
        # Create dialog with session info
        session_info = ft.AlertDialog(
            title=ft.Text("Session Information"),
            content=ft.Column([
                ft.Text(f"Navigation History: {', '.join(app_data.get('navigation_history', []))}"),
                ft.Text(f"Singleton Counter: {shared_singleton.get_counter()}"),
                ft.Text(f"Singleton Config: {shared_singleton.get_config()}"),
            ], scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Close", on_click=lambda e: page.close(session_info))
            ]
        )
        
        page.open(session_info)
    
    # Create UI controls
    title = ft.Text(
        "Welcome to Flet Routing Template",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700
    )
    
    subtitle = ft.Text(
        "A simple multi-page routing skeleton for Flet applications",
        size=16,
        color=ft.Colors.GREY_600
    )
    
    counter_text = ft.Text(
        f"Shared Counter: {shared_singleton.get_counter()}",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_700
    )
    
    # Create buttons
    buttons = ft.Row(
        [
            ft.ElevatedButton(
                "Go to Page 1",
                icon=ft.Icons.ARROW_FORWARD,
                on_click=go_to_page1,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            ft.ElevatedButton(
                "Increment Counter",
                icon=ft.Icons.ADD,
                on_click=update_counter,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            ft.ElevatedButton(
                "Show Session Info",
                icon=ft.Icons.INFO,
                on_click=show_session_info,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    # Features list
    features = ft.Column(
        [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600),
                title=ft.Text("Simple Multi-Page Routing"),
                subtitle=ft.Text("Easy navigation between pages using routes")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600),
                title=ft.Text("Session State Management"),
                subtitle=ft.Text("Share data between pages using page.session")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600),
                title=ft.Text("Singleton Object Pattern"),
                subtitle=ft.Text("Shared object instance across all pages")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600),
                title=ft.Text("Navigation History"),
                subtitle=ft.Text("Track user navigation in session data")
            ),
        ]
    )
    
    # Create the view
    view = ft.View(
        "/",  # Route for this view
        [
            # App bar with title
            ft.AppBar(
                title=ft.Text("Home", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                center_title=True
            ),
            
            # Main content
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=40),  # Spacing
                        title,
                        subtitle,
                        ft.Container(height=40),
                        counter_text,
                        ft.Container(height=20),
                        buttons,
                        ft.Container(height=40),
                        ft.Divider(height=1),
                        ft.Text("Features:", size=20, weight=ft.FontWeight.BOLD),
                        features
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=ft.padding.all(30),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    return view