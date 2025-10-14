Server Deployment (Ubuntu + Docker)

Prerequisites
- Ubuntu 22.04/24.04 EC2, security group open port 80
- Docker & Docker Compose v2 installed
- OpenAI API key

Setup Steps
1) Copy project to server (e.g., /opt/hutech-app)
2) cd /opt/hutech-app/server
3) Create .env file in this folder:

OPENAI_API_KEY=sk-your-key-here
ALLOWED_ORIGINS=http://your-ec2-ip,http://your-domain

4) Start stack
   docker compose up -d --build

5) Access
   - Frontend: http://<EC2-IP>/
   - API: http://<EC2-IP>/api/

Notes
- Frontend still uses localhost in source; Nginx proxies /api to backend, so no code change needed.
- For HTTPS, attach a reverse proxy or extend nginx.conf with TLS certificates.


