FROM nginx:latest
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx-dev.conf /etc/nginx/nginx-dev.conf
RUN apt-get update && apt-get install -y nginx-otel-module && \
    if [ "$BRANCH" = "LOCAL" ]; then \
        cp /etc/nginx/nginx-dev.conf /etc/nginx/nginx.conf; \
    fi
