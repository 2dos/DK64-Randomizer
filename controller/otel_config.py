from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Define a resource to identify your service
resource = Resource(attributes={
    "service.name": "controller",
    "service.version": "1.0.0"
})

# Set up the TracerProvider and Span Exporter
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()

# Configure OTLP Exporter for sending traces to the collector
otlp_exporter = OTLPSpanExporter(endpoint="http://host.docker.internal:4317")

# Add the BatchSpanProcessor to the TracerProvider
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)
