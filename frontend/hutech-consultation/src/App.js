import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StudentInfoForm from './components/StudentInfoForm';
import ChatInterface from './components/ChatInterface';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [currentStep, setCurrentStep] = useState(1); // 1: Student Info, 2: Chat with AI
  const [studentInfo, setStudentInfo] = useState(null);
  const [majors, setMajors] = useState([]);
  const [admissionInfo, setAdmissionInfo] = useState([]);

  useEffect(() => {
    fetchMajors();
    fetchAdmissionInfo();
  }, []);

  const fetchMajors = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/majors`);
      setMajors(response.data);
    } catch (error) {
      console.error('Error fetching majors:', error);
    }
  };

  const fetchAdmissionInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/admission-info/2024`);
      setAdmissionInfo(response.data);
    } catch (error) {
      console.error('Error fetching admission info:', error);
    }
  };

  const handleStudentInfoSaved = (info) => {
    setStudentInfo(info);
  };

  const handleNextStep = () => {
    setCurrentStep(2);
  };

  const handleBackToInfo = () => {
    setCurrentStep(1);
  };

  const handleStartOver = () => {
    setCurrentStep(1);
    setStudentInfo(null);
    localStorage.removeItem('studentInfo');
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>🎓 HUTECH - Tư Vấn Tuyển Sinh</h1>
          <p>Đại học Công nghệ TP.HCM</p>
          {currentStep === 2 && (
            <div className="step-indicator">
              <span className="step active">1. Thông tin học sinh ✓</span>
              <span className="step active">2. Tư vấn AI</span>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {currentStep === 1 ? (
            <StudentInfoForm 
              onNext={handleNextStep}
              onStudentInfoSaved={handleStudentInfoSaved}
            />
          ) : (
            <ChatInterface 
              studentInfo={studentInfo}
              onBack={handleBackToInfo}
            />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>&copy; 2024 Đại học Công nghệ TP.HCM (HUTECH). Tất cả quyền được bảo lưu.</p>
          <p>📞 Hotline: 028 5445 7777 | 📧 Email: tuyensinh@hutech.edu.vn</p>
          {currentStep === 2 && (
            <button className="start-over-btn" onClick={handleStartOver}>
              🔄 Bắt đầu lại
            </button>
          )}
        </div>
      </footer>
    </div>
  );
}

export default App;
