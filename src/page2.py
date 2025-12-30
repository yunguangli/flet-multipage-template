"""
page2.py - Second content page
"""

import flet as ft

def Page2(page: ft.Page):
    """Creates Page 2 view"""
    shared_singleton = page.session.store.get("shared_singleton")
    
    async def go_back(e):
        """Navigate back to Page 1"""
        await page.push_route("/page1")
    
    async def go_forward(e):
        """Navigate forward to Page 3"""
        await page.push_route("/page3")
    
    def get_all_data(e):
        """Retrieve and display all stored data"""
        singleton_data = shared_singleton.to_dict()
        page1_data = page.session.store.get("page1_data") or {}
        
        data_dialog = ft.AlertDialog(
            title=ft.Text("All Stored Data"),
            content=ft.Column([
                ft.Text("Shared Singleton Data:", weight=ft.FontWeight.BOLD),
                ft.Text(f"Counter: {singleton_data['counter']}"),
                ft.Text(f"Data Store: {singleton_data['data_store']}"),
                ft.Text(f"Config: {singleton_data['config']}"),
                ft.Divider(),
                ft.Text("Page 1 Session Data:", weight=ft.FontWeight.BOLD),
                ft.Text(str(page1_data)),
            ], scroll=ft.ScrollMode.AUTO, height=300),
            actions=[ft.TextButton("Close", on_click=lambda e: page.close(data_dialog))]
        )
        page.open(data_dialog)
    
    def reset_counter(e):
        """Demonstrate modifying singleton - reset counter"""
        new_singleton = type(shared_singleton)()
        page.session.store.set("shared_singleton", new_singleton)
        page.snack_bar = ft.SnackBar(content=ft.Text("Singleton counter reset!"), bgcolor=ft.Colors.ORANGE_600)
        page.snack_bar.open = True
        page.update()
    
    # Create UI controls
    title = ft.Text("Page 2: Data Viewer", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    
    stats = ft.Row(
        [
            ft.Container(
                content=ft.Column([ft.Text("Singleton Counter", size=12, color=ft.Colors.GREY_600), ft.Text(str(shared_singleton.get_counter()), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, border_radius=10, bgcolor=ft.Colors.BLUE_50, expand=True
            ),
            ft.Container(
                content=ft.Column([ft.Text("Stored Items", size=12, color=ft.Colors.GREY_600), ft.Text(str(len(shared_singleton.data_store)), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, border_radius=10, bgcolor=ft.Colors.GREEN_50, expand=True
            ),
            ft.Container(
                content=ft.Column([ft.Text("App Version", size=12, color=ft.Colors.GREY_600), ft.Text(shared_singleton.config["version"], size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, border_radius=10, bgcolor=ft.Colors.PURPLE_50, expand=True
            )
        ],
        spacing=20
    )
    
    view = ft.View(
        route="/page2",
        controls=[
            ft.AppBar(
                title=ft.Text("Page 2", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back, tooltip="Back to Page 1")
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=20),
                        title,
                        ft.Text("View and manage application data", size=16, color=ft.Colors.GREY_600),
                        ft.Container(height=30),
                        stats,
                        ft.Container(height=30),
                        ft.Row(
                            [
                                ft.ElevatedButton("View All Data", icon=ft.Icons.DATA_USAGE, on_click=get_all_data, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, padding=ft.padding.symmetric(horizontal=30, vertical=15))),
                                ft.ElevatedButton("Reset Counter", icon=ft.Icons.REFRESH, on_click=reset_counter, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE, padding=ft.padding.symmetric(horizontal=30, vertical=15)))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        ft.Container(height=40),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("Navigation Help", size=18, weight=ft.FontWeight.BOLD),
                                    ft.ListTile(leading=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_600), title=ft.Text("Back Button"), subtitle=ft.Text("In app bar or below - goes to previous page")),
                                    ft.ListTile(leading=ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.GREEN_600), title=ft.Text("Forward Button"), subtitle=ft.Text("Below - goes to next page")),
                                    ft.ListTile(leading=ft.Icon(ft.Icons.HOME, color=ft.Colors.ORANGE_600), title=ft.Text("Home"), subtitle=ft.Text("Use browser back or navigate via buttons"))
                                ]),
                                padding=20
                            )
                        ),
                        ft.Container(height=30),
                        ft.Row(
                            [
                                ft.ElevatedButton("← Back to Page 1", icon=ft.Icons.ARROW_BACK, on_click=go_back, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)),
                                ft.ElevatedButton("Forward to Page 3 →", icon=ft.Icons.ARROW_FORWARD, on_click=go_forward, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE))
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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