"""
pages/home.py - The landing page (``/``).

Demonstrates: shared state via context, a declarative dialog, and a snack bar.
"""

import flet as ft

from app_state import AppState, use_app_state, use_visit
from ui import accent_button, button_row, heading, toast, view

ROUTE = "/"
ACCENT = ft.Colors.BLUE_600

FEATURES = [
    (
        ft.Icons.ROUTE,
        "Declarative routing",
        "ft.Router + ft.Route, one View per route level",
    ),
    (
        ft.Icons.INSTALL_MOBILE,
        "Real back navigation",
        "Swipe back, system back, app bar arrow",
    ),
    (
        ft.Icons.DATA_OBJECT,
        "Observable state",
        "Dataclasses that re-render exactly the pages that read them",
    ),
    (
        ft.Icons.LOCK,
        "Session storage",
        "page.session.store for state outside the component tree",
    ),
    (
        ft.Icons.HISTORY,
        "Navigation history",
        "Recorded automatically whenever a page is shown",
    ),
]


def _feature_list() -> ft.Column:
    return ft.Column(
        controls=[
            ft.ListTile(
                leading=ft.Icon(icon, color=ACCENT),
                title=ft.Text(title),
                subtitle=ft.Text(subtitle),
            )
            for icon, title, subtitle in FEATURES
        ],
        tight=True,
    )


def _session_info_dialog(state: AppState, close) -> ft.AlertDialog:
    """Built from live state, so it always shows the current values."""
    return ft.AlertDialog(
        title=ft.Text("Session information"),
        content=ft.Column(
            controls=[
                ft.Text("Navigation history", weight=ft.FontWeight.BOLD),
                ft.Text(" -> ".join(state.navigation_history) or "(empty)"),
                ft.Divider(height=1),
                ft.Text("App-wide state", weight=ft.FontWeight.BOLD),
                ft.Text(f"Counter: {state.counter}"),
                ft.Text(f"Stored items: {len(state.data_store)}"),
                ft.Text(f"{state.config.app_name} v{state.config.version}"),
            ],
            scroll=ft.ScrollMode.AUTO,
            tight=True,
        ),
        actions=[ft.TextButton("Close", on_click=close)],
        on_dismiss=close,
    )


@ft.component
def Home() -> ft.View:
    state = use_app_state()
    use_visit(ROUTE)
    page = ft.context.page

    # Declarative dialog: `show_info` is the single source of truth. Rendering
    # `None` hides it, so there is no "close" bookkeeping to forget.
    show_info, set_show_info = ft.use_state(False)
    ft.use_dialog(
        _session_info_dialog(state, lambda: set_show_info(False)) if show_info else None
    )

    def increment_counter() -> None:
        toast(f"Counter is now {state.increment_counter()}", ACCENT)

    return view(
        ROUTE,
        "Home",
        ACCENT,
        *heading(
            "Welcome to the Flet multi-page template",
            "A declarative starting point for multi-page Flet apps.",
            ACCENT,
        ),
        ft.Container(height=30),
        ft.Text(
            f"Shared counter: {state.counter}",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700,
        ),
        ft.Container(height=20),
        button_row(
            accent_button(
                "Go to page 1",
                ft.Icons.ARROW_FORWARD,
                ACCENT,
                lambda: page.navigate("/page-1"),
            ),
            accent_button(
                "Increment counter",
                ft.Icons.ADD,
                ft.Colors.GREEN_600,
                increment_counter,
            ),
            accent_button(
                "Session info",
                ft.Icons.INFO,
                ft.Colors.PURPLE_600,
                lambda: set_show_info(True),
            ),
        ),
        ft.Container(height=30),
        ft.Divider(height=1),
        ft.Text("What this template shows", weight=ft.FontWeight.BOLD),
        _feature_list(),
        # This view is the bottom of the stack: Flet must not offer a back arrow.
        can_pop=False,
    )
