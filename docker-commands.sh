#!/bin/bash
# Docker Commands for DermAI Scanner

echo "DermAI Scanner - Docker Management Commands"
echo "==========================================="
echo ""

# Build the Docker image
build() {
    echo "Building Docker image..."
    docker build -t dermai-scanner:latest .
}

# Run container (simple)
run() {
    echo "Running container on port 8501..."
    docker run -p 8501:8501 dermai-scanner:latest
}

# Run container with volume mounts
run_with_volumes() {
    echo "Running container with volume mounts..."
    docker run -p 8501:8501 \
      -v $(pwd)/models:/app/models \
      -v $(pwd)/data:/app/data \
      dermai-scanner:latest
}

# Run container in detached mode
run_detached() {
    echo "Running container in detached mode..."
    docker run -d -p 8501:8501 --name dermai-scanner dermai-scanner:latest
}

# Using docker-compose (recommended)
compose_up() {
    echo "Starting services with docker-compose..."
    docker-compose up -d
}

# View logs
logs() {
    echo "Viewing container logs..."
    docker logs dermai-scanner
}

# View logs (docker-compose)
compose_logs() {
    echo "Viewing docker-compose logs..."
    docker-compose logs -f
}

# Stop container
stop() {
    echo "Stopping container..."
    docker stop dermai-scanner
}

# Stop docker-compose
compose_down() {
    echo "Stopping docker-compose services..."
    docker-compose down
}

# Remove container
remove() {
    echo "Removing container..."
    docker rm dermai-scanner
}

# Remove image
remove_image() {
    echo "Removing image..."
    docker rmi dermai-scanner:latest
}

# Rebuild and restart
rebuild() {
    echo "Rebuilding and restarting..."
    docker-compose up -d --build
}

# Access container shell
shell() {
    echo "Accessing container shell..."
    docker exec -it dermai-scanner /bin/bash
}

# Clean up everything
cleanup() {
    echo "Cleaning up Docker resources..."
    docker-compose down -v
    docker system prune -a
}

# Show menu
case "$1" in
    build)
        build
        ;;
    run)
        run
        ;;
    run-volumes)
        run_with_volumes
        ;;
    run-detached)
        run_detached
        ;;
    up)
        compose_up
        ;;
    logs)
        logs
        ;;
    compose-logs)
        compose_logs
        ;;
    stop)
        stop
        ;;
    down)
        compose_down
        ;;
    remove)
        remove
        ;;
    remove-image)
        remove_image
        ;;
    rebuild)
        rebuild
        ;;
    shell)
        shell
        ;;
    cleanup)
        cleanup
        ;;
    *)
        echo "Usage: $0 {build|run|run-volumes|run-detached|up|logs|compose-logs|stop|down|remove|remove-image|rebuild|shell|cleanup}"
        echo ""
        echo "Commands:"
        echo "  build         - Build Docker image"
        echo "  run           - Run container (simple)"
        echo "  run-volumes   - Run with volume mounts"
        echo "  run-detached  - Run in background"
        echo "  up            - Start with docker-compose"
        echo "  logs          - View container logs"
        echo "  compose-logs  - View docker-compose logs"
        echo "  stop          - Stop container"
        echo "  down          - Stop docker-compose"
        echo "  remove        - Remove container"
        echo "  remove-image  - Remove image"
        echo "  rebuild       - Rebuild and restart"
        echo "  shell         - Access container shell"
        echo "  cleanup       - Clean up all resources"
        exit 1
esac
