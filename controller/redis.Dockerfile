# Start with the official Redis image
FROM redis:latest

# Install OpenTelemetry dependencies
RUN apt-get update && apt-get install -y \
    curl wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install the OpenTelemetry auto-instrumentation agent
ENV OTEL_VERSION=0.114.0
RUN wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v${OTEL_VERSION}/otelcol_${OTEL_VERSION}_linux_amd64.tar.gz \
    && tar -xzf otelcol_${OTEL_VERSION}_linux_amd64.tar.gz \
    && mv otelcol /usr/local/bin/otelcol \
    && rm -f otelcol_${OTEL_VERSION}_linux_amd64.tar.gz

# Expose Redis port
EXPOSE 6379

# Set up environment variables for OpenTelemetry
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4317
ENV OTEL_SERVICE_NAME=redis-service

# Start Redis with the OpenTelemetry agent
CMD ["sh", "-c", "/usr/local/bin/otelcol & redis-server"]