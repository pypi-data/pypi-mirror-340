FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash app
RUN mkdir /data && chown -R app:app /data
VOLUME /data

ENV UV_SYSTEM_PYTHON=1
RUN uv pip install git+https://gitlab.com/meshadmin/meshadmin@migrate-to-uv

WORKDIR /home/app
