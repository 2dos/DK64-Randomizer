FROM nginx:alpine-otel
ARG NGINX=LOCAL
ENV NGINX=$NGINX
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx-local.conf /etc/nginx/nginx-local.conf
RUN if [ "$NGINX" = "LOCAL" ]; then \
        cp /etc/nginx/nginx-local.conf /etc/nginx/nginx.conf; \
    fi
