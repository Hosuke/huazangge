FROM node:20-slim AS frontend
WORKDIR /build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
# Force fresh clone every build by using ADD with a URL that changes
ADD https://api.github.com/repos/Hosuke/llmbase/git/refs/heads/main /tmp/llmbase-version
RUN git clone --depth 1 https://github.com/Hosuke/llmbase.git
WORKDIR /build/llmbase/frontend
RUN npm ci && npx vite build

FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
ADD https://api.github.com/repos/Hosuke/llmbase/git/refs/heads/main /tmp/llmbase-version2
RUN pip install --no-cache-dir git+https://github.com/Hosuke/llmbase.git gunicorn
COPY --from=frontend /build/llmbase/static/dist ./static/dist
COPY config.yaml wsgi.py entrypoint.sh ./
COPY tools/ ./tools/
COPY wiki/ ./wiki/
RUN chmod +x entrypoint.sh && mkdir -p raw wiki/outputs

ENV PORT=5555
EXPOSE ${PORT}
ENTRYPOINT ["./entrypoint.sh"]
# Sun Apr  5 13:37:00 UTC 2026
# Tue Apr  7 08:27:50 UTC 2026
