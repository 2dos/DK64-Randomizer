FROM python:3.12-alpine
# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
ARG DISCORD_APP_TOKEN
ENV DISCORD_APP_TOKEN=$DISCORD_APP_TOKEN
ARG API_KEY
ENV DK64_API_KEY=$API_KEY
# COPY ./discord_bot /app/discord_bot
RUN apk update && apk add git && \
    git config --global core.compression 0 && \
    git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app

WORKDIR /app/discord_bot
RUN pip install -r requirements.txt
# Command to run the application
CMD ["sh", "-c", "sleep 15 && python app.py"]