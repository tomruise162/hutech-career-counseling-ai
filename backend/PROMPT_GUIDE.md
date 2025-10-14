# 🤖 AI Prompt Management Guide - HuNext Career Counseling

## 📋 Tổng quan

Hệ thống quản lý prompt AI cho HUTECH Tư vấn Hướng nghiệp được thiết kế để:
- **Tư vấn hướng nghiệp** dựa trên mô hình RIASEC của John L. Holland
- **Khám phá tính cách** và sở thích nghề nghiệp của học sinh
- **Phân loại nhóm tính cách** và gợi ý ngành học phù hợp
- **Quy trình tư vấn** có cấu trúc 7 phần rõ ràng

## 📁 Cấu trúc file

```
backend/
├── prompts.py              # Định nghĩa prompts và logic xử lý RIASEC
├── prompt_config.json      # Cấu hình prompts và AI model
├── PROMPT_GUIDE.md         # Hướng dẫn này
└── main.py                 # Sử dụng prompts trong API
```

## 🎯 Mô hình RIASEC

### Các nhóm tính cách nghề nghiệp:

**R - Thực tế (Realistic)**
- Đặc điểm: thích thao tác kỹ thuật, máy móc, hoạt động ngoài trời
- Ngành học: Cơ khí, Kỹ thuật ô tô, Xây dựng, Điện – điện tử
- Keywords: kỹ thuật, máy móc, thực hành, lắp ráp, sửa chữa

**I - Nghiên cứu (Investigative)**
- Đặc điểm: thích phân tích, tìm hiểu, khám phá
- Ngành học: Công nghệ thông tin, Công nghệ sinh học, Kỹ thuật phần mềm
- Keywords: nghiên cứu, phân tích, tìm hiểu, khám phá, logic

**A - Nghệ thuật (Artistic)**
- Đặc điểm: thích sáng tạo, tự do, nghệ thuật
- Ngành học: Thiết kế đồ họa, Truyền thông đa phương tiện, Thiết kế nội thất
- Keywords: sáng tạo, nghệ thuật, thiết kế, vẽ, viết, biểu diễn

**S - Xã hội (Social)**
- Đặc điểm: thích giúp đỡ, tương tác, chăm sóc người khác
- Ngành học: Tâm lý học, Công tác xã hội, Điều dưỡng
- Keywords: giúp đỡ, tương tác, chăm sóc, tư vấn, hướng dẫn

**E - Quản lý (Enterprising)**
- Đặc điểm: thích lãnh đạo, thuyết phục, kinh doanh
- Ngành học: Quản trị kinh doanh, Marketing, Quan hệ công chúng
- Keywords: lãnh đạo, thuyết phục, kinh doanh, quản lý, bán hàng

**C - Quy tắc (Conventional)**
- Đặc điểm: thích công việc ổn định, quy trình rõ ràng
- Ngành học: Kế toán, Tài chính – ngân hàng, Quản trị văn phòng
- Keywords: ổn định, quy trình, quy củ, chi tiết, tổ chức

## 🔧 Quy trình tư vấn 7 phần

### 1. Phần mở đầu (Opening)
**Mục đích**: Giới thiệu HuNext, tạo cảm giác thoải mái
**Câu hỏi gợi ý**:
- "Chào bạn 👋 Mình là HuNext, hôm nay mình sẽ giúp bạn khám phá tính cách nghề nghiệp để tìm ra những ngành học phù hợp 🎯"
- "Bạn có sẵn định hướng ngành học hoặc nghề nghiệp nào chưa?"

### 2. Khám phá sở thích & hành vi (Interest Exploration)
**Mục đích**: Gợi nhóm RIASEC ban đầu
**Câu hỏi gợi ý**:
- "Trong thời gian rảnh, bạn thường thích làm gì nhất?"
- "Bạn thích làm việc một mình hay theo nhóm hơn?"
- "Bạn cảm thấy hứng thú nhất với môn học nào ở trường?"

### 3. Khám phá năng lực cá nhân (Personal Ability)
**Mục đích**: Hiểu điểm mạnh và cách học tập
**Câu hỏi gợi ý**:
- "Bạn tự tin nhất ở kỹ năng nào của mình?"
- "Bạn học nhanh nhất khi làm gì: quan sát, thực hành, nghe giảng, đọc tài liệu hay thảo luận?"

### 4. Khám phá giá trị nghề nghiệp (Career Values)
**Mục đích**: Hiểu điều quan trọng trong công việc
**Câu hỏi gợi ý**:
- "Khi nghĩ về một công việc lý tưởng, điều gì quan trọng nhất với bạn?"
- "Bạn thích một công việc ổn định, có quy trình rõ ràng, hay công việc linh hoạt, tự do sáng tạo?"

### 5. Đánh giá nhóm Holland (RIASEC Assessment)
**Mục đích**: Xác nhận nhóm tính cách cụ thể
**Câu hỏi gợi ý**:
- "Bạn có thích làm những việc mang tính kỹ thuật hoặc thực hành không?" → nhóm R
- "Bạn có thích tìm hiểu, phân tích dữ liệu hoặc hiện tượng tự nhiên không?" → nhóm I
- "Bạn có thích sáng tạo, vẽ, viết, thiết kế không?" → nhóm A

### 6. Gợi ý hướng đi nghề nghiệp (Career Guidance)
**Mục đích**: Đưa ra gợi ý ngành học cụ thể tại HUTECH
**Nội dung**:
- Liệt kê ngành học phù hợp với nhóm RIASEC
- Giải thích lý do phù hợp
- Gợi ý ngành giao thoa nếu có nhiều nhóm

### 7. Kết thúc (Closing)
**Mục đích**: Tóm tắt và động viên
**Nội dung**:
- Tóm tắt kết quả buổi tư vấn
- Động viên khám phá thêm thông tin
- Hỏi về tư vấn chi tiết hơn

## 🔄 Cách sử dụng

### 1. Prompt chính (System Prompt)

**Vị trí**: `prompts.py` - `SYSTEM_PROMPT`

```python
SYSTEM_PROMPT = """
Tên của bạn là HuNext, một chuyên viên tư vấn hướng nghiệp thân thiện, tận tâm và chuyên nghiệp.
Nhiệm vụ của bạn là trò chuyện trực tiếp với học sinh để khám phá tính cách, sở thích nghề nghiệp của họ...
"""
```

### 2. Prompt theo từng phần

**Vị trí**: `prompts.py` - Các biến như `OPENING_PROMPT`, `INTEREST_EXPLORATION_PROMPT`

```python
OPENING_PROMPT = """
🧭 Ví dụ cách bắt đầu buổi tư vấn:
"Chào bạn 👋 Mình là HuNext, hôm nay mình sẽ giúp bạn khám phá tính cách nghề nghiệp...
"""
```

### 3. Phân tích RIASEC

```python
def analyze_riasec_type(responses: dict) -> str:
    """
    Phân tích câu trả lời để xác định nhóm RIASEC
    """
    scores = {key: 0 for key in RIASEC_TYPES.keys()}
    
    for response in responses.values():
        response_lower = str(response).lower()
        
        for riasec_type, keywords in RIASEC_KEYWORDS.items():
            for keyword in keywords:
                if keyword in response_lower:
                    scores[riasec_type] += 1
    
    return max(scores, key=scores.get)
```

## 🎯 Phân loại câu hỏi

### Keywords để phân loại

**Vị trí**: `prompts.py` - `QUESTION_KEYWORDS`

```python
QUESTION_KEYWORDS = {
    "opening": ["chào", "bắt đầu", "giới thiệu", "mục tiêu", "định hướng"],
    "interest_exploration": ["sở thích", "thời gian rảnh", "hoạt động", "môn học"],
    "personal_ability": ["kỹ năng", "điểm mạnh", "giỏi", "học nhanh", "tự tin"],
    "career_values": ["công việc lý tưởng", "quan trọng", "môi trường", "tương lai"],
    "riasec_assessment": ["kỹ thuật", "nghiên cứu", "nghệ thuật", "xã hội", "quản lý", "quy tắc"],
    "career_guidance": ["ngành học", "nghề nghiệp", "gợi ý", "phù hợp", "hướng đi"],
    "closing": ["kết thúc", "tóm tắt", "tư vấn chi tiết", "thông tin thêm"]
}
```

## 🔄 Cách thêm prompt mới

### 1. Thêm prompt template

Trong `prompts.py`:
```python
NEW_PHASE_PROMPT = """
🔹 Phần X: Tên phần mới

Mục đích: Mô tả mục đích của phần này
Câu hỏi gợi ý:
"Câu hỏi 1"
"Câu hỏi 2"
...
"""
```

### 2. Thêm keywords phân loại

```python
QUESTION_KEYWORDS = {
    # ... existing keywords
    "new_phase": ["keyword1", "keyword2", "keyword3"]
}
```

### 3. Cập nhật function get_prompt_by_type

```python
def get_prompt_by_type(question_type: str, **kwargs) -> str:
    prompt_templates = {
        # ... existing templates
        "new_phase": NEW_PHASE_PROMPT
    }
    
    template = prompt_templates.get(question_type, SYSTEM_PROMPT)
    return template.format(**kwargs)
```

## ⚙️ Tùy chỉnh cấu hình

### 1. Thay đổi AI model

Trong `prompts.py`:
```python
AI_CONFIG = {
    "model": "gpt-4",  # Thay đổi model
    "max_tokens": 1500,  # Tăng token limit
    "temperature": 0.5,  # Giảm randomness
    # ...
}
```

### 2. Thay đổi communication style

Trong `SYSTEM_PROMPT`:
```python
## COMMUNICATION STYLE:
- **Thân thiện, gần gũi** như nói chuyện với bạn bè
- **Sử dụng emoji** để cuộc trò chuyện nhẹ nhàng
- **Không áp đặt** hay sử dụng từ ngữ xúc phạm
```

### 3. Thêm ngành học mới

Trong `RIASEC_TYPES`:
```python
"R": {
    "name": "Thực tế (Realistic)",
    "majors": ["Cơ khí", "Kỹ thuật ô tô", "Ngành mới"],  # Thêm ngành
    "keywords": ["kỹ thuật", "máy móc", "từ khóa mới"]  # Thêm keyword
}
```

## 🧪 Testing prompts

### 1. Test prompt riêng lẻ

```python
# Test trong Python shell
from prompts import get_prompt_by_type, analyze_riasec_type

# Test phân loại
question_type = classify_question("Tôi muốn khám phá tính cách nghề nghiệp")
print(f"Question type: {question_type}")

# Test phân tích RIASEC
responses = {
    "interest": "Tôi thích lập trình và phân tích dữ liệu",
    "ability": "Tôi giỏi toán và logic"
}
riasec_type = analyze_riasec_type(responses)
print(f"RIASEC type: {riasec_type}")
```

### 2. Test với API

```bash
# Test API endpoint
curl -X POST "http://localhost:8000/consultation" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Tôi muốn khám phá tính cách nghề nghiệp",
    "current_phase": "opening"
  }'
```

## 📊 Monitoring và Debug

### 1. Log prompts

Trong `main.py`, thêm logging:
```python
import logging
logger = logging.getLogger(__name__)

# Trong function get_chatgpt_response
logger.info(f"Question type: {question_type}")
logger.info(f"RIASEC analysis: {riasec_type}")
logger.info(f"System prompt: {system_prompt[:200]}...")
```

### 2. Debug RIASEC analysis

```python
def debug_riasec_analysis(responses: dict):
    scores = {key: 0 for key in RIASEC_TYPES.keys()}
    matches = {}
    
    for response in responses.values():
        response_lower = str(response).lower()
        
        for riasec_type, keywords in RIASEC_KEYWORDS.items():
            matches[riasec_type] = [kw for kw in keywords if kw in response_lower]
            scores[riasec_type] += len(matches[riasec_type])
    
    return {"scores": scores, "matches": matches}
```

## 🔒 Best Practices

### 1. Prompt Design
- **Thân thiện**: Sử dụng tone gần gũi như bạn bè
- **Có cấu trúc**: Theo đúng 7 phần quy trình
- **Không áp đặt**: Để học sinh tự khám phá
- **Sử dụng emoji**: Tạo cảm giác nhẹ nhàng

### 2. RIASEC Analysis
- **Phân tích từ khóa**: Dựa trên keywords đã định nghĩa
- **Xem xét ngữ cảnh**: Không chỉ dựa vào từ khóa đơn lẻ
- **Đa nhóm**: Có thể có nhiều nhóm phù hợp
- **Giải thích**: Luôn giải thích lý do phân loại

### 3. Security
- **Không hardcode** API keys trong prompts
- **Validate input** trước khi gửi đến AI
- **Log sensitive data** một cách cẩn thận

### 4. Performance
- **Cache prompts** nếu có thể
- **Optimize token usage** với max_tokens phù hợp
- **Monitor API costs** và usage

## 🚀 Advanced Features

### 1. Dynamic prompts

```python
def get_dynamic_prompt(question_type: str, user_context: dict) -> str:
    base_prompt = get_prompt_by_type(question_type, **user_context)
    
    # Thêm thông tin động
    if user_context.get("is_first_time"):
        base_prompt += "\n\nLưu ý: Đây là lần đầu học sinh sử dụng, cần hướng dẫn chi tiết hơn."
    
    return base_prompt
```

### 2. Multi-phase tracking

```python
def track_consultation_phase(user_id: str, current_phase: str, responses: dict):
    """Theo dõi tiến trình tư vấn của học sinh"""
    consultation_data = {
        "user_id": user_id,
        "current_phase": current_phase,
        "responses": responses,
        "riasec_scores": analyze_riasec_type(responses),
        "timestamp": datetime.now()
    }
    
    # Lưu vào database hoặc cache
    save_consultation_data(consultation_data)
```

### 3. A/B Testing

```python
PROMPT_VARIANTS = {
    "v1": SYSTEM_PROMPT,
    "v2": SYSTEM_PROMPT_V2,  # Version với tone khác
    "v3": SYSTEM_PROMPT_V3   # Version với câu hỏi khác
}

def get_prompt_variant(user_id: str) -> str:
    # Simple hash-based selection
    variant = hash(user_id) % len(PROMPT_VARIANTS)
    return PROMPT_VARIANTS[f"v{variant + 1}"]
```

---

**Lưu ý**: Luôn test prompts kỹ lưỡng trước khi deploy lên production! Đặc biệt chú ý đến việc phân tích RIASEC chính xác và gợi ý ngành học phù hợp.