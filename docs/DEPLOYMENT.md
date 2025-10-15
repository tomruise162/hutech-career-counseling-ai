# HUTECH Career Counseling System - Deployment Guide

## System Requirements

### Server Requirements
- **Operating System**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: Minimum 2GB (recommended 4GB+)
- **Storage**: Minimum 10GB free space
- **Network**: Stable internet connection
- **CPU**: 2+ cores recommended

### Software Requirements
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning source code
- **OpenAI API Key**: For AI functionality

## Environment Setup

### 1. System Update

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Docker Installation

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 3. Docker Compose Installation

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 4. Apply Group Permissions

```bash
# Logout and login again to apply docker group permissions
exit
# Login again
```

## Application Deployment

### 1. Clone Source Code

```bash
git clone <repository-url>
cd hutech-career-counseling-ai
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit environment file
nano .env
```

Update the following information:
```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Database Configuration
DATABASE_URL=sqlite:///./hutech_consultation.db

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com,http://your-server-ip

# Production Configuration
DEMO_MODE=false
DEBUG=false
```

### 3. Server Deployment

```bash
# Navigate to server directory
cd server

# Create database directory
mkdir -p database

# Create .env file for server
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
DATABASE_URL=sqlite:///./hutech_consultation.db
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://your-server-ip:80,http://your-server-ip,http://localhost:3000
DEMO_MODE=false
DEBUG=false
EOF

# Deploy application stack
docker compose up -d --build
```

### 4. Manual Deployment (Alternative)

```bash
# Create necessary directories
mkdir -p database ssl

# Set proper permissions
chmod 755 database
chmod 700 ssl

# Start services
docker compose up -d

# Check service status
docker compose ps
```

## Verification and Testing

### 1. Check Service Status

```bash
# View running containers
docker compose ps

# Check logs
docker compose logs -f

# Test API endpoint
curl http://localhost/api/majors
```

### 2. Access Points

- **Frontend Application**: http://your-server-ip
- **Backend API**: http://your-server-ip/api
- **API Documentation**: http://your-server-ip/api/docs

### 3. Health Checks

```bash
# Test frontend
curl -I http://your-server-ip

# Test API
curl http://your-server-ip/api/majors

# Test database
docker compose exec backend python -c "import sqlite3; print('Database OK')"
```

## Configuration Management

### Environment Variables

Key environment variables for production:

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Database
DATABASE_URL=sqlite:///./hutech_consultation.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS (Production)
ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com

# Production Settings
DEMO_MODE=false
DEBUG=false
```

### Nginx Configuration

The nginx.conf handles:
- Static file serving
- API request proxying
- URL rewriting
- CORS headers

### Database Configuration

- SQLite database for simplicity
- Persistent storage via Docker volumes
- Automatic backup recommendations

## Security Configuration

### 1. Firewall Setup

```bash
# Ubuntu/Debian
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS (if using SSL)
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

### 2. SSL/TLS Configuration (Optional)

```bash
# Generate SSL certificate (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx.conf for HTTPS
# Add SSL configuration to nginx.conf
```

### 3. API Key Security

- Store API keys in environment variables
- Never commit API keys to version control
- Use different keys for development and production
- Regularly rotate API keys

## Monitoring and Maintenance

### 1. Log Management

```bash
# View application logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f nginx

# Log rotation (optional)
sudo logrotate /etc/logrotate.d/docker
```

### 2. Database Backup

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
mkdir -p $BACKUP_DIR

# Backup database
docker compose exec -T backend cp hutech_consultation.db /app/database/backup_$DATE.db
cp database/backup_$DATE.db $BACKUP_DIR/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "Backup completed: backup_$DATE.db"
EOF

chmod +x backup.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### 3. System Monitoring

```bash
# Check resource usage
docker stats

# Check disk space
df -h

# Check memory usage
free -h

# Check system load
uptime
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Check what's using port 80
sudo netstat -tlnp | grep :80
sudo lsof -i :80

# Stop conflicting services
sudo systemctl stop apache2
sudo systemctl stop nginx
```

2. **Permission Issues**
```bash
# Fix ownership
sudo chown -R $USER:$USER /opt/hutech-app
chmod -R 755 /opt/hutech-app
```

3. **Container Won't Start**
```bash
# Check logs
docker compose logs backend
docker compose logs frontend

# Check configuration
docker compose config

# Rebuild containers
docker compose down
docker compose up -d --build
```

4. **Database Issues**
```bash
# Check database file
ls -la database/

# Recreate database
docker compose exec backend python init_data.py

# Check database integrity
docker compose exec backend python -c "import sqlite3; conn = sqlite3.connect('hutech_consultation.db'); print('Database OK')"
```

5. **API Connection Errors**
```bash
# Check CORS configuration
grep ALLOWED_ORIGINS .env

# Test API directly
curl -v http://localhost:8000/majors

# Check OpenAI API key
docker compose exec backend python -c "import os; print('API Key:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

### Performance Optimization

1. **Resource Limits**
```yaml
# Add to docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

2. **Database Optimization**
- Consider PostgreSQL for high-traffic scenarios
- Implement database connection pooling
- Add database indexes for frequently queried fields

3. **Caching**
- Configure Nginx caching for static files
- Implement Redis for session caching
- Add application-level caching

## Scaling and High Availability

### Horizontal Scaling

```yaml
# docker-compose.yml for multiple backend instances
services:
  backend:
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/hutech_db
```

### Load Balancing

```nginx
# nginx.conf for load balancing
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

### Database Migration

```bash
# Migrate to PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_DB=hutech_consultation \
  -e POSTGRES_USER=hutech \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 postgres:13

# Export SQLite data
sqlite3 hutech_consultation.db .dump > data.sql

# Import to PostgreSQL
psql -h localhost -U hutech -d hutech_consultation < data.sql
```

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Check application logs
   - Verify backup completion
   - Monitor resource usage

2. **Monthly**
   - Update system packages
   - Review security logs
   - Test disaster recovery procedures

3. **Quarterly**
   - Update Docker images
   - Review and rotate API keys
   - Performance optimization review

### Support Contacts

- **Technical Support**: tuyensinh@hutech.edu.vn
- **Phone**: 028 5445 7777
- **Documentation**: See README.md for detailed information

### Emergency Procedures

1. **Service Down**
   ```bash
   docker compose restart
   docker compose logs -f
   ```

2. **Database Corruption**
   ```bash
   # Restore from backup
   cp database/backup_YYYYMMDD.db database/hutech_consultation.db
   docker compose restart backend
   ```

3. **High Resource Usage**
   ```bash
   # Check resource usage
   docker stats
   # Restart services if needed
   docker compose restart
   ```