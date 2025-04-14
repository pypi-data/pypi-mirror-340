import sys

from contextlib import contextmanager
from typing import Optional, Set
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.propagators.textmap import TextMapPropagator
from opentelemetry.util.re import parse_env_headers

from lmnr.openllmetry_sdk.instruments import Instruments
from lmnr.openllmetry_sdk.config import (
    is_content_tracing_enabled,
    is_tracing_enabled,
)
from lmnr.openllmetry_sdk.tracing.tracing import TracerWrapper
from typing import Dict


class TracerManager:
    __tracer_wrapper: TracerWrapper
    __initialized: bool = False

    @staticmethod
    def init(
        app_name: Optional[str] = sys.argv[0],
        api_endpoint: str = "https://api.lmnr.ai",
        api_key: Optional[str] = None,
        headers: Dict[str, str] = {},
        disable_batch=False,
        exporter: Optional[SpanExporter] = None,
        processor: Optional[SpanProcessor] = None,
        propagator: Optional[TextMapPropagator] = None,
        should_enrich_metrics: bool = False,
        resource_attributes: dict = {},
        instruments: Optional[Set[Instruments]] = None,
        base_http_url: Optional[str] = None,
        project_api_key: Optional[str] = None,
        max_export_batch_size: Optional[int] = None,
    ) -> None:
        if not is_tracing_enabled():
            return

        enable_content_tracing = is_content_tracing_enabled()

        if isinstance(headers, str):
            headers = parse_env_headers(headers)

        if api_key and not exporter and not processor and not headers:
            headers = {
                "Authorization": f"Bearer {api_key}",
            }

        # Tracer init
        resource_attributes.update({SERVICE_NAME: app_name})
        TracerManager.__tracer_wrapper = TracerWrapper(
            disable_batch=disable_batch,
            processor=processor,
            propagator=propagator,
            exporter=exporter,
            should_enrich_metrics=should_enrich_metrics,
            instruments=instruments,
            base_http_url=base_http_url,
            project_api_key=project_api_key,
            max_export_batch_size=max_export_batch_size,
            resource_attributes=resource_attributes,
            enable_content_tracing=enable_content_tracing,
            endpoint=api_endpoint,
            headers=headers,
        )
        TracerManager.__initialized = True

    @staticmethod
    def flush() -> bool:
        return TracerManager.__tracer_wrapper.flush()

    @staticmethod
    def shutdown() -> bool:
        try:
            res = TracerManager.__tracer_wrapper.shutdown()
            TracerManager.__tracer_wrapper = None
            TracerManager.__initialized = False
            return res
        except Exception:
            return False

    @staticmethod
    def is_initialized() -> bool:
        return TracerManager.__initialized

    @staticmethod
    def get_tracer_wrapper() -> TracerWrapper:
        return TracerManager.__tracer_wrapper


@contextmanager
def get_tracer(flush_on_exit: bool = False):
    wrapper = TracerManager.get_tracer_wrapper()
    try:
        yield wrapper.get_tracer()
    finally:
        if flush_on_exit:
            wrapper.flush()
