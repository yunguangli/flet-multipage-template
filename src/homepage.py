"""
homepage.py - Home page with welcome message and navigation
"""

import flet as ft

def HomePage(page: ft.Page):
    """
    Creates the homepage view
    """
    # Access the shared singleton from session
    shared_singleton = page.session.store.get("shared_singleton")
    
    async def go_to_page1(e):
        """Navigation function"""
        await page.push_route("/page1")
    
    def update_counter(e):
        """Demonstrates modifying the shared singleton"""
        new_count = shared_singleton.increment_counter()
        counter_text.value = f"Shared Counter: {new_count}"
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Counter incremented to {new_count}!"),
            bgcolor=ft.Colors.GREEN_600
        )
        page.snack_bar.open = True
        page.update()
    
    def show_session_info(e):
        """Demonstrates accessing and displaying session data"""
        app_data = page.session.store.get("app_data") or {}
        
        # Define close handler first
        def close_dialog(e):
            session_info.open = False
            page.update()
        
        session_info = ft.AlertDialog(
            title=ft.Text("Session Information"),
            content=ft.Column([
                ft.Text(f"Navigation History: {', '.join(app_data.get('navigation_history', []))}"),
                ft.Text(f"Singleton Counter: {shared_singleton.get_counter()}"),
                ft.Text(f"Singleton Config: {shared_singleton.get_config()}"),
            ], scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ]
        )
        
        # Show dialog using correct Flet 0.80.0 API
        page.dialog = session_info
        session_info.open = True
        page.update()
    
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
    
    # FIXED: Use keyword arguments for ft.View constructor
    view = ft.View(
        route="/",
        controls=[
            ft.AppBar(
                title=ft.Text("Home", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                center_title=True
            ),
            
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=40),
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