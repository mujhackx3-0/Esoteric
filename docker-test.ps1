Write-Host "=== Docker Build & Test Script ===" -ForegroundColor Cyan

# Step 1: Build the Docker image
Write-Host ""
Write-Host "Step 1: Building Docker image..." -ForegroundColor Yellow
docker build -t esoteric-loan-assistant:latest -f Dockerfile .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Step 2: Run the container
Write-Host ""
Write-Host "Step 2: Starting container..." -ForegroundColor Yellow
docker run -d `
    --name esoteric-test `
    -p 8000:8000 `
    --env-file .env `
    esoteric-loan-assistant:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Container failed to start!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Container started" -ForegroundColor Green

# Step 3: Wait for app to be ready
Write-Host ""
Write-Host "Step 3: Waiting for application to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Step 4: Test health endpoint
Write-Host ""
Write-Host "Step 4: Testing health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    Write-Host "✅ Health check passed: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
    Write-Host "Container logs:" -ForegroundColor Yellow
    docker logs esoteric-test
    docker stop esoteric-test
    docker rm esoteric-test
    exit 1
}

# Step 5: Show logs
Write-Host ""
Write-Host "Step 5: Container logs:" -ForegroundColor Yellow
docker logs esoteric-test --tail 50

Write-Host ""
Write-Host "=== Docker test completed successfully! ===" -ForegroundColor Green
Write-Host "Container is running on http://localhost:8000" -ForegroundColor Cyan
Write-Host "To stop: docker stop esoteric-test" -ForegroundColor Yellow
Write-Host "To remove: docker rm esoteric-test" -ForegroundColor Yellow

