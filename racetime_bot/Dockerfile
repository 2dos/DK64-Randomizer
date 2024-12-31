FROM python:3.12-slim
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
COPY ./ /app/
# Conditionally clone the repository if BRANCH is not LOCAL
RUN if [ "$BRANCH" != "LOCAL" ]; then \
        apt-get update -y && apt-get install -y git && \
        rm -rf /app/ && \
        git config --global core.compression 0 && \
        git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app; \
    fi

WORKDIR /app/racetime_bot
RUN pip install .
WORKDIR /app/racetime_bot/randobot
# Command to run the application
CMD ["python", "__init__.py", "--category_slug", "$CATEGORY_SLUG", "--client_id", "$RGG_CLIENT_ID", "--client_secret", "$RGG_CLIENT_SECRET"]