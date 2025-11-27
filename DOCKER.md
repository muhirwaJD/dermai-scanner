# 🐳 Docker Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access the app at `http://localhost:8501`

### Using Docker Commands

```bash
# Build image
docker build -t dermai-scanner:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  dermai-scanner:latest
```

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+ (optional)
- 4GB RAM minimum
- 10GB disk space

## Step-by-Step Deployment

### 1. Clone Repository

```bash
git clone https://github.com/muhirwaJD/dermai-scanner.git
cd dermai-scanner
```

### 2. Ensure Model is Present

```bash
# Check if model exists
ls -lh models/Skin_Cancer_Model_v1.keras

# If model is missing, download it or place it in the models/ directory
```

### 3. Build Docker Image

```bash
# Option A: Using docker-compose
docker-compose build

# Option B: Using Docker directly
docker build -t dermai-scanner:latest .
```

### 4. Run Container

```bash
# Option A: Using docker-compose
docker-compose up -d

# Option B: Using Docker directly
docker run -d -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  --name dermai-scanner \
  dermai-scanner:latest
```

### 5. Verify Deployment

```bash
# Check container status
docker ps

# View logs
docker logs dermai-scanner

# Or with docker-compose
docker-compose logs -f
```

### 6. Access Application

Open your browser and go to: `http://localhost:8501`

## Configuration

### Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` to customize settings:

```env
STREAMLIT_SERVER_PORT=8501
MODEL_PATH=models/Skin_Cancer_Model_v1.keras
MAX_UPLOAD_SIZE=200
```

### Volume Mounts

The Docker setup mounts two directories:

- `./models:/app/models` - Model files
- `./data:/app/data` - Training/test data

This allows you to:
- Update models without rebuilding the image
- Access uploaded images
- Manage training data

## Common Commands

### Using the Helper Script

```bash
# Make script executable
chmod +x docker-commands.sh

# Build image
./docker-commands.sh build

# Start services
./docker-commands.sh up

# View logs
./docker-commands.sh compose-logs

# Stop services
./docker-commands.sh down

# Rebuild after code changes
./docker-commands.sh rebuild

# Access container shell
./docker-commands.sh shell

# Clean up everything
./docker-commands.sh cleanup
```

### Manual Commands

```bash
# Build
docker build -t dermai-scanner:latest .

# Run (detached)
docker run -d -p 8501:8501 --name dermai-scanner dermai-scanner:latest

# Stop
docker stop dermai-scanner

# Remove container
docker rm dermai-scanner

# Remove image
docker rmi dermai-scanner:latest

# View logs
docker logs -f dermai-scanner

# Execute commands inside container
docker exec -it dermai-scanner /bin/bash

# Inspect container
docker inspect dermai-scanner
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs dermai-scanner

# Common issues:
# - Port 8501 already in use
# - Model file not found
# - Insufficient memory
```

### Port Already in Use

```bash
# Use different port
docker run -p 8502:8501 dermai-scanner:latest

# Or with docker-compose, edit docker-compose.yml:
ports:
  - "8502:8501"
```

### Model Not Found

```bash
# Ensure model is in the correct location
ls -lh models/Skin_Cancer_Model_v1.keras

# Ensure volume is mounted correctly
docker run -v $(pwd)/models:/app/models -p 8501:8501 dermai-scanner:latest
```

### Out of Memory

```bash
# Increase Docker memory limit in Docker Desktop settings
# Or specify memory limit:
docker run -m 4g -p 8501:8501 dermai-scanner:latest
```

### Rebuild After Code Changes

```bash
# Stop and remove old container
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Or without docker-compose:
docker stop dermai-scanner
docker rm dermai-scanner
docker build -t dermai-scanner:latest .
docker run -d -p 8501:8501 --name dermai-scanner dermai-scanner:latest
```

## Production Deployment

### Using Environment Variables

```bash
docker run -d -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e MODEL_PATH=/app/models/Skin_Cancer_Model_v1.keras \
  -v $(pwd)/models:/app/models \
  --name dermai-scanner \
  dermai-scanner:latest
```

### With Docker Compose and .env File

1. Create `.env` file with your settings
2. Docker Compose will automatically load it:

```bash
docker-compose up -d
```

### Health Checks

The container includes a health check:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' dermai-scanner

# View health check logs
docker inspect --format='{{json .State.Health}}' dermai-scanner | jq
```

## Performance Optimization

### Multi-Stage Build (Smaller Image)

The Dockerfile uses a single-stage build for simplicity. For a smaller image, create `Dockerfile.optimized`:

```dockerfile
# Stage 1: Builder
FROM python:3.10.14-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
COPY requirements-docker.txt .
RUN pip install --user --no-cache-dir -r requirements-docker.txt

# Stage 2: Runtime
FROM python:3.10.14-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build with:
```bash
docker build -f Dockerfile.optimized -t dermai-scanner:optimized .
```

## Monitoring

### View Real-Time Logs

```bash
docker logs -f dermai-scanner
```

### Monitor Resource Usage

```bash
docker stats dermai-scanner
```

### Container Metrics

```bash
# CPU and memory usage
docker stats --no-stream dermai-scanner

# Disk usage
docker system df
```

## Cleanup

### Remove Containers and Images

```bash
# Stop and remove container
docker stop dermai-scanner
docker rm dermai-scanner

# Remove image
docker rmi dermai-scanner:latest

# Or use docker-compose
docker-compose down

# Remove volumes too
docker-compose down -v
```

### Complete Cleanup

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Clean everything
docker system prune -a --volumes
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Docker logs: `docker logs dermai-scanner`
- Open an issue on GitHub
