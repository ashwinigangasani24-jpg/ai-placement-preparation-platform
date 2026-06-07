# Deployment Guide

## Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` in backend `.env` with strong random value
- [ ] Change PostgreSQL password from default
- [ ] Set `DEBUG=False` if applicable
- [ ] Update `CORS_ORIGINS` to match production domain
- [ ] Configure `NEXT_PUBLIC_API_URL` for production backend
- [ ] Set up SSL/TLS certificates
- [ ] Configure domain and DNS
- [ ] Set up email service for notifications
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging

## Deployment Options

### Option 1: Docker Compose on VPS

**Requirements**: Docker, Docker Compose, VPS with public IP

**Steps**:

```bash
# 1. Clone repository
git clone <your-repo-url>
cd placement-intelligence

# 2. Update .env files for production
# backend/.env
DATABASE_URL=postgresql://user:password@db:5432/placement
SECRET_KEY=<strong-random-key>
CORS_ORIGINS=https://yourdomain.com

# frontend/.env.local (or in docker-compose.yml)
NEXT_PUBLIC_API_URL=https://api.yourdomain.com

# 3. Update docker-compose.yml for production
# Change localhost to yourdomain.com, configure reverse proxy

# 4. Start services
docker-compose -f docker-compose.yml up -d

# 5. Verify services
curl https://api.yourdomain.com/health
curl https://yourdomain.com
```

### Option 2: Vercel + Railway

**Requirements**: Vercel account, Railway account

**Steps**:

1. **Deploy Frontend to Vercel**:
   ```bash
   npm install -g vercel
   cd frontend
   vercel --prod
   ```

2. **Deploy Backend to Railway**:
   - Create Railway project
   - Connect GitHub repository
   - Add environment variables
   - Deploy

3. **Configure Database on Railway**:
   - Create PostgreSQL service
   - Update DATABASE_URL

### Option 3: AWS / Google Cloud / Azure

**Using Application Load Balancer**:

```yaml
# Example terraform configuration (AWS)
resource "aws_ecs_cluster" "placement" {
  name = "placement-cluster"
}

resource "aws_ecs_service" "backend" {
  name            = "placement-backend"
  cluster         = aws_ecs_cluster.placement.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 3
  
  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "placement-backend"
    container_port   = 8000
  }
}
```

## Database Initialization

### First-Time Setup

```bash
# 1. Ensure PostgreSQL is running
# 2. Connect to database
psql -U postgres -h localhost

# 3. Create database
CREATE DATABASE placement;

# 4. Connect to database
\c placement

# 5. Run backend to create tables
cd backend
source .venv/bin/activate
python -c "from app.db.session import engine; from app.db.models import Base; Base.metadata.create_all(bind=engine)"
```

### Automated Migrations

Create `backend/app/db/init_db.py`:

```python
from sqlalchemy import create_engine
from app.db.models import Base
from app.core.config import settings

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

if __name__ == "__main__":
    init_db()
```

Run during deployment:
```bash
python app/db/init_db.py
```

## Monitoring & Logging

### Application Monitoring

```python
# backend/app/middleware/logging.py
import logging
from fastapi import Request
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response
```

### Health Check

```bash
# Monitor endpoint
curl https://yourdomain.com/health

# Expected response
{"status": "ok", "service": "placement-intelligence-api"}
```

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Nginx or AWS ALB
2. **Multiple Backend Instances**: Run multiple uvicorn workers
3. **Database Replication**: PostgreSQL streaming replication
4. **Cache Layer**: Redis for session/data caching
5. **CDN**: CloudFront or Cloudflare for static assets

### Performance Optimization

```python
# backend/app/main.py
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Add caching headers
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400,  # 24 hours
)
```

## Backup Strategy

### PostgreSQL Backup

```bash
#!/bin/bash
# Daily backup script
BACKUP_DIR="/backups/placement"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U postgres placement > \
    $BACKUP_DIR/placement_$TIMESTAMP.sql

# Compress backup
gzip $BACKUP_DIR/placement_$TIMESTAMP.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
```

### Automated Backups to S3

```bash
# Add to cron: 0 2 * * * /scripts/backup.sh
aws s3 cp $BACKUP_DIR/placement_$TIMESTAMP.sql.gz \
    s3://placement-backups/
```

## Rollback Procedure

```bash
# 1. Keep previous Docker images
docker images | grep placement

# 2. To rollback
docker-compose down
# Update docker-compose.yml to use previous image version
docker-compose up -d

# 3. Restore database backup if needed
pg_restore -d placement /backups/placement_$TIMESTAMP.sql
```

## Security Hardening

### Network Security

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - SECURE_COOKIE=true
      - SAMESITE_COOKIE=Lax
    networks:
      - internal
    
networks:
  internal:
    driver: bridge
```

### Secrets Management

Use AWS Secrets Manager or similar:

```python
import boto3

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='placement-prod-secrets')
```

## Continuous Deployment

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker images
        run: docker build -t placement:latest .
      - name: Deploy to server
        run: |
          ssh user@server "cd /app && git pull && docker-compose up -d"
```

## Troubleshooting Deployment

### Issue: Connection Refused
```bash
# Check if services are running
docker ps

# Check logs
docker logs placement-backend
docker logs placement-frontend
```

### Issue: Database Connection Error
```bash
# Test database connection
psql -h host -U user -d placement -c "SELECT 1"

# Check environment variables
docker exec placement-backend env | grep DATABASE_URL
```

### Issue: CORS Errors
```bash
# Verify CORS origins
curl -H "Origin: https://yourdomain.com" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS https://api.yourdomain.com/api/auth/register
```

## Support & Resources

- [FastAPI Deployment Docs](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment Docs](https://nextjs.org/docs/deployment)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
