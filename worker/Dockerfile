FROM python:3.12-alpine

# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
ARG COPY_FILES="./"

RUN apk update && apk add --no-cache xdelta3 git

# Copy local files
COPY $COPY_FILES /app/

# Conditionally clone the repository if BRANCH is not LOCAL
RUN if [ "$BRANCH" != "LOCAL" ]; then \
        rm -rf /app/ && \
        git config --global core.compression 0 && \
        git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app; \
    fi
WORKDIR /app/worker

# Install dependencies
RUN pip install -r requirements.txt && \
    mv /app/static /app/worker/static && \
    mv /app/randomizer /app/worker/randomizer && \
    mv /app/version.py /app/worker/version.py && \
    mv /app/js.py /app/worker/js.py && \
    mv /app/base-hack /app/worker/base-hack/

# Command to run the application
CMD ["opentelemetry-instrument", "python", "worker.py"]
