import React, { useState } from 'react';
import axios from 'axios';
import './StudentInfoForm.css';

const API_BASE_URL = 'http://localhost:8000';

const StudentInfoForm = ({ onNext, onStudentInfoSaved }) => {
  const [formData, setFormData] = useState({
    student_name: '',
    student_phone: '',
    student_email: '',
    school_name: '',
    grade: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/student-info`, formData);
      console.log('Student info saved:', response.data);
      
      // Lưu thông tin học sinh vào localStorage để sử dụng ở bước tiếp theo
      localStorage.setItem('studentInfo', JSON.stringify(formData));
      
      // Gọi callback để chuyển sang bước tiếp theo
      onStudentInfoSaved(formData);
      onNext();
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Có lỗi xảy ra, vui lòng thử lại');
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = () => {
    return formData.student_name.trim() && 
           formData.student_phone.trim() && 
           formData.student_email.trim() && 
           formData.school_name.trim() && 
           formData.grade;
  };

  return (
    <div className="student-info-form">
      <div className="form-header">
        <h2>📝 Thông tin học sinh</h2>
        <p>Vui lòng điền đầy đủ thông tin để chúng tôi có thể tư vấn tốt nhất cho bạn</p>
      </div>

      <form onSubmit={handleSubmit} className="info-form">
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Họ và tên *</label>
            <input
              type="text"
              name="student_name"
              value={formData.student_name}
              onChange={handleInputChange}
              className="form-input"
              placeholder="Nhập họ và tên của bạn"
              required
            />
          </div>
          <div className="form-group">
            <label className="form-label">Số điện thoại *</label>
            <input
              type="tel"
              name="student_phone"
              value={formData.student_phone}
              onChange={handleInputChange}
              className="form-input"
              placeholder="Nhập số điện thoại"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Email *</label>
          <input
            type="email"
            name="student_email"
            value={formData.student_email}
            onChange={handleInputChange}
            className="form-input"
            placeholder="Nhập email của bạn"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Trường học *</label>
            <input
              type="text"
              name="school_name"
              value={formData.school_name}
              onChange={handleInputChange}
              className="form-input"
              placeholder="Nhập tên trường THPT của bạn"
              required
            />
          </div>
          <div className="form-group">
            <label className="form-label">Lớp *</label>
            <select
              name="grade"
              value={formData.grade}
              onChange={handleInputChange}
              className="form-input"
              required
            >
              <option value="">Chọn lớp</option>
              <option value="10">Lớp 10</option>
              <option value="11">Lớp 11</option>
              <option value="12">Lớp 12</option>
            </select>
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            ❌ {error}
          </div>
        )}

        <div className="form-actions">
          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={loading || !isFormValid()}
          >
            {loading ? 'Đang lưu...' : 'Tiếp tục'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default StudentInfoForm;
