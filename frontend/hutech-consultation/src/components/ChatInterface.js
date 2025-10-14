import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

const API_BASE_URL = 'http://localhost:8000';

const ChatInterface = ({ studentInfo, onBack }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [sessionEnded, setSessionEnded] = useState(false);
  const [restarting, setRestarting] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Khởi tạo cuộc trò chuyện với AI
    const initializeChat = async () => {
      const welcomeMessage = {
        id: Date.now(),
        type: 'ai',
        content: `Hiiii ${studentInfo.student_name} iuuu 🫶✨
                  Mình là HuGo – chuyên viên tư vấn hướng nghiệp siêu dễ thương của HUTECH nè 💼🎓
                  Hôm nay mình sẽ cùng bạn khám phá tính cách nghề nghiệp để tìm ra ngành học “chuẩn gu” nhất cho bạn đóaa~ 🌟
                  Đừng lo nè, đây không phải bài kiểm tra căng thẳng đâu 🤭
                  Chỉ là buổi tám chuyện nhẹ nhàng để hiểu nhau hơn thuii~
                  Bạn sẵn sàng bắt đầu chưa nà? 🌱💬`,
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
    };

    initializeChat();
  }, [studentInfo]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);
    setError(null);

    try {
      // Map local messages to backend history format
      const history = messages.map(m => ({
        role: m.type === 'ai' ? 'assistant' : 'user',
        content: m.content
      }));
      const response = await axios.post(`${API_BASE_URL}/consultation`, {
        student_name: studentInfo.student_name,
        student_phone: studentInfo.student_phone,
        student_email: studentInfo.student_email,
        school_name: studentInfo.school_name,
        grade: studentInfo.grade,
        question: inputMessage.trim(),
        score_range: '',
        session_id: sessionId,
        history
      });

      // Update session ID if this is the first message
      if (!sessionId) {
        setSessionId(response.data.session_id);
      }

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.data.answer,
        suggested_majors: response.data.suggested_majors,
        additional_info: response.data.additional_info,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);

      // Check if session ended (AI response contains [SESSION_END])
      if (response.data.answer.includes('[SESSION_END]')) {
        setSessionEnded(true);
      }

    } catch (error) {
      setError(error.response?.data?.detail || 'Có lỗi xảy ra, vui lòng thử lại');
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Xin lỗi, hiện tại hệ thống đang gặp sự cố. Vui lòng thử lại sau hoặc liên hệ trực tiếp với trường qua hotline: 028 5445 7777',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleEndSession = async () => {
    if (!sessionId) return;
    
    try {
      await axios.post(`${API_BASE_URL}/consultation-sessions/${sessionId}/end`);
      setSessionEnded(true);
    } catch (error) {
      setError('Không thể kết thúc session');
    }
  };

  const handleRestartChat = async () => {
    setRestarting(true);
    
    try {
      // End current session if exists
      if (sessionId) {
        await axios.post(`${API_BASE_URL}/consultation-sessions/${sessionId}/end`);
      }
    } catch (error) {
      console.log('Session already ended or not found:', error);
      // Continue with restart even if ending session fails
    }
    
    // Reset all chat state
    setMessages([]);
    setInputMessage('');
    setLoading(false);
    setError(null);
    setSessionId(null);
    setSessionEnded(false);
    
    // Re-initialize chat with welcome message
    const welcomeMessage = {
      id: Date.now(),
      type: 'ai',
      content: `Hiiii ${studentInfo.student_name} iuuu 🫶✨
                Mình là HuGo – chuyên viên tư vấn hướng nghiệp siêu dễ thương của HUTECH nè 💼🎓
                Hôm nay mình sẽ cùng bạn khám phá tính cách nghề nghiệp để tìm ra ngành học "chuẩn gu" nhất cho bạn đóaa~ 🌟
                Đừng lo nè, đây không phải bài kiểm tra căng thẳng đâu 🤭
                Chỉ là buổi tám chuyện nhẹ nhàng để hiểu nhau hơn thuii~
                Bạn sẵn sàng bắt đầu chưa nà? 🌱💬`,
      timestamp: new Date().toISOString()
    };
    setMessages([welcomeMessage]);
    setRestarting(false);
  };

  const formatMessage = (content) => {
    return content.split('\n').map((line, index) => (
      <span key={index}>
        {line}
        {index < content.split('\n').length - 1 && <br />}
      </span>
    ));
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-left">
          <button className="back-btn" onClick={onBack}>
            ← Quay lại
          </button>
        </div>
        <div className="chat-title">
          <h3>💬 Tư vấn với HuGo AI</h3>
          <p>Học sinh: {studentInfo.student_name} - Lớp {studentInfo.grade}</p>
        </div>
        <div className="header-right">
          <button 
            className="restart-btn" 
            onClick={handleRestartChat} 
            title="Bắt đầu lại cuộc trò chuyện"
            disabled={restarting}
          >
            {restarting ? '⏳' : '🔄'}
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-content">
              {formatMessage(message.content)}
              
              {/* Removed suggested majors section */}
              
              {message.additional_info && (
                <div className="additional-info">
                  <h4>ℹ️ Thông tin bổ sung:</h4>
                  <p>{message.additional_info}</p>
                </div>
              )}
            </div>
            <div className="message-time">
              {new Date(message.timestamp).toLocaleTimeString('vi-VN', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message ai">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span>HuGo đang suy nghĩ...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {!sessionEnded ? (
        <form onSubmit={handleSendMessage} className="chat-input-form">
          <div className="input-group">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Nhập câu hỏi của bạn..."
              className="chat-input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="send-btn"
              disabled={loading || !inputMessage.trim()}
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
          <div className="session-controls">
            <button 
              type="button" 
              className="end-session-btn"
              onClick={handleEndSession}
              disabled={loading}
            >
              🏁 Kết thúc tư vấn
            </button>
          </div>
        </form>
      ) : (
        <div className="session-ended">
          <div className="ended-message">
            <h3>✅ Buổi tư vấn đã kết thúc</h3>
            <p>Cảm ơn bạn đã tham gia tư vấn hướng nghiệp với HuGo!</p>
            <button className="back-btn" onClick={onBack}>
              ← Quay lại trang chủ
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
