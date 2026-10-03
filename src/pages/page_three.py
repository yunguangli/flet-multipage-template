"""
pages/page_three.py - ``/page-3``: a summary of the whole session, plus the
"start over" button that demonstrates resetting session storage.
"""

import flet as ft

from app_state import reset_session, use_app_state, use_visit
from ui import accent_button, button_row, heading, nav_row, toast, view

ROUTE = "/page-3"
ACCENT = ft.Colors.PURPLE_600


@ft.component
def PageThree() -> ft.View:
    state = use_app_state()
    use_visit(ROUTE)
    page = ft.context.page

    def restart() -> None:
        # Resets the models in place, so the pages still on the stack - and the
        # root App component - immediately show the cleared values.
        reset_session()
        page.navigate("/")
        toast("Session cleared - every counter is back to zero.", ft.Colors.RED_600)

    def export() -> None:
        # Stands in for "write it to a file / POST it to an API".
        print(state.snapshot())
        toast("Snapshot printed to the console.", ft.Colors.BLUE_600)

    summary = ft.Column(
        controls=[
            ft.Text("Navigation history", weight=ft.FontWeight.BOLD),
            ft.Text(
                " -> ".join(state.navigation_history) or "(empty)", selectable=True
            ),
            ft.Divider(height=1),
            ft.Text("App state", weight=ft.FontWeight.BOLD),
            ft.Text(f"Counter: {state.counter}", selectable=True),
            ft.Text(f"Stored items: {len(state.data_store)}", selectable=True),
            ft.Text(f"Data: {dict(state.data_store)}", selectable=True),
        ],
        tight=True,
    )

    return view(
        ROUTE,
        "Page 3",
        ACCENT,
        *heading(
            "Page 3: session summary",
            "Everything this session has seen so far.",
            ACCENT,
        ),
        ft.Container(height=25),
        ft.Card(content=ft.Container(content=summary, padding=25), elevation=4),
        ft.Container(height=30),
        ft.Text("Actions", weight=ft.FontWeight.BOLD),
        ft.Container(height=10),
        button_row(
            accent_button(
                "Reset session", ft.Icons.RESTART_ALT, ft.Colors.RED_600, restart
            ),
            accent_button(
                "Export snapshot", ft.Icons.DOWNLOAD, ft.Colors.BLUE_600, export
            ),
        ),
        ft.Container(height=30),
        nav_row(
            accent_button(
                "Page 2",
                ft.Icons.ARROW_BACK,
                ft.Colors.GREY_600,
                lambda: page.navigate("/page-2"),
            ),
            accent_button(
                "Back to home",
                ft.Icons.HOME,
                ft.Colors.ORANGE_600,
                lambda: page.navigate("/"),
            ),
        ),
        ft.Container(height=40),
        ft.Divider(height=1),
        ft.Container(height=10),
        ft.Text(
            f"{state.config.app_name} v{state.config.version}",
            size=12,
            color=ft.Colors.GREY_500,
            text_align=ft.TextAlign.CENTER,
        ),
    )
