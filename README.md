# Flet Multi-Page Routing Template

A starting point for multi-page apps built with **Flet 1.0**'s declarative
component API: `ft.Router`, `ft.Route`, `@ft.component` and dataclass-based
observable state.

## What it demonstrates

| Idea | Flet 1.0 API |
| --- | --- |
| Routing | [`ft.Router`](https://flet.dev/docs/controls/router) + `ft.Route` |
| Back navigation | `manage_views=True` + [`ft.View`](https://flet.dev/docs/controls/view) stack |
| Shared state | `@ft.observable @dataclass` + `ft.create_context` / `ft.use_context` |
| Page-scoped state | `ft.use_state` seeded from `page.session.store` |
| Dialogs | `ft.use_dialog()` (declarative) and `page.show_dialog()` (one-shot snack bars) |
| 404 handling | `ft.Router(not_found=...)` |

## Project layout

```
src/
├── main.py               # Entry point: page setup + the route table
├── app_state.py          # Observable dataclasses, session-store accessors, hooks
├── ui.py                 # Small shared presentation helpers
├── assets/               # Icons and splash screens
└── pages/
    ├── __init__.py
    ├── home.py           # "/"       — landing page
    ├── page_one.py       # "/page-1" — page-scoped state
    ├── page_two.py       # "/page-2" — shared-state dashboard
    ├── page_three.py     # "/page-3" — session summary + reset
    └── not_found.py      # anything else
```

## Getting started

```bash
# with uv
uv sync
uv run flet run src/main.py

# or plain pip
pip install "flet[all]==1.0.3"
cd src && python main.py
```

`python main.py --web` serves it in a browser instead of a desktop window.

## How it works

### 1. One route table, no manual view juggling

`main()` configures the `Page` and hands everything else to a component:

```python
def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.window.width = 1000
    page.render_views(App)          # <- the component tree replaces page.views
```

`App` is a component that owns the session state and returns a `Router`:

```python
@ft.component
def App() -> ft.View:
    state, _ = ft.use_state(get_app_state)

    return AppStateContext(
        state,
        lambda: ft.Router(
            routes=[
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
            manage_views=True,
        ),
    )
```

There is no `on_route_change` / `on_view_pop` handler to write: the Router
subscribes to route changes and re-renders itself.

### 2. The pathless root route

The outer `ft.Route` has no `path`, so it adds no URL segment, but it is always
the first entry in the view stack. Every other page therefore has something to
pop back to. It maps `/` to `home.Home` because `Home` is its only child that
matches with nothing left over.

### 3. `manage_views=True` gives you back navigation for free

The Router returns **one `View` per route level**, so navigating
`/` → `/page-2` produces the stack `[Home, PageTwo]`. Flet then enables:

- the implicit `AppBar` back arrow (only the root opts out, with `can_pop=False`),
- swipe-back on iOS,
- the Android system back button,
- browser Back/Forward.

`page.pop_views_until()` and manual `page.views.remove(...)` calls are *not*
needed - and `pop_views_until()` does not work in component mode.

### 4. Observable dataclasses instead of a singleton in a dict

```python
@ft.observable
@dataclass
class AppState:
    config: AppConfig = field(default_factory=AppConfig)
    counter: int = 0
    data_store: dict[str, str] = field(default_factory=dict)
    navigation_history: list[str] = field(default_factory=lambda: ["/"])
```

`ft.observable` intercepts attribute writes and re-renders exactly the
components that read the model. `list` and `dict` fields are wrapped
automatically, so in-place mutations notify too. No `page.update()` calls, no
manual invalidation.

`AppState` replaces the old "singleton class stashed in `page.session`" pattern
with the same shared-instance semantics, but typed fields and automatic
reactivity. Hang your own services off it (DB pool, HTTP client, current user).

### 5. Context for app-wide state, session storage for page-scoped state

Two different lifetimes, two different mechanisms:

```python
# app-wide: one instance per session, handed down through context
state = use_app_state()                      # use_context(), auto-subscribes

# page-scoped: one instance per session, seeded into component state
draft = use_page_one_draft()                 # ft.use_state(get_page_one_draft)
```

Both models are cached in `page.session.store`, so code *outside* the component
tree - a background task, a service, a page-level event handler - can reach the
same objects via `get_app_state()` / `get_page_one_draft()`.

`reset_session()` clears the store and resets the models **in place**, so pages
that already hold a reference show the cleared values immediately.

### 6. Dialogs follow state

Real dialogs use the declarative hook; `show_info` is the single source of truth
and rendering `None` hides the dialog:

```python
show_info, set_show_info = ft.use_state(False)

ft.use_dialog(
    _session_info_dialog(state, lambda: set_show_info(False)) if show_info else None
)
```

Transient snack bars are one-shot notifications, so `ui.toast()` uses the
imperative `page.show_dialog()` instead.

### 7. Side effects go in effects

```python
@ft.component
def PageOne() -> ft.View:
    draft = use_page_one_draft()
    use_visit("/page-1")                       # history, once per mount
    ft.use_effect(lambda: _count_visit(draft), [])   # visit counter, once per mount
```

Both are wrapped in `ft.use_effect` so they run after the first render rather
than on every re-render (a re-render happens on every keystroke in the text
field).

## Adding a page

1. Create `src/pages/page_four.py` with an `@ft.component` that returns a `View`:

   ```python
   @ft.component
   def PageFour() -> ft.View:
       return view(
           "/page-4", "Page 4", ACCENT,
           *heading("Page 4", "Something new.", ACCENT),
           can_pop=True,
       )
   ```

2. Register it in `main.py`:

   ```python
   ft.Route(path="page-4", component=page_four.PageFour),
   ```

3. Add a navigation button on the page you want to reach it from:

   ```python
   accent_button("Page 4", ft.Icons.ARROW_FORWARD, ACCENT,
                 lambda: ft.context.page.navigate("/page-4"))
   ```

For dynamic segments use `path="items/:item_id"` and read
`ft.use_route_params()["item_id"]` in the component.

## Reference examples

The files at the repo root show the **imperative** alternative that Flet 1.0
still supports - `page.views` manipulated by hand in `on_route_change`. Useful
when porting an existing app, but the Router in `src/` is the recommended path.

| File | Shows |
| --- | --- |
| `example1.py` | Manual `page.views` stack and `on_route_change` |
| `example2.py` | `View.can_pop=False` + `on_confirm_pop` / `confirm_pop()` |
| `example3.py` | Two-level nested routes (`/settings` → `/settings/mail`) |
| `example4.py` | `NavigationDrawer` per view, synced to the current route |

## Migrating from pre-1.0

The API renames that bite first:

| Pre-1.0 | Flet 1.0 |
| --- | --- |
| `page.go("/x")` | `page.navigate("/x")` (sync) or `await page.push_route("/x")` |
| `page.pop_route()` | handled by the Router's view stack |
| `ft.ElevatedButton` | `ft.Button` / `ft.FilledButton` / `ft.OutlinedButton` |
| `ft.padding.all(30)` | `ft.Padding.all(30)` |
| `ft.padding.symmetric(...)` | `ft.Padding.symmetric(...)` |
| `page.window_width` | `page.window.width` |
| `page.snack_bar = ...; page.update()` | `page.show_dialog(ft.SnackBar(...))` |
| `page.open(dlg)` / `page.close(dlg)` | `page.show_dialog(dlg)` / `page.pop_dialog()` |
| `TextField(border_color=...)` | `TextField(border=ft.OutlineInputBorder(...))` |
| `page.on_route_change` + manual views | `page.render_views(App)` + `ft.Router` |
| `ft.session.get(k)` | `page.session.store.get(k)` |

Also note: `ft.Router`'s `not_found` component is called directly rather than
mounted as a route component, so route hooks such as `ft.use_route_location()`
are not available there - use `ft.context.page.route`.

## License

MIT