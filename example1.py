"""
example1.py - Imperative routing, the pre-Router way.

`src/` uses `ft.Router` + `@ft.component`. This file shows the other option Flet
1.0 still supports: build `page.views` yourself and react to
`page.on_route_change`.

Everything here is plain Flet 1.0 syntax:
  * `page.navigate("/route")` instead of the removed `page.go()`
  * `ft.Button` instead of the removed `ft.ElevatedButton`

Run:  python example1.py
"""

import flet as ft


def main(page: ft.Page):
    page.title = "Routes example (imperative)"

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                appbar=ft.AppBar(title=ft.Text("Home")),
                controls=[
                    ft.Text("Home page"),
                    ft.Button(
                        "Visit store",
                        icon=ft.Icons.STORE,
                        on_click=lambda: page.navigate("/store"),
                    ),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    route="/store",
                    appbar=ft.AppBar(title=ft.Text("Store")),
                    controls=[
                        ft.Text("Store page"),
                        ft.Button(
                            "Go home",
                            icon=ft.Icons.HOME,
                            on_click=lambda: page.navigate("/"),
                        ),
                    ],
                )
            )
        # In components mode Flet updates for you; imperatively you must not.
        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        # The client popped the top view: drop it and restore the one below.
        if e.view is not None and len(page.views) > 1:
            page.views.remove(e.view)
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(ft.RouteChangeEvent(name="", control=page, route=page.route))


if __name__ == "__main__":
    ft.run(main)
