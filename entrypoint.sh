#!/bin/bash
# /app/data is the Railway volume mount point
# On first boot, seed it with wiki data from the image

if [ ! -f /app/data/.initialized ]; then
    echo "First boot: initializing persistent data volume..."
    mkdir -p /app/data/raw /app/data/wiki/concepts /app/data/wiki/_meta /app/data/wiki/outputs
    # Copy seed wiki data
    if [ -d /app/seed/wiki ]; then
        cp -rn /app/seed/wiki/* /app/data/wiki/ 2>/dev/null || true
    fi
    touch /app/data/.initialized
    echo "Volume initialized."
else
    echo "Volume already initialized. Preserving existing data."
fi

# Symlink so the app reads/writes to the volume
ln -sfn /app/data/raw /app/raw
ln -sfn /app/data/wiki /app/wiki

exec gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 4 --timeout 300 wsgi:app
