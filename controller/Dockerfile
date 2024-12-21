FROM python:3.12-slim
# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH
# Copy local files

COPY ./ /app/
WORKDIR /app/controller
# Conditionally clone the repository if BRANCH is not LOCAL
RUN if [ "$BRANCH" != "LOCAL" ]; then \
        apt-get update -y && apt-get install -y git && \
        rm -rf /app/ && \
        mkdir /app && \
        git config --global core.compression 0 && \
        git config --global user.email "clone@clone.com" && \
        git config --global user.name "Clone" && \
        git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app; \
    fi

RUN if [ "$BRANCH" = "LOCAL" ]; then \
        mv /app/static /app/controller/static && \
        mv /app/randomizer /app/controller/randomizer && \
        mv /app/js.py /app/controller/js.py && \
        mv /app/ui /app/controller/ui/ && \
        mv /app/templates /app/controller/templates/ && \
        mv /app/index.html /app/controller/index.html && \
        mv /app/randomizer.html /app/controller/randomizer.html && \
        mv /app/base-hack /app/controller/base-hack/; \
    fi

RUN pip install -r requirements.txt && \
    mv /app/version.py /app/controller/version.py

# Command to run the application
CMD ["waitress-serve", "--port=8000", "app:app"]
