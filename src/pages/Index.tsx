import { useState } from 'react';
import LoginPage from '@/components/LoginPage';
import AdminDashboard from '@/components/AdminDashboard';
import FacultyUpload from '@/components/FacultyUpload';
import ExamCenterView from '@/components/ExamCenterView';

const Index = () => {
  const [currentUser, setCurrentUser] = useState<{role: string; username: string} | null>(null);

  const handleLogin = (role: string, username: string) => {
    setCurrentUser({ role, username });
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  // Role-based rendering
  if (!currentUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  switch (currentUser.role) {
    case 'admin':
      return <AdminDashboard username={currentUser.username} onLogout={handleLogout} />;
    case 'faculty':
      return <FacultyUpload username={currentUser.username} onLogout={handleLogout} />;
    case 'exam_center':
      return <ExamCenterView username={currentUser.username} onLogout={handleLogout} />;
    default:
      return <LoginPage onLogin={handleLogin} />;
  }
};

export default Index;
