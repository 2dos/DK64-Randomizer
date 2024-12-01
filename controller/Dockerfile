FROM python:3.12-slim
WORKDIR /app
COPY ./controller/ /app/
# Copy in the folder up ./randomizer
RUN mkdir /app/randomizer
COPY ./static /app/static
COPY ./randomizer /app/randomizer
COPY ./js.py /app/js.py
COPY ./version.py /app/version.py
RUN pip install -r requirements.txt && \
    pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation && \
    opentelemetry-bootstrap --action=install

# Set environment variables for OpenTelemetry
ENV OTEL_RESOURCE_ATTRIBUTES=service.name=controller
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
#CMD ["opentelemetry-instrument", "python", "app.py"]
CMD ["python", "app.py"]