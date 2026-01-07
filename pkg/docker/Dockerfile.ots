# build with context from root of source tree
# setup base image
FROM python:3.13-slim AS build
# docker build args
ARG BUILD_VERSION
ENV VERSION=${BUILD_VERSION}

# setup user
RUN addgroup --gid 1024 ots
RUN adduser --home /app --disabled-password --gecos "" --force-badname --gid 1024 ots

# install deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libpq-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*

USER ots

# install opentakserver from local source.
COPY ./server .
RUN pip install --user .

##########################################
FROM python:3.13-slim AS final
# setup user
RUN addgroup --gid 1024 ots
RUN adduser --home /app --disabled-password --gecos "" --force-badname --gid 1024 ots

# install deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg libpq5 curl \
 && rm -rf /var/lib/apt/lists/*

USER ots
WORKDIR /app/opentakserver
RUN chown -R ots:ots /app

# copy from build
COPY --from=build /app/.local /app/.local
ENV PATH=/app/.local/bin:$PATH

# setup CAs
RUN /app/.local/bin/flask --app /app/.local/lib/python3.13/site-packages/opentakserver/app.py ots create-ca

# entry point
EXPOSE 8081
ENTRYPOINT ["opentakserver"]

# Flask will stop gracefully on SIGINT (Ctrl-C).
# Docker compose tries to stop processes using SIGTERM by default, then sends SIGKILL after a delay if the process doesn't stop.
STOPSIGNAL SIGINT

HEALTHCHECK --interval=1m CMD curl --fail http://localhost:8081/api/health || exit 1