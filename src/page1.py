"""
page1.py - First content page
"""

import flet as ft

def Page1(page: ft.Page):
    """Creates Page 1 view"""
    shared_singleton = page.session.store.get("shared_singleton")
    
    # Store page-specific data in session
    if not page.session.store.get("page1_data"):
        page.session.store.set("page1_data", {
            "visit_count": 0,
            "user_input": "",
            "last_updated": None
        })
    
    # Increment visit count
    page1_data = page.session.store.get("page1_data")
    page1_data["visit_count"] += 1
    page.session.store.set("page1_data", page1_data)
    
    async def go_back(e):
        """Navigate back to homepage"""
        await page.push_route("/")
    
    async def go_forward(e):
        """Navigate forward to Page 2"""
        await page.push_route("/page2")
    
    def update_page_data(e):
        """Update page-specific data in session"""
        if user_input.value.strip():
            page1_data = page.session.store.get("page1_data")
            page1_data["user_input"] = user_input.value
            page1_data["last_updated"] = "Now"
            page.session.store.set("page1_data", page1_data)
            
            data_display.value = f"""
            Page 1 Session Data:
            - Visit Count: {page1_data['visit_count']}
            - User Input: {page1_data['user_input']}
            - Last Updated: {page1_data['last_updated']}
            """
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Page data updated in session!"),
                bgcolor=ft.Colors.BLUE_600
            )
            page.snack_bar.open = True
            page.update()
    
    def store_in_singleton(e):
        """Store data in shared singleton"""
        if user_input.value.strip():
            shared_singleton.store_data("page1_input", user_input.value)
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Data stored in shared singleton!"),
                bgcolor=ft.Colors.GREEN_600
            )
            page.snack_bar.open = True
            page.update()
    
    # Create UI controls
    title = ft.Text("Page 1: Content Management", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    subtitle = ft.Text("Demonstrates session data and shared object usage", size=16, color=ft.Colors.GREY_600)
    
    user_input = ft.TextField(
        label="Enter some data for this page",
        hint_text="Type something here...",
        border_color=ft.Colors.BLUE_400,
        filled=True,
        bgcolor=ft.Colors.WHITE,
        expand=True
    )
    
    data_display = ft.Text(
        f"""
        Page 1 Session Data:
        - Visit Count: {page1_data['visit_count']}
        - User Input: {page1_data['user_input']}
        - Last Updated: {page1_data['last_updated']}
        """,
        size=14,
        selectable=True
    )
    
    navigation_buttons = ft.Row(
        [
            ft.ElevatedButton("← Back to Home", icon=ft.Icons.ARROW_BACK, on_click=go_back, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)),
            ft.ElevatedButton("Forward to Page 2 →", icon=ft.Icons.ARROW_FORWARD, on_click=go_forward, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    action_buttons = ft.Row(
        [
            ft.ElevatedButton("Update Page Data", icon=ft.Icons.SAVE, on_click=update_page_data, style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)),
            ft.ElevatedButton("Store in Singleton", icon=ft.Icons.SHARE, on_click=store_in_singleton, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE))
        ],
        spacing=20
    )
    
    view = ft.View(
        route="/page1",
        controls=[
            ft.AppBar(
                title=ft.Text("Page 1", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back, tooltip="Back to Home")
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=20),
                        title, subtitle, ft.Container(height=30),
                        ft.Text("Data Input:", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([user_input], expand=True), ft.Container(height=20),
                        action_buttons, ft.Container(height=30),
                        ft.Card(content=ft.Container(content=ft.Column([ft.Text("Session Data", size=16, weight=ft.FontWeight.BOLD), data_display], spacing=10), padding=20), elevation=2),
                        ft.Container(height=30),
                        navigation_buttons
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