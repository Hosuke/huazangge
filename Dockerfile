FROM node:20-slim AS frontend
WORKDIR /build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
ARG CACHEBUST=1
RUN git clone --depth 1 https://github.com/Hosuke/llmbase.git
WORKDIR /build/llmbase/frontend
RUN npm ci && npx vite build

FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir git+https://github.com/Hosuke/llmbase.git gunicorn

COPY --from=frontend /build/llmbase/static/dist ./static/dist
COPY config.yaml wsgi.py ./
COPY tools/ ./tools/

# Seed data: copied to /app/seed, then moved to volume on first boot
COPY wiki/ ./seed/wiki/

# Entrypoint that initializes volume data if empty
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV PORT=5555
EXPOSE ${PORT}
ENTRYPOINT ["./entrypoint.sh"]
