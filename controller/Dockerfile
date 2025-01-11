FROM python:3.12-alpine
# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
# Copy local files
ARG CLIENT_ID=" "
ENV CLIENT_ID=$CLIENT_ID
ARG CLIENT_SECRET=" "
ENV CLIENT_SECRET=$CLIENT_SECRET
ARG REDIRECT=" "
ENV REDIRECT=$REDIRECT
ARG COPY_FILES="./"
COPY ${COPY_FILES} /app/
# set the timezone to UTC
ENV TZ=UTC
RUN apk update && apk add --no-cache tzdata git
# Conditionally clone the repository if BRANCH is not LOCAL
RUN if [ "$BRANCH" != "LOCAL" ]; then \
        rm -rf /app/ && \
        git config --global core.compression 0 && \
        git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app; \
    fi


RUN mv /app/static /app/controller/static && \
    mv /app/randomizer /app/controller/randomizer && \
    mv /app/js.py /app/controller/js.py && \
    mv /app/ui /app/controller/ui && \
    mv /app/templates /app/controller/templates && \
    mv /app/index.html /app/controller/index.html && \
    mv /app/randomizer.html /app/controller/randomizer.html && \
    mv /app/base-hack /app/controller/base-hack

WORKDIR /app/controller
RUN pip install -r requirements.txt && \
    mv /app/version.py /app/controller/version.py

# Command to run the application
CMD ["waitress-serve", "--port=8000", "app:app"]
