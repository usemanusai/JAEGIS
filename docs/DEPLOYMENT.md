# JAEGIS Deployment Guide

## Overview

This guide covers deploying JAEGIS in various environments, from development to production. JAEGIS is designed to be flexible and can be deployed using multiple strategies.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Local Development](#local-development)
4. [Docker Deployment](#docker-deployment)
5. [Production Deployment](#production-deployment)
6. [Cloud Deployment](#cloud-deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Requirements:**
- Node.js 18.0.0 or higher
- Python 3.8 or higher
- 2GB RAM
- 1GB disk space
- Network access for GitHub API

**Recommended Requirements:**
- Node.js 20.0.0 or higher
- Python 3.11 or higher
- 4GB RAM
- 5GB disk space
- Redis for caching (optional but recommended)

### Dependencies

**Node.js Dependencies:**
```bash
npm install
```

**Python Dependencies:**
```bash
pip install -r requirements.txt
```

**Optional Dependencies:**
- Redis (for distributed caching)
- PM2 (for process management)
- Nginx (for reverse proxy)

## Environment Setup

### Environment Variables

Create a `.env` file in the project root:

```bash
# System Configuration
NODE_ENV=production
PORT=3000
HOST=0.0.0.0

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_COMMANDS_URL=https://raw.githubusercontent.com/usemanusai/JAEGIS/main/commands/commands.md

# Cache Configuration
CACHE_TYPE=memory
CACHE_DURATION=3600000
REDIS_URL=redis://localhost:6379

# Python Integration
PYTHON_HOST=localhost
PYTHON_PORT=5000
PYTHON_TIMEOUT=30000

# Security
SECRET_KEY=your_secret_key_here
CORS_ORIGIN=*

# Monitoring
ENABLE_MONITORING=true
LOG_LEVEL=info
LOG_FILE=logs/jaegis.log

# Performance
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=30000
RATE_LIMIT_WINDOW=60000
RATE_LIMIT_MAX=100
```

### Configuration Files

**config/production.json:**
```json
{
  "system": {
    "name": "JAEGIS Production",
    "version": "2.0.0",
    "environment": "production",
    "debug": false
  },
  "server": {
    "port": 3000,
    "host": "0.0.0.0",
    "cors": {
      "enabled": true,
      "origin": "*"
    }
  },
  "cache": {
    "enabled": true,
    "type": "redis",
    "duration": 3600000,
    "cleanup_interval": 300000
  },
  "monitoring": {
    "enabled": true,
    "interval": 30000,
    "retention": 86400000
  }
}
```

## Local Development

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/usemanusai/JAEGIS.git
cd JAEGIS
```

2. **Install dependencies:**
```bash
npm install
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start development server:**
```bash
npm run dev
```

5. **Test the installation:**
```bash
npm run health
```

### Development Scripts

```bash
# Start development server with hot reload
npm run dev

# Run tests
npm test

# Run linting
npm run lint

# Format code
npm run format

# Build documentation
npm run docs

# Run benchmarks
npm run benchmark
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["npm", "start"]
```

### Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  jaegis:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - jaegis
    restart: unless-stopped

volumes:
  redis_data:
```

### Build and Run

```bash
# Build the image
docker build -t jaegis:latest .

# Run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f jaegis
```

## Production Deployment

### Using PM2

1. **Install PM2:**
```bash
npm install -g pm2
```

2. **Create ecosystem file (ecosystem.config.js):**
```javascript
module.exports = {
  apps: [{
    name: 'jaegis',
    script: 'src/nodejs/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    log_file: 'logs/combined.log',
    out_file: 'logs/out.log',
    error_file: 'logs/error.log',
    log_date_format: 'YYYY-MM-DD HH:mm Z',
    merge_logs: true,
    max_memory_restart: '1G',
    node_args: '--max-old-space-size=1024'
  }]
}
```

3. **Deploy:**
```bash
# Start application
pm2 start ecosystem.config.js --env production

# Save PM2 configuration
pm2 save

# Setup startup script
pm2 startup

# Monitor
pm2 monit
```

### Nginx Configuration

**nginx.conf:**
```nginx
upstream jaegis {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://jaegis;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    location /ws {
        proxy_pass http://jaegis;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Systemd Service

**jaegis.service:**
```ini
[Unit]
Description=JAEGIS AI Agent Intelligence System
After=network.target

[Service]
Type=simple
User=jaegis
WorkingDirectory=/opt/jaegis
ExecStart=/usr/bin/node src/nodejs/index.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

```bash
# Install service
sudo cp jaegis.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jaegis
sudo systemctl start jaegis
```

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. **Launch EC2 instance:**
   - AMI: Amazon Linux 2
   - Instance type: t3.medium or larger
   - Security groups: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Setup instance:**
```bash
# Update system
sudo yum update -y

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs

# Install Git
sudo yum install -y git

# Clone and setup JAEGIS
git clone https://github.com/usemanusai/JAEGIS.git
cd JAEGIS
npm install --production
```

3. **Configure and start:**
```bash
# Setup environment
cp .env.example .env
# Edit .env file

# Start with PM2
npm install -g pm2
pm2 start ecosystem.config.js --env production
pm2 startup
pm2 save
```

#### Using ECS

**task-definition.json:**
```json
{
  "family": "jaegis",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "jaegis",
      "image": "your-account.dkr.ecr.region.amazonaws.com/jaegis:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/jaegis",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Using Cloud Run

1. **Build and push image:**
```bash
# Build image
docker build -t gcr.io/your-project/jaegis .

# Push to Container Registry
docker push gcr.io/your-project/jaegis
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy jaegis \
  --image gcr.io/your-project/jaegis \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3000 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

### Azure Deployment

#### Using Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name jaegis \
  --image your-registry.azurecr.io/jaegis:latest \
  --cpu 1 \
  --memory 1 \
  --ports 3000 \
  --environment-variables NODE_ENV=production \
  --restart-policy Always
```

## Monitoring & Maintenance

### Health Monitoring

**Health Check Script (health-check.sh):**
```bash
#!/bin/bash

ENDPOINT="http://localhost:3000/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ JAEGIS is healthy"
    exit 0
else
    echo "❌ JAEGIS health check failed (HTTP $RESPONSE)"
    exit 1
fi
```

### Log Management

**Logrotate configuration (/etc/logrotate.d/jaegis):**
```
/opt/jaegis/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 jaegis jaegis
    postrotate
        pm2 reloadLogs
    endscript
}
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/jaegis"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/ .env

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Performance Monitoring

**Monitoring Script (monitor.sh):**
```bash
#!/bin/bash

# Check CPU and Memory usage
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')
MEMORY=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')

# Check JAEGIS metrics
METRICS=$(curl -s http://localhost:3000/api/metrics)
ERROR_RATE=$(echo $METRICS | jq -r '.system.rates.errorRate')

echo "CPU: ${CPU}%, Memory: ${MEMORY}%, Error Rate: ${ERROR_RATE}%"

# Alert if thresholds exceeded
if (( $(echo "$CPU > 80" | bc -l) )); then
    echo "⚠️  High CPU usage: ${CPU}%"
fi

if (( $(echo "$MEMORY > 80" | bc -l) )); then
    echo "⚠️  High memory usage: ${MEMORY}%"
fi

if (( $(echo "$ERROR_RATE > 5" | bc -l) )); then
    echo "⚠️  High error rate: ${ERROR_RATE}%"
fi
```

## Troubleshooting

### Common Issues

#### Service Won't Start

```bash
# Check logs
pm2 logs jaegis

# Check configuration
npm run config validate

# Check dependencies
npm audit

# Check ports
netstat -tulpn | grep 3000
```

#### High Memory Usage

```bash
# Check memory usage
pm2 monit

# Restart with memory limit
pm2 restart jaegis --max-memory-restart 1G

# Check for memory leaks
node --inspect src/nodejs/index.js
```

#### Slow Performance

```bash
# Check system metrics
curl http://localhost:3000/api/metrics

# Check cache hit rate
curl http://localhost:3000/api/status

# Enable debug logging
DEBUG=jaegis:* pm2 restart jaegis
```

#### Connection Issues

```bash
# Check network connectivity
curl -I http://localhost:3000/health

# Check firewall
sudo ufw status

# Check DNS resolution
nslookup your-domain.com
```

### Debug Mode

```bash
# Start in debug mode
DEBUG=jaegis:* npm start

# Enable verbose logging
LOG_LEVEL=debug npm start

# Profile performance
node --prof src/nodejs/index.js
```

### Recovery Procedures

#### Automatic Recovery

```bash
#!/bin/bash
# auto-recovery.sh

if ! curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "Service unhealthy, attempting recovery..."
    
    # Try graceful restart
    pm2 restart jaegis
    sleep 30
    
    # Check if recovered
    if curl -f http://localhost:3000/health > /dev/null 2>&1; then
        echo "✅ Service recovered"
    else
        echo "❌ Recovery failed, manual intervention required"
        # Send alert
        echo "JAEGIS recovery failed" | mail -s "JAEGIS Alert" admin@example.com
    fi
fi
```

#### Manual Recovery

1. **Check service status:**
```bash
pm2 status
systemctl status jaegis
```

2. **Review logs:**
```bash
pm2 logs jaegis --lines 100
tail -f logs/error.log
```

3. **Restart services:**
```bash
pm2 restart all
systemctl restart jaegis
```

4. **Verify recovery:**
```bash
curl http://localhost:3000/health
npm run health
```

## Security Considerations

### Production Security

1. **Environment Variables:**
   - Use secure secret management
   - Rotate secrets regularly
   - Never commit secrets to version control

2. **Network Security:**
   - Use HTTPS in production
   - Configure proper CORS policies
   - Implement rate limiting

3. **Access Control:**
   - Run with non-root user
   - Implement authentication
   - Use proper file permissions

4. **Updates:**
   - Keep dependencies updated
   - Monitor security advisories
   - Implement automated security scanning

### SSL/TLS Configuration

```bash
# Generate SSL certificate with Let's Encrypt
sudo certbot --nginx -d your-domain.com

# Or use custom certificates
sudo mkdir -p /etc/nginx/ssl
sudo cp your-cert.pem /etc/nginx/ssl/cert.pem
sudo cp your-key.pem /etc/nginx/ssl/key.pem
sudo chmod 600 /etc/nginx/ssl/*
```

## Support

For deployment support:
- GitHub Issues: https://github.com/usemanusai/JAEGIS/issues
- Documentation: https://github.com/usemanusai/JAEGIS/docs
- Email: use.manus.ai@gmail.com

## Changelog

### Version 2.0.0
- Complete system rewrite
- Enhanced performance monitoring
- Improved error handling
- Docker support
- Cloud deployment guides