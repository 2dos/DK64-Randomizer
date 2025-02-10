FROM python:3.12-alpine
# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
ARG CATEGORY_SLUG
ARG RGG_CLIENT_ID
ARG RGG_CLIENT_SECRET
ARG DISCORD_WEBHOOK
ARG API_KEY
ENV DISCORD_WEBHOOK=$DISCORD_WEBHOOK
ENV DK64_API_KEY=$API_KEY
ENV CATEGORY_SLUG=$CATEGORY_SLUG
ENV RGG_CLIENT_ID=$RGG_CLIENT_ID
ENV RGG_CLIENT_SECRET=$RGG_CLIENT_SECRET

# COPY ./racetime_bot /app/
RUN apk update && apk add git && \
    git config --global core.compression 0 && \
    git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app

WORKDIR /app/racetime_bot
RUN pip install .
WORKDIR /app/racetime_bot/randobot
# Command to run the application
CMD ["sh", "-c", "sleep 15 && python __init__.py"]