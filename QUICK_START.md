# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API Key
- Git (for cloning repository)

## Setup Instructions

### 1. Configure API Key

```bash
# Copy environment template
cp env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 2. Auto Start (Recommended for Windows)

```cmd
# Run the automated setup script
start-all.bat
```

### 3. Manual Start

```bash
# Terminal 1 - Backend Server
cd backend
pip install -r requirements.txt
python init_data.py  # First time only
python main.py

# Terminal 2 - Frontend Application
cd frontend/hutech-consultation
npm install  # First time only
npm start
```

### 4. Docker Compose (Alternative)

```bash
# Start all services with Docker
docker-compose up -d

# View logs
docker-compose logs -f
```

## Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Testing the System

```bash
# Run system tests
python test_system.py

# Test API endpoints
curl http://localhost:8000/majors
curl http://localhost:8000/admission-info/2024
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Backend: Change port in backend/main.py
   - Frontend: Change port in frontend/package.json

2. **API Key Issues**
   - Verify OpenAI API key is correct
   - Check API key has sufficient credits

3. **Database Errors**
   - Run: `python backend/init_data.py`
   - Check file permissions

### Logs and Debugging

```bash
# View backend logs
cd backend && python main.py

# View frontend logs
cd frontend/hutech-consultation && npm start

# Docker logs
docker-compose logs -f
```

## Next Steps

1. Test the counseling flow
2. Customize prompts in backend/prompts.py
3. Configure production settings
4. Deploy to server

## Support

- Email: tuyensinh@hutech.edu.vn
- Phone: 028 5445 7777
- Documentation: See README.md for detailed information