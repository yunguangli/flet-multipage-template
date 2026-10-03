"""
app_state.py - The application's shared, observable state.

Two models live here, both plain dataclasses:

``AppState``
    App-wide state (counter, key/value store, navigation history). One instance
    per user session, handed to components through React context so that no page
    has to thread it through props.

``PageOneDraft``
    State that belongs to a *single* page but must survive navigation. The page
    seeds it from the session store with ``ft.use_state``, so leaving and
    re-entering the page keeps the user's text.

Why dataclasses + ``ft.observable``?

* typed fields with IDE completion and no stringly-typed dict keys,
* ``@ft.observable`` intercepts attribute writes and re-renders exactly the
  components that read the model - no ``page.update()`` calls to forget,
* ``list`` and ``dict`` fields are wrapped automatically, so in-place
  mutations (``state.data_store.clear()``) notify just like assignments.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import flet as ft

# Keys used in ``page.session.store``.
APP_STATE_KEY = "app_state"
PAGE_ONE_DRAFT_KEY = "page-1:draft"


@ft.observable
@dataclass
class AppConfig:
    """Application-wide settings. Read-only as far as the UI is concerned."""

    app_name: str = "Flet Multi-Page Template"
    version: str = "1.0.0"
    debug: bool = True


@ft.observable
@dataclass
class AppState:
    """The app's shared "singleton": one observable instance per user session.

    A real application would hang heavier things off this model - a database
    connection pool, an HTTP client, a cache, the current user - and every page
    would reach them the same way.
    """

    config: AppConfig = field(default_factory=AppConfig)

    # --- shared, reactive values -------------------------------------------
    counter: int = 0
    data_store: dict[str, str] = field(default_factory=dict)
    navigation_history: list[str] = field(default_factory=lambda: ["/"])

    # --- model API ---------------------------------------------------------
    def increment_counter(self) -> int:
        """Bump the shared counter and return the new value."""
        self.counter += 1
        return self.counter

    def store_data(self, key: str, value: str) -> None:
        """Put a value in the app-wide key/value store."""
        self.data_store[key] = value

    def get_data(self, key: str) -> str | None:
        """Read a value from the app-wide key/value store."""
        return self.data_store.get(key)

    def record_visit(self, route: str) -> None:
        """Append ``route`` to the navigation history, once per route."""
        if route not in self.navigation_history:
            self.navigation_history.append(route)

    def reset(self) -> None:
        """Restore every field to its default (configuration is kept)."""
        self.counter = 0
        self.data_store.clear()
        self.navigation_history.clear()
        self.navigation_history.append("/")

    def snapshot(self) -> dict:
        """A plain dict of everything in the model - handy for debugging."""
        return {
            "config": {
                "app_name": self.config.app_name,
                "version": self.config.version,
                "debug": self.config.debug,
            },
            "counter": self.counter,
            "data_store": dict(self.data_store),
            "navigation_history": list(self.navigation_history),
        }


@ft.observable
@dataclass
class PageOneDraft:
    """Page-scoped state that has to outlive the page's own component."""

    visits: int = 0
    text: str = ""
    saved_at: str | None = None

    def reset(self) -> None:
        """Forget the draft and the visit count."""
        self.visits = 0
        self.text = ""
        self.saved_at = None


# ---------------------------------------------------------------------------
# Session-store accessors
#
# ``page.session.store`` is a per-user, server-side key/value store. Keeping the
# models there means non-component code (a background task, a service, an event
# handler outside the component tree) can reach the same objects the UI renders.
# ---------------------------------------------------------------------------


def get_app_state() -> AppState:
    """Return this session's :class:`AppState`, creating it on first access."""
    store = ft.context.page.session.store
    state = store.get(APP_STATE_KEY)
    if not isinstance(state, AppState):
        state = AppState()
        store.set(APP_STATE_KEY, state)
    return state


def get_page_one_draft() -> PageOneDraft:
    """Return this session's page-one draft, creating it on first access."""
    store = ft.context.page.session.store
    draft = store.get(PAGE_ONE_DRAFT_KEY)
    if not isinstance(draft, PageOneDraft):
        draft = PageOneDraft()
        store.set(PAGE_ONE_DRAFT_KEY, draft)
    return draft


def reset_session() -> None:
    """Wipe everything stored for this session.

    The two models are reset *in place* instead of being replaced: components
    that already hold a reference - the root ``App`` state, the current page's
    draft - keep rendering the very same objects, so the cleared values show up
    immediately without any re-mounting.
    """
    store = ft.context.page.session.store
    app_state, draft = get_app_state(), get_page_one_draft()

    store.clear()
    app_state.reset()
    draft.reset()
    store.set(APP_STATE_KEY, app_state)
    store.set(PAGE_ONE_DRAFT_KEY, draft)


# ---------------------------------------------------------------------------
# Component hooks
# ---------------------------------------------------------------------------


# `None` default: reading the context outside of <AppStateContext> is a bug, so
# the hook raises instead of silently handing back a throwaway model.
AppStateContext: ft.ContextProvider[AppState | None] = ft.create_context(None)


def use_app_state() -> AppState:
    """Read the shared :class:`AppState` from context.

    Because the value is observable, the calling component is subscribed to it:
    any later mutation re-renders it. No ``page.update()`` required.
    """
    state = ft.use_context(AppStateContext)
    if state is None:
        raise RuntimeError(
            "use_app_state() must be called inside an <AppStateContext> provider"
        )
    return state


def use_page_one_draft() -> PageOneDraft:
    """Seed page-scoped state from the session store and keep it reactive.

    ``ft.use_state`` calls the getter once per mount. Because the returned model
    is observable, the component re-renders whenever it changes - and because
    the model itself lives in the session store, the data is still there the
    next time the page is opened.
    """
    draft, _ = ft.use_state(get_page_one_draft)
    return draft


def use_visit(route: str) -> None:
    """Append ``route`` to the shared history when the page is shown.

    Wrapped in ``ft.use_effect`` so the record happens *after* render, once per
    mount, rather than on every re-render.
    """
    state = use_app_state()
    ft.use_effect(lambda: state.record_visit(route), [route])
