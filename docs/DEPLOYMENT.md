# 🚀 Hướng Dẫn Deploy HUTECH Tư Vấn Tuyển Sinh

## 📋 Yêu cầu hệ thống

### Server Requirements
- **OS**: Ubuntu 20.04+ hoặc CentOS 8+
- **RAM**: Tối thiểu 2GB (khuyến nghị 4GB+)
- **Storage**: Tối thiểu 10GB free space
- **Network**: Kết nối internet ổn định

### Software Requirements
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: Để clone source code
- **OpenAI API Key**: Để sử dụng ChatGPT

## 🔧 Cài đặt môi trường

### 1. Cập nhật hệ thống
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Cài đặt Docker
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

### 3. Cài đặt Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 4. Logout và login lại
```bash
# Để áp dụng group permissions
exit
# Login lại
```

## 📥 Deploy ứng dụng

### 1. Clone source code
```bash
git clone <repository-url>
cd Hutech_project
```

### 2. Cấu hình environment
```bash
# Copy file environment mẫu
cp backend/env_example.txt .env

# Chỉnh sửa file .env
nano .env
```

Cập nhật các thông tin sau:
```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Database Configuration
DATABASE_URL=sqlite:///./hutech_consultation.db

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com
```

### 3. Deploy với script tự động
```bash
# Cấp quyền thực thi
chmod +x deploy.sh

# Chạy deploy
./deploy.sh
```

### 4. Deploy thủ công (nếu cần)
```bash
# Tạo thư mục cần thiết
mkdir -p database ssl

# Build và start containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Khởi tạo dữ liệu mẫu
sleep 10
docker-compose exec backend python init_data.py
```

## 🌐 Cấu hình Domain & SSL

### 1. Cài đặt Nginx (nếu không dùng Docker)
```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 2. Cấu hình domain
```bash
# Tạo file cấu hình Nginx
sudo nano /etc/nginx/sites-available/hutech-consultation
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hutech-consultation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Cài đặt SSL với Let's Encrypt
```bash
# Cài đặt Certbot
sudo apt install certbot python3-certbot-nginx -y

# Tạo SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## 🔒 Cấu hình Firewall

### Ubuntu/Debian (UFW)
```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22

# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Check status
sudo ufw status
```

### CentOS/RHEL (Firewalld)
```bash
# Start firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Allow services
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Reload
sudo firewall-cmd --reload
```

## 📊 Monitoring & Maintenance

### 1. Systemd Service
```bash
# Tạo systemd service
sudo nano /etc/systemd/system/hutech-consultation.service
```

```ini
[Unit]
Description=HUTECH Consultation System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/Hutech_project
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl enable hutech-consultation.service
sudo systemctl start hutech-consultation.service
```

### 2. Log rotation
```bash
# Tạo logrotate config
sudo nano /etc/logrotate.d/hutech-consultation
```

```
/var/log/hutech-consultation/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        docker-compose restart
    endscript
}
```

### 3. Backup script
```bash
# Tạo backup script
nano backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backup/hutech-consultation"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec -T backend cp hutech_consultation.db /app/database/backup_$DATE.db

# Backup source code
tar -czf $BACKUP_DIR/source_$DATE.tar.gz /path/to/Hutech_project

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# Cấp quyền và thêm vào crontab
chmod +x backup.sh
crontab -e

# Thêm dòng sau để backup hàng ngày lúc 2:00 AM
0 2 * * * /path/to/backup.sh
```

## 🔧 Troubleshooting

### 1. Kiểm tra trạng thái services
```bash
# Docker containers
docker-compose ps

# Systemd service
sudo systemctl status hutech-consultation.service

# Nginx
sudo systemctl status nginx

# Logs
docker-compose logs -f
```

### 2. Lỗi thường gặp

#### Container không start
```bash
# Xem logs chi tiết
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### Port conflicts
```bash
# Kiểm tra port đang sử dụng
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill process sử dụng port
sudo kill -9 $(lsof -t -i:8000)
```

#### Database issues
```bash
# Kiểm tra database file
docker-compose exec backend ls -la *.db

# Recreate database
docker-compose exec backend rm -f hutech_consultation.db
docker-compose exec backend python init_data.py
```

#### SSL certificate issues
```bash
# Renew certificate
sudo certbot renew

# Test certificate
sudo certbot certificates
```

### 3. Performance optimization

#### Nginx optimization
```nginx
# Thêm vào nginx.conf
worker_processes auto;
worker_connections 1024;

http {
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    client_max_body_size 10M;
    client_body_timeout 60s;
    client_header_timeout 60s;
}
```

#### Docker optimization
```yaml
# Thêm vào docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

## 📈 Scaling

### 1. Load balancing
```nginx
upstream backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

upstream frontend {
    server localhost:3000;
    server localhost:3001;
}
```

### 2. Database scaling
```yaml
# Sử dụng PostgreSQL thay vì SQLite
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: hutech_consultation
      POSTGRES_USER: hutech
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    environment:
      DATABASE_URL: postgresql://hutech:your_password@postgres:5432/hutech_consultation
```

## 🔄 Updates & Maintenance

### 1. Update application
```bash
# Pull latest code
git pull origin main

# Rebuild và restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Update database nếu cần
docker-compose exec backend python init_data.py
```

### 2. System updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Restart services
sudo systemctl restart docker
sudo systemctl restart hutech-consultation.service
```

### 3. Security updates
```bash
# Check for security updates
sudo apt list --upgradable

# Update dependencies
docker-compose exec backend pip install --upgrade -r requirements.txt
docker-compose exec frontend npm update
```

---

**Lưu ý**: Luôn backup dữ liệu trước khi thực hiện updates hoặc thay đổi cấu hình!
