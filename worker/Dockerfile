FROM python:3.12-alpine

# Define ARG and ENV variables
ARG BRANCH=LOCAL
ENV BRANCH=$BRANCH

RUN apk update && apk add --no-cache xdelta3 git gcc libc-dev wget tzdata \
    && wget https://github.com/jmacd/xdelta/archive/refs/tags/v3.1.0.tar.gz \
    && tar -xzf v3.1.0.tar.gz \
    && cd xdelta-3.1.0/xdelta3 \
    && cp xdelta3.h /usr/include \
    && cp xdelta3.c /usr/include

RUN pip install -r https://raw.githubusercontent.com/2dos/DK64-Randomizer/refs/heads/dev/worker/requirements.txt
# set the timezone to UTC
ENV TZ=UTC
# Copy local files
# COPY ./ /app/

# Conditionally clone the repository if BRANCH is not LOCAL
RUN git config --global core.compression 0 && \
    git clone --depth 1 --branch $BRANCH https://github.com/2dos/DK64-Randomizer.git /app
COPY randomizer/Encryption.py /app/randomizer/Encryption.py
WORKDIR /app/worker

# Install dependencies
RUN mv /app/static /app/worker/static && \
    mv /app/randomizer /app/worker/randomizer && \
    mv /app/version.py /app/worker/version.py && \
    mv /app/js.py /app/worker/js.py && \
    mv /app/base-hack /app/worker/base-hack/

# Command to run the application
CMD ["python", "worker.py"]
