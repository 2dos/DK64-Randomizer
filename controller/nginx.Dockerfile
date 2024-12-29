FROM nginx:alpine-otel
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx-local.conf /etc/nginx/nginx-local.conf
RUN if [ "$BRANCH" = "LOCAL" ]; then \
        cp /etc/nginx/nginx-local.conf /etc/nginx/nginx.conf; \
    fi
