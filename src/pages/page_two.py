"""
pages/page_two.py - ``/page-2``: a read-only dashboard over the shared state.

Every tile is rendered straight from ``AppState``, so any page that mutates the
model updates this page with no extra wiring.
"""

import flet as ft

from app_state import AppState, use_app_state, use_visit
from ui import accent_button, button_row, heading, nav_row, toast, view

ROUTE = "/page-2"
ACCENT = ft.Colors.GREEN_600


def _stat(label: str, value: str, accent: ft.Colors) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(label, size=12, color=ft.Colors.GREY_600),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=accent),
            ],
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.GREY_50,
        expand=True,
    )


def _state_dialog(state: AppState, close) -> ft.AlertDialog:
    stored = [
        ft.Text(f"{key} = {value}", selectable=True)
        for key, value in state.data_store.items()
    ]
    return ft.AlertDialog(
        title=ft.Text("Everything in app state"),
        content=ft.Column(
            controls=[
                ft.Text(f"Counter: {state.counter}", selectable=True),
                ft.Divider(height=1),
                ft.Text("Key/value store", weight=ft.FontWeight.BOLD),
                *(stored or [ft.Text("(empty)", italic=True)]),
                ft.Divider(height=1),
                ft.Text("Navigation history", weight=ft.FontWeight.BOLD),
                ft.Text(" -> ".join(state.navigation_history) or "(empty)"),
            ],
            scroll=ft.ScrollMode.AUTO,
            tight=True,
        ),
        actions=[ft.TextButton("Close", on_click=close)],
        on_dismiss=close,
    )


@ft.component
def PageTwo() -> ft.View:
    state = use_app_state()
    use_visit(ROUTE)
    page = ft.context.page

    show_data, set_show_data = ft.use_state(False)
    ft.use_dialog(
        _state_dialog(state, lambda: set_show_data(False)) if show_data else None
    )

    def reset_state() -> None:
        state.reset()
        toast("Counter and key/value store cleared.", ft.Colors.ORANGE_600)

    return view(
        ROUTE,
        "Page 2",
        ACCENT,
        *heading(
            "Page 2: shared state dashboard",
            "These tiles are rendered from AppState - mutate it anywhere.",
            ACCENT,
        ),
        ft.Container(height=30),
        ft.Row(
            controls=[
                _stat("Shared counter", str(state.counter), ft.Colors.BLUE_700),
                _stat("Stored items", str(len(state.data_store)), ACCENT),
                _stat("Version", state.config.version, ft.Colors.PURPLE_700),
            ],
            spacing=20,
        ),
        ft.Container(height=30),
        button_row(
            accent_button(
                "View all data",
                ft.Icons.DATA_USAGE,
                ft.Colors.BLUE_600,
                lambda: set_show_data(True),
            ),
            accent_button(
                "Reset app state", ft.Icons.REFRESH, ft.Colors.ORANGE_600, reset_state
            ),
        ),
        ft.Container(height=30),
        nav_row(
            accent_button(
                "Page 1",
                ft.Icons.ARROW_BACK,
                ft.Colors.GREY_600,
                lambda: page.navigate("/page-1"),
            ),
            accent_button(
                "Page 3",
                ft.Icons.ARROW_FORWARD,
                ACCENT,
                lambda: page.navigate("/page-3"),
            ),
        ),
    )
