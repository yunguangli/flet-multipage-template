"""
example2.py - Intercepting back navigation with `View.on_confirm_pop`.

A view with `can_pop=False` is asked for permission before it is popped: Flet
fires the view's `on_confirm_pop` handler, and the view answers with
`confirm_pop(True/False)`. If no answer arrives before the frontend timeout,
the pop is cancelled.

Run:  python example2.py
"""

import flet as ft


class HomeView(ft.View):
    def __init__(self):
        super().__init__(
            route="/",
            can_pop=False,
            on_confirm_pop=self.ask_to_leave,
            appbar=ft.AppBar(title=ft.Text("Home")),
            controls=[
                ft.Text("Home page"),
                ft.Button(
                    "Go to store",
                    icon=ft.Icons.STORE,
                    on_click=lambda: self.page.navigate("/store"),
                ),
            ],
        )

    async def ask_to_leave(self, e: ft.ControlEvent):
        async def on_yes(e: ft.ControlEvent):
            self.page.pop_dialog()
            await self.confirm_pop(True)

        async def on_no(e: ft.ControlEvent):
            self.page.pop_dialog()
            await self.confirm_pop(False)

        self.page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Please confirm"),
                content=ft.Text("Leave this page?"),
                actions=[
                    ft.Button("Yes", on_click=on_yes),
                    ft.TextButton("No", on_click=on_no),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )


class StoreView(ft.View):
    def __init__(self):
        super().__init__(
            route="/store",
            appbar=ft.AppBar(title=ft.Text("Store")),
            controls=[
                ft.Text("Store page"),
                ft.Button(
                    "Go home",
                    icon=ft.Icons.HOME,
                    on_click=lambda: self.page.navigate("/"),
                ),
            ],
        )


def main(page: ft.Page):
    page.title = "Confirm pop example"

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.views.append(HomeView())
        if page.route == "/store":
            page.views.append(StoreView())
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
