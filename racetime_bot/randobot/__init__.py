"""Loader function for the RandoBot package."""

import argparse
import logging
import sys

from bot import RandoBot
import logging
import os
import socket
from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import metrics

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging.basicConfig(level=logging.INFO)

# Define a resource to identify your service
resource = Resource(
    attributes={
        "service.name": "racetime_bot",
        "service.version": "1.0",
        "deployment.environment": os.environ.get("BRANCH", "LOCAL"),
        "container.id": next((l.rsplit("/", 1)[-1] for l in open("/proc/self/cgroup") if "docker" in l), "") if os.path.exists("/proc/self/cgroup") else "",
        "container.name": socket.gethostname(),
    }
)
logger = logging.getLogger(__name__)

# check the args we started the script with
if __name__ == "__main__" or os.environ.get("BRANCH", "LOCAL") != "LOCAL":
    # create the providers
    logger_provider = LoggerProvider(resource=resource)
    # set the providers
    set_logger_provider(logger_provider)
    # Set up the TracerProvider and Span Exporter
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer_provider = trace.get_tracer_provider()

    # # Configure OTLP Exporter for sending traces to the collector
    otlp_exporter = OTLPSpanExporter(endpoint="http://host.docker.internal:4318/v1/traces")
    # # Add the BatchSpanProcessor to the TracerProvider
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://host.docker.internal:4318/v1/metrics"))
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meterProvider)
    RequestsInstrumentor().instrument()
    handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    logger.addHandler(handler)


def main():
    """Initialize and run the bot."""
    parser = argparse.ArgumentParser(
        description="RandoBot, because Zootr seeds weren't scary enough already.",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose output")
    parser.add_argument("--host", type=str, nargs="?", help="change the ractime.gg host (debug only!")
    parser.add_argument("--insecure", action="store_true", help="don't use HTTPS (debug only!)")

    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stdout)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s (%(levelname)s) :: %(message)s"))
    logger.addHandler(handler)

    if args.host:
        RandoBot.racetime_host = args.host
    if args.insecure:
        RandoBot.racetime_secure = False

    inst = RandoBot(
        category_slug=os.environ.get("CATEGORY_SLUG"),
        client_id=os.environ.get("RGG_CLIENT_ID"),
        client_secret=os.environ.get("RGG_CLIENT_SECRET"),
        logger=logger,
    )
    inst.run()


if __name__ == "__main__":
    main()
