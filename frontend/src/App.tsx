import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import './App.css';

// Pages
import AboutPage from './pages/About';
import DocumentationPage from './pages/Documentation';
import VolunteersPage from './pages/Volunteers';
import LoginPage from './pages/Login';
import DashboardPage from './pages/Dashboard';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('vc_token'));

  const handleLogin = (newToken: string) => {
    setToken(newToken);
    localStorage.setItem('vc_token', newToken);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('vc_token');
  };

  return (
    <Router>
      <div className="app-container">
        <nav className="navbar glass">
          <Link to="/" className="logo neon-text">VC-UY1</Link>
          <div className="nav-links">
            <Link to="/about">About</Link>
            <Link to="/documentation">Doc</Link>
            <Link to="/volunteers">Volunteers</Link>
            {token ? (
              <>
                <Link to="/dashboard" className="neon-text">Dashboard</Link>
                <button className="logout-btn" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <Link to="/login">Admin Login</Link>
            )}
          </div>
        </nav>

        <main className="content">
          <Routes>
            <Route path="/" element={<LandingView />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/documentation" element={<DocumentationPage />} />
            <Route path="/volunteers" element={<VolunteersPage />} />
            <Route path="/login" element={token ? <Navigate to="/dashboard" /> : <LoginPage onLogin={handleLogin} />} />
            <Route path="/dashboard" element={token ? <DashboardPage token={token} /> : <Navigate to="/login" />} />
          </Routes>
        </main>

        <footer className="footer glass">
          <p>© 2026 VC-UY1 - University of Yaoundé 1 - M2 Research</p>
        </footer>
      </div>
    </Router>
  );
}

function LandingView() {
  const navigate = useNavigate();
  return (
    <section className="hero">
      <h1 className="hero-title">VC-UY1: <br /><span className="neon-text">Volunteer Computing Resilience</span></h1>
      <p className="hero-subtitle">Harnessing African idle compute power through frugal TinyML prediction.</p>
      <div className="hero-actions">
        <button className="btn-primary" onClick={() => navigate('/volunteers')}>Download Agent</button>
        <button className="btn-secondary" onClick={() => navigate('/about')}>Learn More</button>
      </div>

      <div className="hero-stats">
        <div className="stat-card glass shadow-neon">
          <h3>F1 Prediction</h3>
          <p className="neon-text">82.4%</p>
        </div>
        <div className="stat-card glass">
          <h3>RAM Used</h3>
          <p className="neon-text">&lt; 8 MB</p>
        </div>
        <div className="stat-card glass">
          <h3>Dataset Size</h3>
          <p className="neon-text">484k+</p>
        </div>
      </div>
    </section>
  );
}

export default App;
