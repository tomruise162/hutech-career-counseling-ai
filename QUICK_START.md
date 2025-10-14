# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key

## Setup

1. **Configure API Key**
   ```bash
   # Edit backend/.env and add your OpenAI API key
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

2. **Auto Start (Recommended)**
   ```cmd
   start-all.bat
   ```

3. **Manual Start**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python init_data.py  # First time only
   python main.py

   # Terminal 2 - Frontend
   cd frontend/hutech-consultation
   npm install  # First time only
   npm start
   ```

## Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Testing
```bash
python test_system.py
```

## Support
- Email: tuyensinh@hutech.edu.vn
- Hotline: 028 5445 7777
