"""
main.py - Entry point, page setup and the route table.

Flet 1.0 renders this app through the *component* API. ``main()`` only configures
the ``Page``; everything the user sees comes from the ``App`` component, which is
a ``ft.Router`` plus a tree of ``ft.Route`` definitions. There is no manual
``page.views.append(...)`` / ``on_route_change`` bookkeeping any more.

Run with::

    python main.py          # desktop app
    python main.py --web    # browser
"""

import flet as ft

from app_state import AppStateContext, get_app_state
from pages import home, not_found, page_one, page_three, page_two

APP_TITLE = "Flet Multi-Page Template"


@ft.component
def App() -> ft.View:
    """Root component: owns the session state and renders the route table.

    ``ft.use_state`` is passed the *getter*, not an instance, so the model is
    created once - on the first render - and then kept for the lifetime of this
    component, which is the lifetime of the user session.
    """
    state, _ = ft.use_state(get_app_state)

    # Everything created inside the provider callback - the Router and every
    # Route component below it - can call `use_app_state()`.
    return AppStateContext(
        state,
        lambda: ft.Router(
            routes=[
                # A pathless root route adds no URL segment but always sits at
                # the bottom of the view stack, giving every other page
                # something to pop back to.
                ft.Route(
                    component=home.Home,
                    children=[
                        ft.Route(path="page-1", component=page_one.PageOne),
                        ft.Route(path="page-2", component=page_two.PageTwo),
                        ft.Route(path="page-3", component=page_three.PageThree),
                    ],
                )
            ],
            not_found=not_found.NotFound,
            # Emit one View per route level instead of a single control tree.
            # This is what enables the app bar back arrow, swipe-back on mobile
            # and the system back button - all handled by Flet, no code.
            manage_views=True,
        ),
    )


def main(page: ft.Page) -> None:
    """Flet entry point. Runs once per user session."""
    page.title = APP_TITLE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.padding = 0
    page.window.width = 1000
    page.window.height = 700

    page.render_views(App)


if __name__ == "__main__":
    ft.run(main)
