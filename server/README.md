# Server Deployment Guide

## Prerequisites

- Ubuntu 22.04/24.04 EC2 instance
- Security group configured to allow port 80 (HTTP)
- Docker and Docker Compose v2 installed
- OpenAI API key
- Git installed

## Setup Steps

### 1. Copy Project to Server

```bash
# Clone repository to server
git clone <repository-url> /opt/hutech-app
cd /opt/hutech-app/server
```

### 2. Configure Environment

```bash
# Create .env file in server directory
cat > .env << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Database Configuration
DATABASE_URL=sqlite:///./hutech_consultation.db

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://your-ec2-ip:80,http://your-ec2-ip,http://localhost:3000,http://127.0.0.1:3000

# Production Configuration
DEMO_MODE=false
DEBUG=false
EOF
```

### 3. Create Database Directory

```bash
# Create directory for persistent database storage
mkdir -p database
```

### 4. Start Application Stack

```bash
# Build and start all services
docker compose up -d --build

# Check service status
docker compose ps

# View logs
docker compose logs -f
```

### 5. Verify Deployment

```bash
# Test API endpoint
curl http://your-ec2-ip/api/majors

# Test frontend
curl -I http://your-ec2-ip
```

## Access Points

- **Frontend Application**: http://your-ec2-ip
- **Backend API**: http://your-ec2-ip/api
- **API Documentation**: http://your-ec2-ip/api/docs

## Architecture

The deployment uses a three-tier architecture:

1. **Nginx** (Port 80) - Reverse proxy and static file server
2. **Frontend** (Port 3000) - React application
3. **Backend** (Port 8000) - FastAPI application

### Request Flow

```
Client Request → Nginx (Port 80) → Frontend/Backend
```

- Static files and frontend routes: Nginx → Frontend
- API requests (/api/*): Nginx → Backend

## Configuration Details

### Nginx Configuration

The nginx.conf file handles:
- Static file serving for frontend
- API request proxying to backend
- URL rewriting for API calls
- CORS headers

### Database Persistence

Database files are stored in the `./database/` directory and mounted as a volume to ensure data persistence across container restarts.

### Environment Variables

Key environment variables:
- `OPENAI_API_KEY`: Required for AI functionality
- `ALLOWED_ORIGINS`: CORS configuration for production
- `DATABASE_URL`: SQLite database path
- `DEMO_MODE`: Set to false for production
- `DEBUG`: Set to false for production

## Maintenance

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f nginx
```

### Updating Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker compose down
docker compose up -d --build
```

### Database Backup

```bash
# Backup database
cp database/hutech_consultation.db database/backup_$(date +%Y%m%d).db

# Restore database
cp database/backup_20240101.db database/hutech_consultation.db
docker compose restart backend
```

### Monitoring

```bash
# Check container status
docker compose ps

# Check resource usage
docker stats

# Check disk space
df -h
```

## Security Considerations

1. **Firewall**: Ensure only necessary ports are open
2. **API Key**: Keep OpenAI API key secure
3. **Updates**: Regularly update Docker images and system packages
4. **Backups**: Regular database backups
5. **HTTPS**: Consider adding SSL/TLS certificates for production

## Troubleshooting

### Common Issues

1. **Port 80 Already in Use**
   ```bash
   sudo netstat -tlnp | grep :80
   sudo systemctl stop apache2  # If Apache is running
   ```

2. **Permission Issues**
   ```bash
   sudo chown -R $USER:$USER /opt/hutech-app
   ```

3. **Container Won't Start**
   ```bash
   docker compose logs backend
   docker compose logs frontend
   ```

4. **API Connection Errors**
   - Check ALLOWED_ORIGINS in .env
   - Verify OpenAI API key
   - Check network connectivity

### Performance Optimization

1. **Resource Limits**: Add resource limits to docker-compose.yml
2. **Caching**: Configure Nginx caching for static files
3. **Database**: Consider PostgreSQL for high-traffic scenarios
4. **Load Balancing**: Add multiple backend instances for scaling

## Support

For deployment issues:
- Check logs: `docker compose logs -f`
- Verify configuration: `docker compose config`
- Test connectivity: `curl http://localhost/api/majors`
- Contact: tuyensinh@hutech.edu.vn