"""
page3.py - Third content page

Demonstrates:
- Final page in navigation flow
- Summary of data collected
- Options to return or restart
"""

import flet as ft

def Page3(page: ft.Page):
    """
    Creates Page 3 view
    """
    
    # Access shared singleton
    shared_singleton = page.session.get("shared_singleton")
    
    def go_back(e):
        """Navigate back to Page 2"""
        page.go("/page2")
    
    def go_home(e):
        """Navigate back to homepage"""
        page.go("/")
    
    def restart_app(e):
        """
        Demonstrates clearing session data and restarting
        """
        # Clear all session data (except shared_singleton)
        page.session.clear()
        
        # Reinitialize shared singleton
        from shared_singleton import SharedSingleton
        new_singleton = SharedSingleton()
        page.session.set("shared_singleton", new_singleton)
        
        # Initialize app data
        page.session.set("app_data", {
            "user_preferences": {},
            "navigation_history": ["/"],
            "page_data": {}
        })
        
        # Go to homepage
        page.go("/")
        
        # Show message
        page.snack_bar = ft.SnackBar(
            content=ft.Text("App restarted! All data cleared."),
            bgcolor=ft.Colors.RED_600
        )
        page.snack_bar.open = True
    
    # Get navigation history
    app_data = page.session.get("app_data") or {}
    navigation_history = app_data.get("navigation_history", [])
    
    # Create summary
    summary = f"""
    Application Summary:
    
    Pages Visited: {len(navigation_history)}
    Navigation Path: {" → ".join(navigation_history)}
    
    Shared Singleton Stats:
    - Counter Value: {shared_singleton.get_counter()}
    - Data Items Stored: {len(shared_singleton.data_store)}
    - Data: {shared_singleton.data_store}
    
    Session Data:
    - Page 1 Visits: {(page.session.get('page1_data') or {}).get('visit_count', 0)}
    - Navigation History: {navigation_history}
    """
    
    # Create UI controls
    title = ft.Text(
        "Page 3: Summary & Actions",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_700
    )
    
    summary_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Session Summary", size=20, weight=ft.FontWeight.BOLD, 
                       color=ft.Colors.PURPLE_600),
                ft.Text(summary, size=14, selectable=True)
            ], spacing=15),
            padding=25
        ),
        elevation=4
    )
    
    # Create the view
    view = ft.View(
        "/page3",
        [
            ft.AppBar(
                title=ft.Text("Page 3", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.PURPLE_600,
                color=ft.Colors.WHITE,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=go_back,
                    tooltip="Back to Page 2"
                )
            ),
            
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=20),
                        title,
                        ft.Text("Final page with application summary", 
                               size=16, color=ft.Colors.GREY_600),
                        ft.Container(height=30),
                        
                        summary_card,
                        ft.Container(height=30),
                        
                        ft.Text("Actions:", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Restart Application",
                                    icon=ft.Icons.RESTART_ALT,
                                    on_click=restart_app,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.RED_600,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Export Data",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: print("Export data functionality"),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE_600,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        ft.Container(height=40),
                        
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "← Back to Page 2",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=go_back,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREY_600,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                                    )
                                ),
                                ft.ElevatedButton(
                                    "🏠 Return to Home",
                                    icon=ft.Icons.HOME,
                                    on_click=go_home,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.ORANGE_600,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        
                        # Footer
                        ft.Container(
                            content=ft.Column([
                                ft.Divider(),
                                ft.Row([
                                    ft.Text("Flet Routing Template v1.0", color=ft.Colors.GREY_500),
                                    ft.Text("•", color=ft.Colors.GREY_500),
                                    ft.Text("Educational Purpose", color=ft.Colors.GREY_500),
                                    ft.Text("•", color=ft.Colors.GREY_500),
                                    ft.Text("Beginner Friendly", color=ft.Colors.GREY_500)
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                            ]),
                            padding=ft.padding.only(top=40)
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=30,
                expand=True
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    return view