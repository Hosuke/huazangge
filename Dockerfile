FROM node:20-slim AS frontend
WORKDIR /build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/Hosuke/llmbase.git
WORKDIR /build/llmbase/frontend
RUN npm ci && npx vite build

FROM python:3.12-slim
WORKDIR /app

# Install system deps + llmbase
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir git+https://github.com/Hosuke/llmbase.git gunicorn

# Copy frontend build
COPY --from=frontend /build/llmbase/static/dist ./static/dist

# Copy config, tools, wiki (not raw - too large for upload)
COPY config.yaml wsgi.py ./
COPY tools/ ./tools/
COPY wiki/ ./wiki/
RUN mkdir -p raw wiki/outputs

ENV PORT=5555
EXPOSE ${PORT}
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 4 --timeout 300 wsgi:app
# 2026-04-04T18:17:57Z
