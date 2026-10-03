"""
example3.py - Imperative nested routes: two levels of `/settings`.

Run:  python example3.py
"""

import flet as ft

SETTINGS = "/settings"
MAIL_SETTINGS = "/settings/mail"


def main(page: ft.Page):
    page.title = "Nested routes example (imperative)"

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        page.views.append(
            ft.View(
                route="/",
                appbar=ft.AppBar(title=ft.Text("Home")),
                controls=[
                    ft.Text("Home page"),
                    ft.Button(
                        "Open settings",
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda: page.navigate(SETTINGS),
                    ),
                ],
            )
        )

        # /settings and /settings/mail both keep the settings view underneath.
        if page.route in (SETTINGS, MAIL_SETTINGS):
            page.views.append(
                ft.View(
                    route=SETTINGS,
                    appbar=ft.AppBar(title=ft.Text("Settings")),
                    controls=[
                        ft.Text("Settings", theme_style=ft.TextThemeStyle.BODY_LARGE),
                        ft.Button(
                            content="Open mail settings",
                            icon=ft.Icons.MAIL,
                            on_click=lambda: page.navigate(MAIL_SETTINGS),
                        ),
                    ],
                )
            )

        if page.route == MAIL_SETTINGS:
            page.views.append(
                ft.View(
                    route=MAIL_SETTINGS,
                    appbar=ft.AppBar(title=ft.Text("Mail settings")),
                    controls=[ft.Text("Mail settings!")],
                )
            )

        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None and len(page.views) > 1:
            page.views.remove(e.view)
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(ft.RouteChangeEvent(name="", control=page, route=page.route))


if __name__ == "__main__":
    ft.run(main)
