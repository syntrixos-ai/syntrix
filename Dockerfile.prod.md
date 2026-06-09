# Syntrix AI - Build Configuration

This Dockerfile builds a production-ready container for Syntrix AI.

## Build

```bash
docker build -t syntrix:latest -f Dockerfile.prod .
```

## Run

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://..." \
  -e GROQ_API_KEY="your-key" \
  -e SECRET_KEY="your-secret" \
  syntrix:latest
```

## Features

- Multi-stage build for smaller image size
- Non-root user for security
- Health checks
- Automatic database migrations
- Production-optimized dependencies
