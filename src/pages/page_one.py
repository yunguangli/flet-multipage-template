"""
pages/page_one.py - ``/page-1``: page-scoped state that survives navigation.

Demonstrates: ``ft.use_state`` seeded from the session store, so the draft is
still there when the user navigates away and comes back.
"""

import flet as ft

from app_state import PageOneDraft, use_app_state, use_page_one_draft, use_visit
from ui import accent_button, button_row, heading, nav_row, toast, view

ROUTE = "/page-1"
ACCENT = ft.Colors.BLUE_600


def _count_visit(draft: PageOneDraft) -> None:
    draft.visits += 1


def _draft_summary(draft: PageOneDraft) -> ft.Card:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Page state", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Visits: {draft.visits}"),
                    ft.Text(f"Draft: {draft.text or '(empty)'}"),
                    ft.Text(f"Saved at: {draft.saved_at or '(never)'}"),
                ],
                tight=True,
            ),
            padding=20,
        ),
        elevation=2,
    )


@ft.component
def PageOne() -> ft.View:
    state = use_app_state()
    draft = use_page_one_draft()
    use_visit(ROUTE)
    page = ft.context.page

    # Side effects belong in effects: this runs once per mount, not on every
    # keystroke that re-renders the page.
    ft.use_effect(lambda: _count_visit(draft), [])

    def save_locally() -> None:
        if not draft.text.strip():
            return
        draft.saved_at = "just now"
        toast("Saved to the page's own state.", ACCENT)

    def save_globally() -> None:
        if not draft.text.strip():
            return
        state.store_data(ROUTE, draft.text)
        toast("Saved to the shared app state.", ft.Colors.GREEN_600)

    return view(
        ROUTE,
        "Page 1",
        ACCENT,
        *heading(
            "Page 1: page-scoped state",
            "Type something, save it, navigate away and come back.",
            ACCENT,
        ),
        ft.Container(height=25),
        ft.TextField(
            label="Draft text",
            hint_text="Survives navigation, but not a page reload",
            value=draft.text,
            filled=True,
            # `border` replaces the deprecated `border_color` in Flet 1.0.
            border=ft.OutlineInputBorder(side=ft.BorderSide(color=ft.Colors.BLUE_400)),
            # Writing straight to the observable model is enough: the component
            # subscribed to it in `use_page_one_draft()` and re-renders.
            on_change=lambda e: setattr(draft, "text", e.control.value),
        ),
        ft.Container(height=20),
        button_row(
            accent_button(
                "Save to page state", ft.Icons.SAVE, ft.Colors.PURPLE_600, save_locally
            ),
            accent_button(
                "Save to app state", ft.Icons.SHARE, ft.Colors.GREEN_600, save_globally
            ),
        ),
        ft.Container(height=25),
        _draft_summary(draft),
        ft.Container(height=30),
        nav_row(
            accent_button(
                "Back to home",
                ft.Icons.ARROW_BACK,
                ft.Colors.GREY_600,
                lambda: page.navigate("/"),
            ),
            accent_button(
                "Page 2",
                ft.Icons.ARROW_FORWARD,
                ACCENT,
                lambda: page.navigate("/page-2"),
            ),
        ),
    )
