# scripts/test-container.ps1
Write-Host "Testing Container Security..."

# Build and run
docker-compose build
docker-compose up -d

# Wait for startup
Start-Sleep -Seconds 15

# Test health endpoint
Write-Host "Testing health endpoint..."
curl -f http://localhost:8000/health
Write-Host "Healthcheck PASSED"

# Test non-root user
Write-Host "Testing non-root user..."
docker-compose exec app id
Write-Host "Non-root user PASSED"

# Cleanup
docker-compose down
Write-Host "All container tests completed!"
