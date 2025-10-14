"""
Script để khởi tạo dữ liệu mẫu cho hệ thống tư vấn tuyển sinh HUTECH
"""
import sqlite3
import os

def init_sample_data():
    """Khởi tạo dữ liệu mẫu"""
    conn = sqlite3.connect("hutech_consultation.db")
    cursor = conn.cursor()
    
    # Tạo các bảng nếu chưa có
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
    
    # Thêm các ngành học mẫu
    majors_data = [
        {
            "name": "Công nghệ thông tin",
            "code": "CNTT",
            "description": "Ngành học về phát triển phần mềm, hệ thống thông tin, trí tuệ nhân tạo",
            "requirements": "Tốt nghiệp THPT, có kiến thức cơ bản về toán học và tin học",
            "career_prospects": "Lập trình viên, phân tích hệ thống, chuyên gia AI/ML, quản trị mạng"
        },
        {
            "name": "Kỹ thuật phần mềm",
            "code": "KTPM",
            "description": "Chuyên sâu về phát triển phần mềm, quy trình phát triển, quản lý dự án",
            "requirements": "Tốt nghiệp THPT, tư duy logic tốt, yêu thích lập trình",
            "career_prospects": "Software Engineer, Project Manager, System Architect, DevOps Engineer"
        },
        {
            "name": "Khoa học máy tính",
            "code": "KMT",
            "description": "Nghiên cứu về thuật toán, cấu trúc dữ liệu, trí tuệ nhân tạo",
            "requirements": "Tốt nghiệp THPT, giỏi toán học và tư duy logic",
            "career_prospects": "Nhà nghiên cứu AI, Data Scientist, Algorithm Engineer, Research Scientist"
        },
        {
            "name": "Kỹ thuật cơ khí",
            "code": "KTCK",
            "description": "Thiết kế, chế tạo và vận hành máy móc, thiết bị cơ khí",
            "requirements": "Tốt nghiệp THPT, có khả năng tư duy không gian và vật lý",
            "career_prospects": "Kỹ sư cơ khí, thiết kế sản phẩm, quản lý sản xuất, chuyên viên bảo trì"
        },
        {
            "name": "Kỹ thuật điện tử",
            "code": "KTD",
            "description": "Thiết kế và phát triển các hệ thống điện tử, vi mạch",
            "requirements": "Tốt nghiệp THPT, giỏi vật lý và toán học",
            "career_prospects": "Kỹ sư điện tử, thiết kế vi mạch, chuyên viên IoT, kỹ thuật viên điện tử"
        },
        {
            "name": "Quản trị kinh doanh",
            "code": "QTKD",
            "description": "Quản lý doanh nghiệp, marketing, nhân sự, tài chính",
            "requirements": "Tốt nghiệp THPT, có kỹ năng giao tiếp và lãnh đạo",
            "career_prospects": "Quản lý doanh nghiệp, chuyên viên marketing, nhân viên nhân sự, tư vấn kinh doanh"
        },
        {
            "name": "Marketing",
            "code": "MKT",
            "description": "Nghiên cứu thị trường, quảng cáo, xây dựng thương hiệu",
            "requirements": "Tốt nghiệp THPT, có khả năng sáng tạo và giao tiếp",
            "career_prospects": "Chuyên viên marketing, quản lý thương hiệu, chuyên viên quảng cáo, digital marketing"
        },
        {
            "name": "Kế toán",
            "code": "KT",
            "description": "Ghi chép, phân tích và báo cáo tài chính doanh nghiệp",
            "requirements": "Tốt nghiệp THPT, cẩn thận, tỉ mỉ, giỏi toán",
            "career_prospects": "Kế toán viên, kiểm toán viên, chuyên viên tài chính, quản lý tài chính"
        },
        {
            "name": "Tài chính - Ngân hàng",
            "code": "TCNH",
            "description": "Quản lý tài chính, đầu tư, ngân hàng, bảo hiểm",
            "requirements": "Tốt nghiệp THPT, giỏi toán và có khả năng phân tích",
            "career_prospects": "Chuyên viên tài chính, nhân viên ngân hàng, chuyên viên đầu tư, quản lý rủi ro"
        },
        {
            "name": "Ngôn ngữ Anh",
            "code": "NNA",
            "description": "Chuyên sâu về tiếng Anh, văn hóa, văn học và dịch thuật",
            "requirements": "Tốt nghiệp THPT, có nền tảng tiếng Anh tốt",
            "career_prospects": "Biên dịch viên, phiên dịch viên, giáo viên tiếng Anh, hướng dẫn viên du lịch"
        },
        {
            "name": "Du lịch và Lữ hành",
            "code": "DL",
            "description": "Quản lý du lịch, thiết kế tour, marketing du lịch",
            "requirements": "Tốt nghiệp THPT, có kỹ năng giao tiếp tốt, yêu thích du lịch",
            "career_prospects": "Hướng dẫn viên du lịch, quản lý khách sạn, nhân viên lữ hành"
        },
        {
            "name": "Thiết kế đồ họa",
            "code": "TDH",
            "description": "Thiết kế logo, poster, website, ứng dụng di động",
            "requirements": "Tốt nghiệp THPT, có khả năng sáng tạo và thẩm mỹ",
            "career_prospects": "Graphic Designer, UI/UX Designer, Art Director, Freelance Designer"
        },
        {
            "name": "Truyền thông đa phương tiện",
            "code": "TTDPM",
            "description": "Sản xuất nội dung video, audio, website, game",
            "requirements": "Tốt nghiệp THPT, có khả năng sáng tạo và kỹ thuật",
            "career_prospects": "Video Editor, Content Creator, Game Developer, Multimedia Producer"
        },
        {
            "name": "Tâm lý học",
            "code": "TLH",
            "description": "Nghiên cứu hành vi con người, tư vấn tâm lý",
            "requirements": "Tốt nghiệp THPT, có khả năng lắng nghe và thấu hiểu",
            "career_prospects": "Nhà tâm lý học, tư vấn viên, chuyên viên nhân sự, nhà nghiên cứu"
        },
        {
            "name": "Y Dược",
            "code": "YD",
            "description": "Nghiên cứu về y học, dược học, chăm sóc sức khỏe",
            "requirements": "Tốt nghiệp THPT, có kiến thức tốt về sinh học và hóa học",
            "career_prospects": "Bác sĩ, dược sĩ, y tá, kỹ thuật viên y tế"
        }
    ]
    
    for major in majors_data:
        cursor.execute("""
            INSERT OR REPLACE INTO majors (name, code, description, requirements, career_prospects)
            VALUES (?, ?, ?, ?, ?)
        """, (
            major["name"],
            major["code"],
            major["description"],
            major["requirements"],
            major["career_prospects"]
        ))
    
    # Thêm thông tin điểm chuẩn mẫu (năm 2024)
    admission_data = [
        {"year": 2024, "major_code": "CNTT", "min_score": 18.0, "max_score": 28.5, "total_seats": 200},
        {"year": 2024, "major_code": "KTPM", "min_score": 17.5, "max_score": 27.8, "total_seats": 150},
        {"year": 2024, "major_code": "KMT", "min_score": 19.0, "max_score": 29.0, "total_seats": 120},
        {"year": 2024, "major_code": "KTCK", "min_score": 16.5, "max_score": 26.0, "total_seats": 100},
        {"year": 2024, "major_code": "KTD", "min_score": 17.0, "max_score": 26.5, "total_seats": 80},
        {"year": 2024, "major_code": "QTKD", "min_score": 16.0, "max_score": 25.5, "total_seats": 180},
        {"year": 2024, "major_code": "MKT", "min_score": 15.5, "max_score": 24.8, "total_seats": 120},
        {"year": 2024, "major_code": "KT", "min_score": 15.0, "max_score": 24.0, "total_seats": 150},
        {"year": 2024, "major_code": "TCNH", "min_score": 16.5, "max_score": 25.8, "total_seats": 100},
        {"year": 2024, "major_code": "NNA", "min_score": 15.5, "max_score": 24.8, "total_seats": 120},
        {"year": 2024, "major_code": "DL", "min_score": 15.0, "max_score": 23.5, "total_seats": 100},
        {"year": 2024, "major_code": "TDH", "min_score": 16.0, "max_score": 25.0, "total_seats": 80},
        {"year": 2024, "major_code": "TTDPM", "min_score": 15.5, "max_score": 24.5, "total_seats": 60},
        {"year": 2024, "major_code": "TLH", "min_score": 16.5, "max_score": 25.5, "total_seats": 80},
        {"year": 2024, "major_code": "YD", "min_score": 20.0, "max_score": 30.0, "total_seats": 80},
    ]
    
    for admission in admission_data:
        cursor.execute("""
            INSERT OR REPLACE INTO admission_info (year, major_code, min_score, max_score, total_seats)
            VALUES (?, ?, ?, ?, ?)
        """, (
            admission["year"],
            admission["major_code"],
            admission["min_score"],
            admission["max_score"],
            admission["total_seats"]
        ))
    
    conn.commit()
    conn.close()
    print("✅ Dữ liệu mẫu đã được khởi tạo thành công!")

if __name__ == "__main__":
    init_sample_data()
