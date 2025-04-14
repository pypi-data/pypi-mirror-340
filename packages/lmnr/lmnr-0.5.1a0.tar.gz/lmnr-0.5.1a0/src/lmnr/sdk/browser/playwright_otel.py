import logging
import uuid

from lmnr.sdk.browser.pw_utils import handle_navigation_async, handle_navigation_sync
from lmnr.sdk.browser.utils import with_tracer_wrapper
from lmnr.version import __version__

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import (
    get_tracer,
    Tracer,
    get_current_span,
    Span,
    INVALID_SPAN,
    set_span_in_context,
)
from opentelemetry.context import get_current
from typing import Collection, Optional
from wrapt import wrap_function_wrapper

try:
    from playwright.async_api import Browser
    from playwright.sync_api import (
        Browser as SyncBrowser,
        BrowserContext as SyncBrowserContext,
    )
except ImportError as e:
    raise ImportError(
        f"Attempted to import {__file__}, but it is designed "
        "to patch Playwright, which is not installed. Use `pip install playwright` "
        "to install Playwright or remove this import."
    ) from e

# all available versions at https://pypi.org/project/playwright/#history
_instruments = ("playwright >= 1.9.0",)
logger = logging.getLogger(__name__)

_context_spans: dict[str, Span] = {}
_project_api_key: Optional[str] = None
_base_http_url: Optional[str] = None


@with_tracer_wrapper
def _wrap_new_page(tracer: Tracer, to_wrap, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
        f"{to_wrap.get('object')}.{to_wrap.get('method')}"
    ) as span:
        page = wrapped(*args, **kwargs)
        session_id = str(uuid.uuid4().hex)
        trace_id = format(get_current_span().get_span_context().trace_id, "032x")
        span.set_attribute("lmnr.internal.has_browser_session", True)
        handle_navigation_sync(
            page, session_id, trace_id, _project_api_key, _base_http_url
        )
        return page


@with_tracer_wrapper
async def _wrap_new_page_async(
    tracer: Tracer, to_wrap, wrapped, instance, args, kwargs
):
    with tracer.start_as_current_span(
        f"{to_wrap.get('object')}.{to_wrap.get('method')}"
    ) as span:
        page = await wrapped(*args, **kwargs)
        session_id = str(uuid.uuid4().hex)
        trace_id = format(span.get_span_context().trace_id, "032x")
        span.set_attribute("lmnr.internal.has_browser_session", True)
        await handle_navigation_async(
            page, session_id, trace_id, _project_api_key, _base_http_url
        )
        return page


@with_tracer_wrapper
def _wrap_new_browser_sync(tracer: Tracer, to_wrap, wrapped, instance, args, kwargs):
    global _context_spans
    browser: SyncBrowser = wrapped(*args, **kwargs)
    session_id = str(uuid.uuid4().hex)
    for context in browser.contexts:
        span = get_current_span()
        if span == INVALID_SPAN:
            span = tracer.start_span(
                name=f"{to_wrap.get('object')}.{to_wrap.get('method')}"
            )
            set_span_in_context(span, get_current())
            _context_spans[id(context)] = span
        span.set_attribute("lmnr.internal.has_browser_session", True)
        trace_id = format(span.get_span_context().trace_id, "032x")
        context.on(
            "page",
            lambda page: handle_navigation_sync(
                page, session_id, trace_id, _project_api_key, _base_http_url
            ),
        )
        for page in context.pages:
            handle_navigation_sync(
                page, session_id, trace_id, _project_api_key, _base_http_url
            )
    return browser


@with_tracer_wrapper
async def _wrap_new_browser_async(
    tracer: Tracer, to_wrap, wrapped, instance, args, kwargs
):
    global _context_spans
    browser: Browser = await wrapped(*args, **kwargs)
    session_id = str(uuid.uuid4().hex)
    for context in browser.contexts:
        span = get_current_span()
        if span == INVALID_SPAN:
            span = tracer.start_span(
                name=f"{to_wrap.get('object')}.{to_wrap.get('method')}"
            )
            set_span_in_context(span, get_current())
            _context_spans[id(context)] = span
        span.set_attribute("lmnr.internal.has_browser_session", True)
        trace_id = format(span.get_span_context().trace_id, "032x")

        async def handle_page_navigation(page):
            return await handle_navigation_async(
                page, session_id, trace_id, _project_api_key, _base_http_url
            )

        context.on("page", handle_page_navigation)
        for page in context.pages:
            await handle_navigation_async(
                page, session_id, trace_id, _project_api_key, _base_http_url
            )
    return browser


@with_tracer_wrapper
def _wrap_new_context_sync(tracer: Tracer, to_wrap, wrapped, instance, args, kwargs):
    context: SyncBrowserContext = wrapped(*args, **kwargs)
    session_id = str(uuid.uuid4().hex)
    span = get_current_span()
    if span == INVALID_SPAN:
        span = tracer.start_span(
            name=f"{to_wrap.get('object')}.{to_wrap.get('method')}"
        )
        set_span_in_context(span, get_current())
        _context_spans[id(context)] = span
    span.set_attribute("lmnr.internal.has_browser_session", True)
    trace_id = format(span.get_span_context().trace_id, "032x")

    context.on(
        "page",
        lambda page: handle_navigation_sync(
            page, session_id, trace_id, _project_api_key, _base_http_url
        ),
    )
    for page in context.pages:
        handle_navigation_sync(
            page, session_id, trace_id, _project_api_key, _base_http_url
        )
    return context


@with_tracer_wrapper
async def _wrap_new_context_async(
    tracer: Tracer, to_wrap, wrapped, instance, args, kwargs
):
    context: SyncBrowserContext = await wrapped(*args, **kwargs)
    session_id = str(uuid.uuid4().hex)
    span = get_current_span()
    if span == INVALID_SPAN:
        span = tracer.start_span(
            name=f"{to_wrap.get('object')}.{to_wrap.get('method')}"
        )
        set_span_in_context(span, get_current())
        _context_spans[id(context)] = span
    span.set_attribute("lmnr.internal.has_browser_session", True)
    trace_id = format(span.get_span_context().trace_id, "032x")

    async def handle_page_navigation(page):
        return await handle_navigation_async(
            page, session_id, trace_id, _project_api_key, _base_http_url
        )

    context.on("page", handle_page_navigation)
    for page in context.pages:
        await handle_navigation_async(
            page, session_id, trace_id, _project_api_key, _base_http_url
        )
    return context


@with_tracer_wrapper
def _wrap_close_browser_sync(
    tracer: Tracer,
    to_wrap,
    wrapped,
    instance: SyncBrowser,
    args,
    kwargs,
):
    global _context_spans
    for context in instance.contexts:
        key = id(context)
        span = _context_spans.get(key)
        if span:
            if span.is_recording():
                span.end()
            _context_spans.pop(key)
    return wrapped(*args, **kwargs)


@with_tracer_wrapper
async def _wrap_close_browser_async(
    tracer: Tracer,
    to_wrap,
    wrapped,
    instance: Browser,
    args,
    kwargs,
):
    global _context_spans
    for context in instance.contexts:
        key = id(context)
        span = _context_spans.get(key)
        if span:
            if span.is_recording():
                span.end()
            _context_spans.pop(key)
    return await wrapped(*args, **kwargs)


WRAPPED_METHODS = [
    {
        "package": "playwright.sync_api",
        "object": "BrowserContext",
        "method": "new_page",
        "wrapper": _wrap_new_page,
    },
    {
        "package": "playwright.sync_api",
        "object": "Browser",
        "method": "new_page",
        "wrapper": _wrap_new_page,
    },
    {
        "package": "playwright.sync_api",
        "object": "BrowserType",
        "method": "launch",
        "wrapper": _wrap_new_browser_sync,
    },
    {
        "package": "playwright.sync_api",
        "object": "BrowserType",
        "method": "connect",
        "wrapper": _wrap_new_browser_sync,
    },
    {
        "package": "playwright.sync_api",
        "object": "BrowserType",
        "method": "connect_over_cdp",
        "wrapper": _wrap_new_browser_sync,
    },
    {
        "package": "playwright.sync_api",
        "object": "Browser",
        "method": "close",
        "wrapper": _wrap_close_browser_sync,
    },
    {
        "package": "playwright.sync_api",
        "object": "Browser",
        "method": "new_context",
        "wrapper": _wrap_new_context_sync,
    },
    {
        "package": "playwright.sync_api",
        "object": "BrowserType",
        "method": "launch_persistent_context",
        "wrapper": _wrap_new_context_sync,
    },
]

WRAPPED_METHODS_ASYNC = [
    {
        "package": "playwright.async_api",
        "object": "BrowserContext",
        "method": "new_page",
        "wrapper": _wrap_new_page_async,
    },
    {
        "package": "playwright.async_api",
        "object": "Browser",
        "method": "new_page",
        "wrapper": _wrap_new_page_async,
    },
    {
        "package": "playwright.async_api",
        "object": "BrowserType",
        "method": "launch",
        "wrapper": _wrap_new_browser_async,
    },
    {
        "package": "playwright.async_api",
        "object": "BrowserType",
        "method": "connect",
        "wrapper": _wrap_new_browser_async,
    },
    {
        "package": "playwright.async_api",
        "object": "BrowserType",
        "method": "connect_over_cdp",
        "wrapper": _wrap_new_browser_async,
    },
    {
        "package": "playwright.async_api",
        "object": "Browser",
        "method": "close",
        "wrapper": _wrap_close_browser_async,
    },
    {
        "package": "playwright.async_api",
        "object": "Browser",
        "method": "new_context",
        "wrapper": _wrap_new_context_async,
    },
    {
        "package": "playwright.sync_api",
        "object": "BrowserType",
        "method": "launch_persistent_context",
        "wrapper": _wrap_new_context_sync,
    },
]


class PlaywrightInstrumentor(BaseInstrumentor):
    def __init__(self):
        super().__init__()

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        global _project_api_key, _base_http_url

        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, __version__, tracer_provider)

        if kwargs.get("project_api_key"):
            _project_api_key = kwargs.get("project_api_key")

        if kwargs.get("base_http_url"):
            _base_http_url = kwargs.get("base_http_url")

        for wrapped_method in WRAPPED_METHODS:
            wrap_package = wrapped_method.get("package")
            wrap_object = wrapped_method.get("object")
            wrap_method = wrapped_method.get("method")
            try:
                wrap_function_wrapper(
                    wrap_package,
                    f"{wrap_object}.{wrap_method}",
                    wrapped_method.get("wrapper")(
                        tracer,
                        wrapped_method,
                    ),
                )
            except ModuleNotFoundError:
                pass  # that's ok, we don't want to fail if some module is missing

        # Wrap async methods
        for wrapped_method in WRAPPED_METHODS_ASYNC:
            wrap_package = wrapped_method.get("package")
            wrap_object = wrapped_method.get("object")
            wrap_method = wrapped_method.get("method")
            try:
                wrap_function_wrapper(
                    wrap_package,
                    f"{wrap_object}.{wrap_method}",
                    wrapped_method.get("wrapper")(
                        tracer,
                        wrapped_method,
                    ),
                )
            except ModuleNotFoundError:
                pass  # that's ok, we don't want to fail if some module is missing

    def _uninstrument(self, **kwargs):
        # Unwrap methods
        global _context_spans
        for wrapped_method in WRAPPED_METHODS + WRAPPED_METHODS_ASYNC:
            wrap_package = wrapped_method.get("package")
            wrap_object = wrapped_method.get("object")
            wrap_method = wrapped_method.get("method")
            unwrap(wrap_package, f"{wrap_object}.{wrap_method}")
            for span in _context_spans.values():
                if span.is_recording():
                    span.end()
            _context_spans = {}
