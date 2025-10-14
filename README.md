# HUTECH Career Counseling System - HuGo AI

## Overview

This is a local demo of HUTECH's career counseling system with **HuGo AI** - an intelligent career counselor using John L. Holland's RIASEC model for personality-based career guidance.

## Key Features

### HuGo AI Career Counseling
- Career counseling based on RIASEC model
- Personality discovery and career interests
- Automatic personality type classification
- Major suggestions suitable for HUTECH
- Interactive chat interface with restart functionality

### RIASEC Model
- **R - Realistic**: Technical, mechanical, hands-on
- **I - Investigative**: Analysis, research, exploration  
- **A - Artistic**: Creative, design, arts
- **S - Social**: Helping, interaction, care
- **E - Enterprising**: Leadership, persuasion, business
- **C - Conventional**: Stability, procedures, organization

### 7-Step Counseling Process
1. **Opening**: Introduce HuGo, create comfortable atmosphere
2. **Interest exploration**: Initial RIASEC group identification
3. **Personal abilities**: Understand strengths and learning style
4. **Career values**: What's important in work
5. **RIASEC assessment**: Confirm specific personality type
6. **Career guidance**: Suitable majors at HUTECH
7. **Closing**: Summary and encouragement

## Installation & Setup

### System Requirements
- **Python 3.8+**
- **Node.js 16+**
- **Docker & Docker Compose** (optional)
- **OpenAI API Key**

### Quick Start

**Windows - Auto Start (Recommended):**
```cmd
# 1. Configure API key
copy env.example .env
# Edit .env and add OPENAI_API_KEY=sk-your-key-here

# 2. Run auto-start script for both backend and frontend
start-all.bat
```

**Manual Setup:**
```powershell
# 1. Configure API key
copy env.example .env
# Edit .env and add OPENAI_API_KEY=sk-your-key-here

# 2. Initialize database
cd backend
python init_data.py
cd ..

# 3. Start backend (terminal 1)
cd backend
python main.py

# 4. Start frontend (terminal 2)
cd frontend/hutech-consultation
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Mode (Optional)

**Windows PowerShell:**
```powershell
# 1. Configure API key
copy env.example .env
# Edit .env and add OPENAI_API_KEY=sk-your-key-here

# 2. Run Docker deployment
.\deploy.ps1
```

**Access:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Nginx Proxy: http://localhost:8080

## Project Structure

```
Demo_local/
├── backend/                    # FastAPI server with HuGo AI
│   ├── main.py                # API endpoints
│   ├── prompts.py             # RIASEC prompts and logic
│   ├── init_data.py           # Initialize sample data
│   ├── hutech_consultation.db # SQLite database
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React app
│   └── hutech-consultation/
│       ├── src/
│       │   ├── App.js         # Main React component
│       │   └── components/    # React components
│       │       ├── ChatInterface.js    # Chat with HuGo AI
│       │       └── StudentInfoForm.js  # Student information form
│       └── package.json       # Node.js dependencies
├── start-all.bat              # Auto-start script
├── export_sqlite_to_csv.py    # Data export utility
├── check_data.ipynb           # Data analysis notebook
└── README.md                  # This file
```

## API Endpoints

### Student Information
```http
POST /student-info
Content-Type: application/json

{
  "student_name": "John Doe",
  "student_phone": "0123456789",
  "student_email": "john@example.com",
  "school_name": "High School ABC",
  "grade": "12"
}
```

### Career Counseling
```http
POST /consultation
Content-Type: application/json

{
  "student_name": "John Doe",
  "student_phone": "0123456789",
  "student_email": "john@example.com",
  "school_name": "High School ABC",
  "grade": "12",
  "question": "I want to explore my career personality",
  "score_range": "",
  "session_id": null,
  "history": []
}
```

### Session Management
```http
POST /consultation-sessions/{session_id}/end
```

### Available Majors
```http
GET /majors
```

### Admission Information
```http
GET /admission-info/2024
```

## Database Schema

### consultation_sessions
- id (INTEGER PRIMARY KEY)
- student_name (TEXT)
- student_phone (TEXT)
- student_email (TEXT)
- school_name (TEXT)
- grade (TEXT)
- score_range (TEXT)
- riasec_result (TEXT)
- suggested_majors (TEXT)
- status (TEXT)
- created_at (TIMESTAMP)
- ended_at (TIMESTAMP)

### consultation_messages
- id (INTEGER PRIMARY KEY)
- session_id (INTEGER)
- role (TEXT) - 'user' or 'assistant'
- content (TEXT)
- timestamp (TIMESTAMP)

## Data Export

Use the provided Python script to export data to CSV:

```bash
python export_sqlite_to_csv.py
```

This creates 4 CSV files:
- consultation_sessions_export.csv - Session information
- consultation_messages_export.csv - All chat messages
- consultation_combined_export.csv - Sessions with message statistics
- consultation_detailed_messages_export.csv - Messages with student info

## Features

### Chat Interface
- Real-time chat with HuGo AI
- Restart chat functionality (reload button)
- Mobile-responsive design
- Session management
- Message history tracking

### Student Information Form
- Input validation
- Mobile-friendly interface
- Data persistence

### Backend Features
- FastAPI with automatic API documentation
- SQLite database with session management
- OpenAI GPT integration
- CORS support for frontend
- Error handling and logging

## Testing

### Manual Testing
```bash
# Test student info endpoint
curl -X POST "http://localhost:8000/student-info" \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "John Doe",
    "student_phone": "0123456789",
    "student_email": "john@example.com",
    "school_name": "High School ABC",
    "grade": "12"
  }'

# Test consultation endpoint
curl -X POST "http://localhost:8000/consultation" \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "John Doe",
    "student_phone": "0123456789",
    "student_email": "john@example.com",
    "school_name": "High School ABC",
    "grade": "12",
    "question": "I want to explore my career personality"
  }'
```

## Troubleshooting

### Common Issues

1. **Invalid OpenAI API Key**
   ```bash
   # Check key in .env file
   type .env
   ```

2. **Port conflicts**
   ```bash
   # Check ports in use
   netstat -an | findstr :3000
   netstat -an | findstr :8000
   ```

3. **Python dependencies**
   ```bash
   # Reinstall dependencies
   cd backend
   pip install -r requirements.txt --force-reinstall
   ```

4. **Node.js dependencies**
   ```bash
   # Reinstall dependencies
   cd frontend/hutech-consultation
   rmdir /s node_modules
   del package-lock.json
   npm install
   ```

5. **Database issues**
   ```bash
   # Reinitialize database
   cd backend
   del hutech_consultation.db
   python init_data.py
   ```

## Environment Configuration

Create a `.env` file from the template:

```bash
copy env.example .env
```

Required environment variables:
- OPENAI_API_KEY: Your OpenAI API key
- DATABASE_URL: SQLite database path
- HOST: Server host (default: 0.0.0.0)
- PORT: Server port (default: 8000)
- DEBUG: Debug mode (default: true)

## Support

- **Email**: tuyensinh@hutech.edu.vn
- **Hotline**: 028 5445 7777
- **Website**: https://hutech.edu.vn

---

**HuGo AI - Discover your potential, shape your future!**