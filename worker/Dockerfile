FROM python:3.12-slim

# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH

# Install required dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    make \
    git \
    build-essential \
    wget \
    autoconf

# Install xdelta
RUN wget https://github.com/jmacd/xdelta/archive/refs/tags/v3.1.0.tar.gz \
    && tar -xzf v3.1.0.tar.gz \
    && cd xdelta-3.1.0/xdelta3 \
    && autoreconf --install \
    && ./configure \
    && make \
    && make install \
    && cp xdelta3.c /usr/include/ \
    && cd .. \
    && rm -rf xdelta-3.1.0 v3.1.0.tar.gz \
    && pip install pyxdelta

# Copy local files
COPY ./ /app/

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

RUN opentelemetry-bootstrap --action=install

# Command to run the application
CMD ["opentelemetry-instrument", "python", "worker.py"]
