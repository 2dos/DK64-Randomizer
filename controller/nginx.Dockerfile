FROM nginx:alpine-otel
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx-dev.conf /etc/nginx/nginx-dev.conf
RUN if [ "$BRANCH" = "LOCAL" ]; then \
        cp /etc/nginx/nginx-dev.conf /etc/nginx/nginx.conf; \
    fi
