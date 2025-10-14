from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from datetime import datetime
import json
from typing import List, Optional
import openai
from dotenv import load_dotenv
import sqlite3
import logging
from prompts import SYSTEM_PROMPT, AI_CONFIG

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="HUTECH Tư Vấn Tuyển Sinh API",
    description="API tư vấn tuyển sinh cho học sinh sử dụng ChatGPT",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database setup
DATABASE_URL = "sqlite:///./hutech_consultation.db"

def get_db_connection():
    """Get SQLite database connection with proper configuration"""
    conn = sqlite3.connect("hutech_consultation.db", timeout=30.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=1000")
    conn.execute("PRAGMA temp_store=MEMORY")
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create consultation_sessions table (1 session per consultation)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultation_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            student_phone TEXT,
            student_email TEXT,
            school_name TEXT,
            grade TEXT,
            score_range TEXT,
            riasec_result TEXT,
            suggested_majors TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP
        )
    """)
    
    # Create consultation_messages table (multiple messages per session)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES consultation_sessions(id)
        )
    """)
    
    # Keep old table for backward compatibility (will be deprecated)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            student_phone TEXT,
            student_email TEXT,
            school_name TEXT,
            grade TEXT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            major_interest TEXT,
            score_range TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create student_info table for storing student information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_phone TEXT NOT NULL,
            student_email TEXT NOT NULL,
            school_name TEXT NOT NULL,
            grade TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create majors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS majors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            description TEXT,
            requirements TEXT,
            career_prospects TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create admission_info table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admission_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            major_code TEXT NOT NULL,
            min_score REAL,
            max_score REAL,
            total_seats INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

def migrate_old_data():
    """Migrate data from old consultation_history to new session-based format"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if there's old data to migrate
        cursor.execute("SELECT COUNT(*) FROM consultation_history")
        old_count = cursor.fetchone()[0]
        
        if old_count == 0:
            conn.close()
            return
        
        logger.info(f"Found {old_count} old records to migrate")
        
        # Get all old records grouped by student
        cursor.execute("""
            SELECT student_name, student_phone, student_email, school_name, grade, score_range,
                   GROUP_CONCAT(question || '|' || answer, '|||') as conversations
            FROM consultation_history 
            GROUP BY student_phone, student_email
        """)
        
        old_records = cursor.fetchall()
        
        for record in old_records:
            student_name, student_phone, student_email, school_name, grade, score_range, conversations = record
            
            # Create new session
            cursor.execute("""
                INSERT INTO consultation_sessions 
                (student_name, student_phone, student_email, school_name, grade, score_range, status)
                VALUES (?, ?, ?, ?, ?, ?, 'completed')
            """, (student_name, student_phone, student_email, school_name, grade, score_range))
            
            session_id = cursor.lastrowid
            
            # Parse and insert messages
            if conversations:
                conversation_pairs = conversations.split('|||')
                for pair in conversation_pairs:
                    if '|' in pair:
                        question, answer = pair.split('|', 1)
                        
                        # Insert user message
                        cursor.execute("""
                            INSERT INTO consultation_messages (session_id, role, content)
                            VALUES (?, 'user', ?)
                        """, (session_id, question))
                        
                        # Insert assistant message
                        cursor.execute("""
                            INSERT INTO consultation_messages (session_id, role, content)
                            VALUES (?, 'assistant', ?)
                        """, (session_id, answer))
        
        conn.commit()
        logger.info(f"Successfully migrated {len(old_records)} student records")
        
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

# Run migration on startup
migrate_old_data()

# Pydantic models
from pydantic import BaseModel

class ConsultationRequest(BaseModel):
    student_name: Optional[str] = None
    student_phone: Optional[str] = None
    student_email: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] = None
    question: str
    score_range: Optional[str] = None
    session_id: Optional[int] = None  # For continuing existing session
    history: Optional[List[dict]] = None  # [{"role": "user"|"assistant", "content": "..."}]

class StudentInfoRequest(BaseModel):
    student_name: str
    student_phone: str
    student_email: str
    school_name: str
    grade: str

class ConsultationResponse(BaseModel):
    answer: str
    session_id: int
    suggested_majors: List[str] = []
    additional_info: str = ""

class MajorInfo(BaseModel):
    name: str
    code: str
    description: str
    requirements: str
    career_prospects: str

# ChatGPT integration
async def get_chatgpt_response(question: str, context: str = "", request_data: dict = None, history: Optional[List[dict]] = None) -> str:
    """Get response from ChatGPT API with intelligent prompt selection"""
    try:
        system_prompt = SYSTEM_PROMPT.format(context=context)
        # Build messages with system + history + current user
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        if history:
            # Filter and normalize roles
            for msg in history:
                role = msg.get("role")
                content = msg.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": question})

        # Gọi ChatGPT API với cấu hình từ prompts.py (SDK v1 hoặc v0 fallback)
        try:
            # SDK v1.x
            try:
                from openai import OpenAI  # type: ignore
                client = OpenAI()
                response = client.chat.completions.create(
                    model=AI_CONFIG["model"],
                    messages=messages,
                    max_tokens=AI_CONFIG["max_tokens"],
                    temperature=AI_CONFIG["temperature"],
                    top_p=AI_CONFIG["top_p"],
                    frequency_penalty=AI_CONFIG["frequency_penalty"],
                    presence_penalty=AI_CONFIG["presence_penalty"]
                )
                return response.choices[0].message.content
            except Exception:
                # SDK v0.x legacy
                legacy_response = openai.ChatCompletion.create(
                    model=AI_CONFIG["model"],
                    messages=messages,
                    max_tokens=AI_CONFIG["max_tokens"],
                    temperature=AI_CONFIG["temperature"],
                    top_p=AI_CONFIG["top_p"],
                    frequency_penalty=AI_CONFIG["frequency_penalty"],
                    presence_penalty=AI_CONFIG["presence_penalty"]
                )
                return legacy_response["choices"][0]["message"]["content"]
        except Exception as call_err:
            raise call_err
        
    except Exception as e:
        logger.error(f"Error calling ChatGPT API: {e}")
        return "Xin lỗi, hiện tại hệ thống đang gặp sự cố. Vui lòng thử lại sau hoặc liên hệ trực tiếp với trường."

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "HUTECH Tư Vấn Tuyển Sinh API", "version": "1.0.0"}

@app.post("/student-info")
async def save_student_info(request: StudentInfoRequest):
    """Lưu thông tin học sinh"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO student_info 
            (student_name, student_phone, student_email, school_name, grade)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.student_name,
            request.student_phone,
            request.student_email,
            request.school_name,
            request.grade
        ))
        conn.commit()
        student_id = cursor.lastrowid
        
        return {"message": "Thông tin học sinh đã được lưu thành công", "student_id": student_id}
        
    except Exception as e:
        logger.error(f"Error saving student info: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống")
    finally:
        if conn:
            conn.close()

@app.post("/consultation", response_model=ConsultationResponse)
async def consultation(request: ConsultationRequest):
    """Tư vấn tuyển sinh"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get or create session
        session_id = request.session_id
        if not session_id:
            # Create new session
            cursor.execute("""
                INSERT INTO consultation_sessions 
                (student_name, student_phone, student_email, school_name, grade, score_range)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                request.student_name,
                request.student_phone,
                request.student_email,
                request.school_name,
                request.grade,
                request.score_range
            ))
            session_id = cursor.lastrowid
        else:
            # Update existing session with latest student info if provided
            if request.student_name or request.score_range:
                cursor.execute("""
                    UPDATE consultation_sessions 
                    SET student_name = COALESCE(?, student_name),
                        student_phone = COALESCE(?, student_phone),
                        student_email = COALESCE(?, student_email),
                        school_name = COALESCE(?, school_name),
                        grade = COALESCE(?, grade),
                        score_range = COALESCE(?, score_range)
                    WHERE id = ?
                """, (
                    request.student_name,
                    request.student_phone,
                    request.student_email,
                    request.school_name,
                    request.grade,
                    request.score_range,
                    session_id
                ))
        
        # Save user message
        cursor.execute("""
            INSERT INTO consultation_messages (session_id, role, content)
            VALUES (?, 'user', ?)
        """, (session_id, request.question))
        
        # Build context from student info
        context = ""
        if request.score_range:
            context += f"Điểm số dự kiến: {request.score_range}. "
        
        # Get ChatGPT response với prompt thông minh (kèm lịch sử)
        answer = await get_chatgpt_response(request.question, context, {}, request.history)
        
        # Check if session should end
        session_ended = False
        if "[SESSION_END]" in answer:
            # Remove the marker from the answer
            answer = answer.replace("[SESSION_END]", "").strip()
            session_ended = True
            
            # Update session status
            cursor.execute("""
                UPDATE consultation_sessions 
                SET status = 'completed', ended_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (session_id,))
        
        # Save AI response
        cursor.execute("""
            INSERT INTO consultation_messages (session_id, role, content)
            VALUES (?, 'assistant', ?)
        """, (session_id, answer))
        
        conn.commit()
        
        # Do not extract or return suggested majors; leave empty
        suggested_majors: List[str] = []
        
        return ConsultationResponse(
            answer=answer,
            session_id=session_id,
            suggested_majors=suggested_majors,
            additional_info=""
        )
        
    except Exception as e:
        logger.error(f"Error in consultation: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Lỗi hệ thống")
    finally:
        if conn:
            conn.close()

@app.get("/majors")
async def get_majors():
    """Lấy danh sách các ngành học"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM majors ORDER BY name")
    majors = cursor.fetchall()
    conn.close()
    
    return [dict(major) for major in majors]

@app.get("/admission-info/{year}")
async def get_admission_info(year: int):
    """Lấy thông tin điểm chuẩn theo năm"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM admission_info 
        WHERE year = ? 
        ORDER BY major_code
    """, (year,))
    info = cursor.fetchall()
    conn.close()
    
    return [dict(item) for item in info]

@app.get("/consultation-history")
async def get_consultation_history(limit: int = 50):
    """Lấy lịch sử tư vấn (legacy format)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM consultation_history 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    history = cursor.fetchall()
    conn.close()
    
    return [dict(item) for item in history]

@app.get("/consultation-sessions")
async def get_consultation_sessions(limit: int = 50):
    """Lấy danh sách các session tư vấn"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM consultation_sessions 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    sessions = cursor.fetchall()
    conn.close()
    
    return [dict(session) for session in sessions]

@app.get("/consultation-sessions/{session_id}/messages")
async def get_session_messages(session_id: int):
    """Lấy tất cả tin nhắn trong một session"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM consultation_messages 
        WHERE session_id = ? 
        ORDER BY timestamp ASC
    """, (session_id,))
    messages = cursor.fetchall()
    conn.close()
    
    return [dict(message) for message in messages]

@app.get("/consultation-sessions/{session_id}")
async def get_session_details(session_id: int):
    """Lấy thông tin chi tiết của một session"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get session info
    cursor.execute("SELECT * FROM consultation_sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    
    if not session:
        conn.close()
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get messages
    cursor.execute("""
        SELECT * FROM consultation_messages 
        WHERE session_id = ? 
        ORDER BY timestamp ASC
    """, (session_id,))
    messages = cursor.fetchall()
    
    conn.close()
    
    return {
        "session": dict(session),
        "messages": [dict(message) for message in messages]
    }

@app.post("/consultation-sessions/{session_id}/end")
async def end_session(session_id: int):
    """Kết thúc session thủ công"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if session exists
    cursor.execute("SELECT * FROM consultation_sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    
    if not session:
        conn.close()
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Update session status
    cursor.execute("""
        UPDATE consultation_sessions 
        SET status = 'completed', ended_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (session_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Session ended successfully", "session_id": session_id}

@app.post("/majors")
async def add_major(major: MajorInfo):
    """Thêm ngành học mới (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO majors (name, code, description, requirements, career_prospects)
        VALUES (?, ?, ?, ?, ?)
    """, (
        major.name,
        major.code,
        major.description,
        major.requirements,
        major.career_prospects
    ))
    conn.commit()
    conn.close()
    
    return {"message": "Ngành học đã được thêm thành công"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
