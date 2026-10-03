"""
ui.py - The page-level building blocks shared by every page.

Nothing here hides Flet: these are thin wrappers around controls documented at
https://flet.dev/docs/controls/view that would otherwise be copy-pasted into
every page file. Add more helpers here as the app grows.
"""

from __future__ import annotations

import flet as ft

CONTENT_PADDING = 30


def view(
    route: str,
    title: str,
    accent: ft.Colors,
    *controls: ft.Control,
    **kwargs: object,
) -> ft.View:
    """Build a page-level ``View``: app bar + padded, scrollable content.

    A ``View`` behaves like a ``Column``, so the scrolling and the padding are
    set on the view itself instead of on a nested container.

    There is no explicit back button: with ``manage_views=True`` the Router
    returns one ``View`` per route level, and Flet inserts the implicit back
    arrow on every view that can be popped. Only the root view opts out, by
    passing ``can_pop=False``.

    Extra keyword arguments are forwarded to ``ft.View``, which is how a page
    opts out of the implicit back arrow.
    """
    return ft.View(
        route=route,
        appbar=ft.AppBar(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            bgcolor=accent,
            color=ft.Colors.WHITE,
        ),
        padding=ft.Padding.all(CONTENT_PADDING),
        scroll=ft.ScrollMode.AUTO,
        controls=list(controls),
        **kwargs,
    )


def heading(title: str, subtitle: str, accent: ft.Colors) -> list[ft.Control]:
    """The title/subtitle pair every page opens with."""
    return [
        ft.Text(title, size=28, weight=ft.FontWeight.BOLD, color=accent),
        ft.Text(subtitle, size=15, color=ft.Colors.GREY_600),
    ]


def button_row(*buttons: ft.Control) -> ft.Row:
    """A centred, wrapping row of action buttons."""
    return ft.Row(
        controls=list(buttons),
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        wrap=True,
    )


def nav_row(*buttons: ft.Control) -> ft.Row:
    """A row of navigation buttons, first one left-aligned, last one right."""
    return ft.Row(
        controls=list(buttons),
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def toast(message: str, accent: ft.Colors | None = None) -> None:
    """Show a transient snack bar.

    Snack bars are one-shot notifications, so this is the one place where the
    imperative ``page.show_dialog()`` is a better fit than the declarative
    ``ft.use_dialog()`` hook that real dialogs use.
    """
    ft.context.page.show_dialog(ft.SnackBar(content=ft.Text(message), bgcolor=accent))


def accent_button(
    label: str,
    icon: ft.IconData,
    accent: ft.Colors,
    on_click,
) -> ft.Button:
    """A filled button in the page's accent colour."""
    return ft.Button(
        label,
        icon=icon,
        bgcolor=accent,
        color=ft.Colors.WHITE,
        on_click=on_click,
    )
