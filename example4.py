"""
example4.py - A `NavigationDrawer` per view, kept in sync with the current route.

Run:  python example4.py
"""

import flet as ft

ROUTES = ["/", "/store", "/about"]


def _drawer(selected_index: int, on_change) -> ft.NavigationDrawer:
    return ft.NavigationDrawer(
        selected_index=selected_index,
        on_change=on_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Home",
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
            ),
            ft.Divider(height=1),
            ft.NavigationDrawerDestination(
                label="Store",
                icon=ft.Icons.STORE_OUTLINED,
                selected_icon=ft.Icons.STORE,
            ),
            ft.NavigationDrawerDestination(
                label="About",
                icon=ft.Icons.INFO_OUTLINED,
                selected_icon=ft.Icons.INFO,
            ),
        ],
    )


def _view(title: str, selected_index: int, *controls) -> ft.View:
    def on_drawer_change(e: ft.ControlEvent):
        e.control.page.navigate(ROUTES[e.control.selected_index])

    def open_drawer(e: ft.ControlEvent):
        # `show_drawer()` is async, so schedule it on the page's event loop.
        e.control.page.run_task(e.control.page.show_drawer)

    return ft.View(
        route=ROUTES[selected_index],
        appbar=ft.AppBar(
            title=ft.Text(title),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            leading=ft.IconButton(
                ft.Icons.MENU,
                tooltip="Open navigation drawer",
                on_click=open_drawer,
            ),
            # Without this Flet would also insert an automatic back button.
            automatically_imply_leading=False,
        ),
        drawer=_drawer(selected_index, on_drawer_change),
        controls=list(controls),
    )


def main(page: ft.Page):
    page.title = "Drawer navigation example"

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                _view(
                    "Home",
                    0,
                    ft.Text("Welcome to the home page"),
                    ft.Button(
                        "Go to store",
                        icon=ft.Icons.ARROW_FORWARD,
                        on_click=lambda: page.navigate("/store"),
                    ),
                )
            )
        elif page.route == "/store":
            page.views.append(
                _view(
                    "Store",
                    1,
                    ft.Text("Welcome to the store page"),
                    ft.Button(
                        "Go to about",
                        icon=ft.Icons.ARROW_FORWARD,
                        on_click=lambda: page.navigate("/about"),
                    ),
                )
            )
        elif page.route == "/about":
            page.views.append(
                _view(
                    "About",
                    2,
                    ft.Text("Welcome to the about page"),
                    ft.Button(
                        "Go home",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda: page.navigate("/"),
                    ),
                )
            )
        else:
            page.navigate("/")
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
