"""
pages/not_found.py - Rendered by ``ft.Router`` when no route matches.

Two things to know about this slot:

* With ``manage_views=True`` the Router wraps whatever ``not_found`` returns in
  a ``View`` of its own, so this component returns plain controls, not a View.
* The Router invokes ``not_found`` directly rather than mounting it as a route
  component, so the route hooks (``ft.use_route_location()``) are not available
  here. ``ft.context.page.route`` carries the same information.
"""

import flet as ft

from ui import CONTENT_PADDING, accent_button

ACCENT = ft.Colors.GREY_700


@ft.component
def NotFound() -> ft.Container:
    page = ft.context.page

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=40),
                ft.Text(
                    "404",
                    size=64,
                    weight=ft.FontWeight.BOLD,
                    color=ACCENT,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"No route matches {page.route!r}.",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                accent_button(
                    "Back to home",
                    ft.Icons.HOME,
                    ACCENT,
                    lambda: page.navigate("/"),
                ),
                ft.Container(height=30),
                ft.Text(
                    "Add an ft.Route for this path in main.py to serve it.",
                    size=12,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        ),
        padding=ft.Padding.all(CONTENT_PADDING),
        expand=True,
    )
