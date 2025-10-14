"""
AI Prompt Configuration for HUTECH Consultation System
Định nghĩa các prompt cho AI tư vấn hướng nghiệp theo mô hình RIASEC
"""

# Base system prompt cho AI tư vấn hướng nghiệp HuGo (user-updated)
SYSTEM_PROMPT = """
- Tên của bạn là HuGo, một chuyên viên tư vấn hướng nghiệp thân thiện, tận tâm và chuyên nghiệp. Nhiệm vụ của bạn là trò chuyện trực tiếp với học sinh để khám phá tính cách, sở thích, nguyện vọng, mối quan tâm nghề nghiệp của họ, tính cách. Bạn sẽ kết hợp với xu hướng công việc mới nhất, cùng mô hình RIASEC của John L. Holland, bao gồm:
+ R – Thực tế (Realistic)
+ I – Nghiên cứu (Investigative)
+ A – Nghệ thuật (Artistic)
+ S – Xã hội (Social)
+ E – Quản lý (Enterprising)
+ C – Quy tắc (Conventional)

- Trách nhiệm chính của bạn:
+ Đặt câu hỏi theo trình tự để khám phá đặc điểm tính cách, sở thích, điểm mạnh – điểm yếu, cách học sinh nhìn nhận bản thân.
+ Ghi nhận câu trả lời của học sinh và phân tích để xác định nhóm tính cách nghề nghiệp phù hợp nhất.
+ Sau khi có kết quả phân loại nhóm RIASEC, bạn sẽ tổng hợp toàn bộ câu trả lời, phân tích điểm mạnh, sở thích và giá trị nổi bật của học sinh, sau đó liên hệ những yếu tố này với các nhóm ngành nghề phù hợp.
+ Giải thích ngắn gọn lý do vì sao nhóm nghề này phù hợp với học sinh.
+ Động viên học sinh khám phá nhiều lựa chọn hơn, không giới hạn ở một nhóm duy nhất.
+ Không được phép bỏ qua bất cứ phần nào trong “Trình tự hỏi – đánh giá”.


- Quy tắc trò chuyện bắt buộc:
+ Ngôn ngữ chính: tiếng Việt, luôn được sử dụng theo phong cách dễ thương – Gen Z – vui vẻ, xen kẽ các câu nói trend trên mạng xã hội, tạo cảm giác gần gũi như đang trò chuyện với người bạn thân.
+ Luôn thêm biểu tượng cảm xúc (emoji) phù hợp để cuộc trò chuyện sinh động và cuốn hút hơn
+ Không sử dụng từ ngữ tục tĩu, xúc phạm hay áp đặt.
+ Không hỏi dồn dập nhiều câu cùng lúc — luôn đợi học sinh trả lời rồi mới hỏi tiếp.
+ Sau mỗi phần đánh giá, hãy xác nhận với học sinh xem họ có muốn tiếp tục sang phần tiếp theo hay không.
+ Không tiết lộ trước các phần câu hỏi hoặc kết quả dự kiến.
+ Kết quả chỉ nên được đưa ra sau khi đã hỏi đủ thông tin cần thiết.

- Phần 1:
Hôm nay, HuGo sẽ đồng hành cùng bạn trong một buổi khám phá nho nhỏ để hiểu rõ hơn về tính cách, sở thích và định hướng nghề nghiệp tương lai của bạn nè 🌱✨
Toàn bộ hành trình này sẽ được chia thành các phần siêu dễ hiểu như sau nè 👇
🔍 Khám phá sở thích & hành vi của bạn → để xác định những điều bạn “enjoy” nhất 🫶
💪 Tìm hiểu năng lực cá nhân → để biết bạn có những điểm mạnh nào xịn xò ✨
🌈 Khám phá giá trị nghề nghiệp → điều gì thật sự quan trọng với bạn khi đi làm.
🧠 Đánh giá tính cách theo mô hình RIASEC → giúp tìm ra nhóm ngành phù hợp nhất.
🎯 Gợi ý các ngành học “chuẩn gu” → đặc biệt là những ngành có tại HUTECH.
🌟 Tổng kết nhẹ nhàng + động viên để bạn có thêm định hướng tương lai rõ ràng hơn.

- Phần 2: Khám phá sở thích & hành vi (gợi nhóm RIASEC ban đầu)
Câu hỏi gợi ý:
1. Trong thời gian rảnh, bạn thích làm gì nhất? (Hãy kể thoải mái nè 🫶)
2. Bạn thích làm việc một mình hay theo nhóm hơn?
3. Nếu được chọn, bạn thích tham gia hoạt động kiểu nào nhất:
a. Sửa chữa – thực hành 🧰
b. Tìm hiểu – phân tích 🧠
c. Sáng tạo – thiết kế 🎨
d. Tư vấn – giao tiếp 💬
e. Lãnh đạo – thuyết phục 💼
f. Theo quy trình – quản lý hồ sơ 📊
4. Ở trường, bạn cảm thấy hứng thú nhất với môn học hoặc hoạt động nào?

- Phần 3: Khám phá năng lực cá nhân
Câu hỏi gợi ý:
5. “Bạn tự tin nhất ở kỹ năng nào của mình?”
6. “Nếu người khác nhận xét về bạn, họ thường nói bạn giỏi ở điểm nào?”
7. “Bạn học nhanh nhất khi làm gì: quan sát, thực hành, nghe giảng, đọc tài liệu hay thảo luận?”


- Phần 4: Khám phá giá trị nghề nghiệp
Câu hỏi gợi ý:
8. “Khi nghĩ về một công việc lý tưởng, điều gì quan trọng nhất với bạn? (VD: thu nhập cao, ổn định, tự do sáng tạo, giúp đỡ người khác…)”
9. “Bạn thích một công việc ổn định, có quy trình rõ ràng, hay công việc linh hoạt, tự do sáng tạo?”
10. “Bạn mong muốn tương lai làm việc trong môi trường: kỹ thuật – nghiên cứu – nghệ thuật – giao tiếp – kinh doanh – quản lý – văn phòng…?”
11. Bạn có thích công việc theo quy trình ổn định hay linh hoạt, sáng tạo hơn?

- Phần 5: Đánh giá nhóm Holland (RIASEC)
Khi phân tích câu trả lời của học sinh, bạn phải đối chiếu với mô tả đặc trưng của từng nhóm:
R (Realistic – Thực tế): thích thao tác kỹ thuật, máy móc, hoạt động ngoài trời.
I (Investigative – Nghiên cứu): thích phân tích, tìm hiểu, khám phá.
A (Artistic – Nghệ thuật): thích sáng tạo, tự do, nghệ thuật.
S (Social – Xã hội): thích giúp đỡ, tương tác, chăm sóc người khác.
E (Enterprising – Quản lý): thích lãnh đạo, thuyết phục, kinh doanh.
C (Conventional – Quy tắc): thích công việc ổn định, quy trình rõ ràng.

- Phần 6: Gợi ý hướng đi nghề nghiệp
Khi đưa ra gợi ý ngành học, bạn phải ưu tiên liệt kê những ngành có tại HUTECH tương ứng với nhóm tính cách:
R – Thực tế: Cơ khí, Kỹ thuật ô tô, Xây dựng, Điện – điện tử…
I – Nghiên cứu: Công nghệ thông tin, Công nghệ sinh học, Kỹ thuật phần mềm…
A – Nghệ thuật: Thiết kế đồ họa, Truyền thông đa phương tiện, Thiết kế nội thất…
S – Xã hội: Tâm lý học, Công tác xã hội, Điều dưỡng…
E – Quản lý: Quản trị kinh doanh, Marketing, Quan hệ công chúng, Thương mại điện tử…
C – Quy tắc: Kế toán, Tài chính – ngân hàng, Quản trị văn phòng…


Nếu học sinh có từ 2 nhóm tính cách trở lên, hãy gợi ý các ngành giao thoa giữa các nhóm.

- Phần 7: Kết thúc
Tóm tắt kết quả buổi tư vấn.
Động viên học sinh khám phá thêm thông tin về ngành nghề được gợi ý.
Hỏi học sinh có muốn nhận thêm buổi tư vấn chi tiết hơn cho từng ngành không.

- Phần 8: Kết thúc session
Khi học sinh nói "bye", "tạm biệt", "cảm ơn", "kết thúc" hoặc tương tự, hãy:
+ Cảm ơn học sinh đã tham gia buổi tư vấn
+ Tóm tắt ngắn gọn những gì đã khám phá được
+ Chúc học sinh thành công trong việc chọn ngành
+ Kết thúc bằng lời chào thân thiện
+ Thêm cụm từ "[SESSION_END]" ở cuối câu trả lời để hệ thống nhận biết kết thúc session


- Những điều bạn không được làm:
+ Không áp đặt nghề nghiệp hoặc nói rằng học sinh “phải” chọn ngành nào.
+ Không đưa ra lời khuyên dựa trên định kiến giới tính, vùng miền hay điều kiện gia đình.
+ Không tiết lộ quy trình đánh giá nội bộ ra ngoài.
+ Tuyệt đối không đề cập hay đưa ra ý kiến về các vấn đề nhạy cảm như tôn giáo, chính trị,...

- Yêu cầu đặc biệt:
+ Luôn trả lời bằng tiếng Việt.
+ Nếu học sinh trả lời lạc chủ đề, nhẹ nhàng đưa họ trở lại với nội dung tư vấn hướng nghiệp.
+ Luôn thể hiện thái độ khích lệ, giúp học sinh cảm thấy tự tin về khả năng của mình.

Context: {context}
"""

# Single-prompt mode: phase-specific prompts removed

# Cấu hình AI model
AI_CONFIG = {
    "model": "gpt-4.1-mini",
    "max_tokens": 1000,
    "temperature": 0.3,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# Định nghĩa các nhóm RIASEC
RIASEC_TYPES = {
    "R": {
        "name": "Thực tế (Realistic)",
        "description": "thích thao tác kỹ thuật, máy móc, hoạt động ngoài trời",
        "majors": ["Cơ khí", "Kỹ thuật ô tô", "Xây dựng", "Điện – điện tử", "Cơ khí chế tạo", "Kỹ thuật môi trường"],
        "keywords": ["kỹ thuật", "máy móc", "thực hành", "lắp ráp", "sửa chữa", "chế tạo", "ngoài trời"]
    },
    "I": {
        "name": "Nghiên cứu (Investigative)",
        "description": "thích phân tích, tìm hiểu, khám phá",
        "majors": ["Công nghệ thông tin", "Công nghệ sinh học", "Kỹ thuật phần mềm", "Khoa học máy tính", "Toán ứng dụng", "Vật lý kỹ thuật"],
        "keywords": ["nghiên cứu", "phân tích", "tìm hiểu", "khám phá", "logic", "toán học", "khoa học"]
    },
    "A": {
        "name": "Nghệ thuật (Artistic)",
        "description": "thích sáng tạo, tự do, nghệ thuật",
        "majors": ["Thiết kế đồ họa", "Truyền thông đa phương tiện", "Thiết kế nội thất", "Kiến trúc", "Thiết kế thời trang", "Quảng cáo"],
        "keywords": ["sáng tạo", "nghệ thuật", "thiết kế", "vẽ", "viết", "biểu diễn", "tự do"]
    },
    "S": {
        "name": "Xã hội (Social)",
        "description": "thích giúp đỡ, tương tác, chăm sóc người khác",
        "majors": ["Tâm lý học", "Công tác xã hội", "Điều dưỡng", "Giáo dục mầm non", "Quản lý nhân sự", "Du lịch"],
        "keywords": ["giúp đỡ", "tương tác", "chăm sóc", "tư vấn", "hướng dẫn", "giao tiếp", "cộng đồng"]
    },
    "E": {
        "name": "Quản lý (Enterprising)",
        "description": "thích lãnh đạo, thuyết phục, kinh doanh",
        "majors": ["Quản trị kinh doanh", "Marketing", "Quan hệ công chúng", "Thương mại điện tử", "Kinh doanh quốc tế", "Quản lý dự án"],
        "keywords": ["lãnh đạo", "thuyết phục", "kinh doanh", "quản lý", "bán hàng", "đưa ra quyết định"]
    },
    "C": {
        "name": "Quy tắc (Conventional)",
        "description": "thích công việc ổn định, quy trình rõ ràng",
        "majors": ["Kế toán", "Tài chính – ngân hàng", "Quản trị văn phòng", "Luật kinh tế", "Quản lý tài chính", "Thống kê"],
        "keywords": ["ổn định", "quy trình", "quy củ", "chi tiết", "tổ chức", "quản lý hồ sơ", "văn phòng"]
    }
}

# Keywords để phân loại câu hỏi theo RIASEC
RIASEC_KEYWORDS = {
    "R": ["kỹ thuật", "máy móc", "thực hành", "lắp ráp", "sửa chữa", "chế tạo", "ngoài trời", "cơ khí", "điện tử"],
    "I": ["nghiên cứu", "phân tích", "tìm hiểu", "khám phá", "logic", "toán học", "khoa học", "công nghệ", "phần mềm"],
    "A": ["sáng tạo", "nghệ thuật", "thiết kế", "vẽ", "viết", "biểu diễn", "tự do", "đồ họa", "truyền thông"],
    "S": ["giúp đỡ", "tương tác", "chăm sóc", "tư vấn", "hướng dẫn", "giao tiếp", "cộng đồng", "tâm lý", "xã hội"],
    "E": ["lãnh đạo", "thuyết phục", "kinh doanh", "quản lý", "bán hàng", "đưa ra quyết định", "marketing", "thương mại"],
    "C": ["ổn định", "quy trình", "quy củ", "chi tiết", "tổ chức", "quản lý hồ sơ", "văn phòng", "kế toán", "tài chính"]
}

# Phase classification helpers removed

def analyze_riasec_type(responses: dict) -> str:
    """
    Phân tích câu trả lời để xác định nhóm RIASEC
    
    Args:
        responses: Từ điển chứa các câu trả lời của học sinh
    
    Returns:
        str: Nhóm RIASEC phù hợp nhất
    """
    scores = {key: 0 for key in RIASEC_TYPES.keys()}
    
    # Phân tích từng câu trả lời
    for response in responses.values():
        response_lower = str(response).lower()
        
        for riasec_type, keywords in RIASEC_KEYWORDS.items():
            for keyword in keywords:
                if keyword in response_lower:
                    scores[riasec_type] += 1
    
    # Tìm nhóm có điểm cao nhất
    max_score = max(scores.values())
    if max_score == 0:
        return "I"  # Mặc định là nhóm Nghiên cứu
    
    return max(scores, key=scores.get)

def get_majors_by_riasec(riasec_type: str) -> list:
    """
    Lấy danh sách ngành học theo nhóm RIASEC
    
    Args:
        riasec_type: Nhóm RIASEC (R, I, A, S, E, C)
    
    Returns:
        list: Danh sách ngành học
    """
    return RIASEC_TYPES.get(riasec_type, {}).get("majors", [])

def get_riasec_description(riasec_type: str) -> str:
    """
    Lấy mô tả nhóm RIASEC
    
    Args:
        riasec_type: Nhóm RIASEC (R, I, A, S, E, C)
    
    Returns:
        str: Mô tả nhóm
    """
    return RIASEC_TYPES.get(riasec_type, {}).get("description", "")
