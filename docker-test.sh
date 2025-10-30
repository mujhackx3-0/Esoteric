#!/bin/bash

echo "=== Docker Build & Test Script ==="

# Step 1: Build the Docker image
echo ""
echo "Step 1: Building Docker image..."
docker build -t esoteric-loan-assistant:latest -f Dockerfile .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully"

# Step 2: Run the container
echo ""
echo "Step 2: Starting container..."
docker run -d \
    --name esoteric-test \
    -p 8000:8000 \
    --env-file .env \
    esoteric-loan-assistant:latest

if [ $? -ne 0 ]; then
    echo "❌ Container failed to start!"
    exit 1
fi

echo "✅ Container started"

# Step 3: Wait for app to be ready
echo ""
echo "Step 3: Waiting for application to be ready..."
sleep 10

# Step 4: Test health endpoint
echo ""
echo "Step 4: Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)

if [ $? -eq 0 ]; then
    echo "✅ Health check passed: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
    docker logs esoteric-test
    docker stop esoteric-test
    docker rm esoteric-test
    exit 1
fi

# Step 5: Show logs
echo ""
echo "Step 5: Container logs:"
docker logs esoteric-test --tail 50

echo ""
echo "=== Docker test completed successfully! ==="
echo "Container is running on http://localhost:8000"
echo "To stop: docker stop esoteric-test"
echo "To remove: docker rm esoteric-test"

