#!/bin/sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4317 OTEL_EXPORTER_OTLP_PROTOCOL=grpc OTEL_RESOURCE_ATTRIBUTES=service.name=controller opentelemetry-instrument python app.py