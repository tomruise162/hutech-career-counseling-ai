# HUTECH Career Counseling System - HuGo AI

## Overview

This is a career counseling system for HUTECH University featuring HuGo AI - an intelligent career counselor that uses John L. Holland's RIASEC model to provide personalized career guidance and major recommendations.

## Key Features

### HuGo AI Career Counseling
- Career counseling based on RIASEC personality model
- Interactive personality discovery and assessment
- Automatic personality type classification
- Personalized major suggestions for HUTECH programs
- Chat interface with session management and restart functionality

### RIASEC Model Implementation
- **R - Realistic**: Technical, mechanical, hands-on careers
- **I - Investigative**: Analysis, research, exploration careers
- **A - Artistic**: Creative, design, arts careers
- **S - Social**: Helping, interaction, care careers
- **E - Enterprising**: Leadership, persuasion, business careers
- **C - Conventional**: Stability, procedures, organization careers

### 7-Step Counseling Process
1. **Opening**: Introduction and atmosphere setting
2. **Interest exploration**: Initial RIASEC group identification
3. **Personal abilities**: Understanding strengths and learning style
4. **Career values**: Identifying work priorities
5. **RIASEC assessment**: Confirming specific personality type
6. **Career guidance**: Recommending suitable HUTECH majors
7. **Closing**: Summary and encouragement

## System Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- Docker and Docker Compose (for containerized deployment)
- OpenAI API Key
- Modern web browser

## Installation and Setup

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd hutech-career-counseling-ai
```

2. **Configure environment variables**
```bash
# Copy environment template
cp env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
python init_data.py
cd ..
```

4. **Install frontend dependencies**
```bash
cd frontend/hutech-consultation
npm install
cd ../..
```

### Running the Application

#### Option 1: Manual Start
```bash
# Start backend server
cd backend
python main.py

# In another terminal, start frontend
cd frontend/hutech-consultation
npm start
```

#### Option 2: Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Option 3: Windows Auto Start
```cmd
# Run the automated setup script
start-all.bat
```

## Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Interface**: http://localhost:8000/admin

## API Endpoints

### Student Information
- `POST /student-info` - Save student information
- `GET /student-info/{student_id}` - Retrieve student information

### Career Counseling
- `POST /consultation` - Start or continue counseling session
- `GET /consultation-sessions/{session_id}` - Get session details
- `POST /consultation-sessions/{session_id}/end` - End counseling session

### Academic Information
- `GET /majors` - Get all available majors
- `GET /admission-info/{year}` - Get admission information for specific year

## Database Schema

The system uses SQLite database with the following main tables:
- `students` - Student information
- `consultation_sessions` - Counseling session data
- `majors` - Available academic programs
- `admission_info` - Admission requirements and statistics

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `DATABASE_URL` - Database connection string
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `ALLOWED_ORIGINS` - CORS allowed origins
- `DEMO_MODE` - Enable demo mode (default: true)
- `DEBUG` - Enable debug mode (default: true)

### Customization

You can customize the counseling prompts and responses by editing:
- `backend/prompts.py` - Main counseling prompts
- `backend/prompt_config.json` - Prompt configuration
- `frontend/src/components/` - UI components

## Deployment

### Production Deployment

1. **Server Requirements**
   - Ubuntu 20.04+ or CentOS 8+
   - Minimum 2GB RAM (recommended 4GB+)
   - 10GB+ free storage
   - Docker and Docker Compose installed

2. **Deployment Steps**
```bash
# Clone repository
git clone <repository-url>
cd hutech-career-counseling-ai

# Configure environment
cp env.example .env
# Edit .env with production settings

# Deploy with Docker Compose
cd server
docker-compose up -d
```

3. **Access Points**
   - Application: http://your-server-ip
   - API: http://your-server-ip/api
   - Documentation: http://your-server-ip/api/docs

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify OpenAI API key is correct
   - Check network connectivity
   - Ensure backend server is running

2. **Database Issues**
   - Check database file permissions
   - Verify SQLite installation
   - Run database initialization script

3. **Frontend Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

### Logs and Debugging

```bash
# View application logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check database
sqlite3 hutech_consultation.db ".tables"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For technical support or questions:
- Email: tuyensinh@hutech.edu.vn
- Phone: 028 5445 7777
- Documentation: See docs/ folder for detailed guides

## Changelog

### Version 1.0.0
- Initial release with HuGo AI counseling system
- RIASEC model implementation
- Interactive chat interface
- Major recommendation system
- Session management
- Docker deployment support