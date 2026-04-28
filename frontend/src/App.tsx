import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence, type Variants } from 'framer-motion';
import { Activity, Shield, Download, Info, Book, LogIn, Server, Zap, ArrowRight, User, Globe, Lock, CheckCircle2, ShieldAlert, Mail } from 'lucide-react';
import './App.css';

// --- ANIMATION VARIANTS ---
const pageVariants: Variants = {
  initial: { opacity: 0, scale: 0.98 },
  animate: { opacity: 1, scale: 1, transition: { duration: 0.5, ease: [0.4, 0, 0.2, 1] } },
  exit: { opacity: 0, scale: 0.98, transition: { duration: 0.3 } }
};

const staggerContainer: Variants = {
  animate: { transition: { staggerChildren: 0.1 } }
};

// --- COMPONENTS ---
function Nav() {
  const location = useLocation();
  const isLogged = !!localStorage.getItem('vc_token');

  return (
    <motion.nav
      className="navbar"
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 100 }}
    >
      <Link to="/" className="logo">
        <img src="/logo.svg?v=gold_final_v2" alt="VC-UY1 Logo" style={{ height: '35px', filter: 'drop-shadow(0 0 8px rgba(204, 255, 0, 0.4))' }} />
      </Link>
      <div className="nav-links">
        <NavLink to="/about" active={location.pathname === '/about'} icon={<Info size={16} />}>About</NavLink>
        <NavLink to="/documentation" active={location.pathname === '/documentation'} icon={<Book size={16} />}>Spec</NavLink>
        <NavLink to="/volunteers" active={location.pathname === '/volunteers'} icon={<Download size={16} />}>Join</NavLink>
        <NavLink to="/docs" active={location.pathname === '/docs'} icon={<Lock size={16} />}>Transparency</NavLink>
        <NavLink to="/contact" active={location.pathname === '/contact'} icon={<Mail size={16} />}>Contact</NavLink>
        {isLogged ? (
          <NavLink to="/dashboard" active={location.pathname === '/dashboard'} icon={<Activity size={16} />} className="neon-text">Dashboard</NavLink>
        ) : (
          <NavLink to="/login" active={location.pathname === '/login'} icon={<LogIn size={16} />}>Admin</NavLink>
        )}
      </div>
    </motion.nav>
  );
}

function NavLink({ to, children, active, icon, className = "" }: any) {
  return (
    <Link to={to} className={`nav-link ${active ? 'active' : ''} ${className}`}>
      <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {icon} {children}
      </span>
    </Link>
  );
}

// --- PAGES ---
function LandingPage() {
  const [liveData, setLiveData] = useState<any[]>([]);
  const [stats, setStats] = useState({ snapshots: 0, f1_score: "82.4%", footprint: "< 8MB" });

  useEffect(() => {
    const fetchLiveFeed = async () => {
      try {
        const res = await fetch('/feed');
        if (res.ok) {
          const data = await res.json();
          setLiveData(data);
        }
      } catch (e) {
        console.error("Live feed offline");
      }
    };

    const fetchStats = async () => {
      try {
        const res = await fetch('/stats/live');
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (e) { }
    };

    fetchLiveFeed();
    fetchStats();

    const interval = setInterval(() => {
      fetchLiveFeed();
      fetchStats();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <motion.section className="page-content hero-section" variants={pageVariants} initial="initial" animate="animate" exit="exit">
      <div className="hero-grid">
        <div className="hero-text">
          <motion.h1 className="hero-title">Resilient <br /> <span className="gradient-text">African VC</span> <br /> Infrastructure</motion.h1>
          <p className="hero-subtitle">Harnessing underutilized compute power in resource-constrained environments using frugal TinyML availability prediction.</p>
          <div className="hero-actions">
            <Link to="/volunteers" className="btn-wow">Become a Contributor <ArrowRight style={{ marginLeft: 8 }} /></Link>
            <Link to="/about" className="btn-outline">Watch Research Overview</Link>
          </div>
        </div>
        <div className="hero-visual">
          <img src="/hero_illustration.svg" alt="Cyber Grid Elements" style={{ width: '100%', maxWidth: '400px', transform: 'scale(1.1)' }} />
        </div>
      </div>

      <motion.div className="stats-strip" variants={staggerContainer} initial="initial" animate="animate" style={{ marginTop: 40 }}>
        <StatCard icon={<Server />} value={stats.snapshots.toLocaleString() + (stats.snapshots > 0 ? '' : '+')} label="Snapshots Collected (Live)" />
        <StatCard icon={<Zap />} value={stats.f1_score} label="Prediction F1-Score" />
        <StatCard icon={<Shield />} value={stats.footprint} label="Model Footprint" />
      </motion.div>

      {/* ENLARGED ARCHITECTURE SVG */}
      <div style={{ marginTop: 80, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <h3 style={{ fontSize: 24, marginBottom: 20, textAlign: 'center' }}><Globe className="neon-text" style={{ display: 'inline', verticalAlign: 'middle', marginRight: 10 }} /> Distributed Artificial Intelligence Architecture</h3>
        <motion.div className="floating-glow" animate={{ y: [0, -10, 0] }} transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }} style={{ width: '100%', maxWidth: '1000px' }}>
          <img src="/architecture.svg" alt="Distributed Architecture" style={{ width: '100%', borderRadius: 20, boxShadow: '0 20px 40px rgba(0,0,0,0.5)' }} />
        </motion.div>
      </div>

      <div style={{ marginTop: 80 }}>
        <h3 style={{ fontSize: 24, marginBottom: 20, display: 'flex', alignItems: 'center', gap: 10 }}><Activity className="neon-text" /> Live Volunteer Telemetry Stream</h3>
        <p style={{ marginBottom: 20, color: '#aaa' }}>Real-time transmission from global nodes (last 50 packets). Full access is restricted to authenticated researchers.</p>
        <div className="card-glass" style={{ maxHeight: 400, overflowY: 'auto', padding: 0 }}>
          <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #333', backgroundColor: 'rgba(0,0,0,0.5)' }}>
                <th style={{ padding: '15px 20px', color: '#888' }}>Snapshot ID</th>
                <th style={{ padding: '15px 20px', color: '#888' }}>Timestamp</th>
                <th style={{ padding: '15px 20px', color: '#888' }}>CPU Load</th>
                <th style={{ padding: '15px 20px', color: '#888' }}>RAM Usaage</th>
                <th style={{ padding: '15px 20px', color: '#888' }}>Power State</th>
              </tr>
            </thead>
            <tbody>
              {liveData.map((s, i) => (
                <motion.tr
                  key={s.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  style={{ borderBottom: '1px solid #222' }}
                >
                  <td style={{ padding: '15px 20px', fontFamily: 'monospace', color: '#ccff00' }}>#{s.id}</td>
                  <td style={{ padding: '15px 20px', color: '#ddd' }}>{new Date(s.timestamp * 1000).toLocaleTimeString()}</td>
                  <td style={{ padding: '15px 20px', color: '#ddd' }}>{s.cpu}%</td>
                  <td style={{ padding: '15px 20px', color: '#ddd' }}>{s.ram}%</td>
                  <td style={{ padding: '15px 20px' }}>
                    {s.plugged ? <span style={{ color: '#27c93f', fontSize: 12 }}>⚡ PLUGGED</span> : <span style={{ color: '#ffbd2e', fontSize: 12 }}>🔋 {s.battery}%</span>}
                  </td>
                </motion.tr>
              ))}
              {liveData.length === 0 && (
                <tr><td colSpan={5} style={{ padding: 40, textAlign: 'center', color: '#555' }}>Awaiting incoming streams...</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </motion.section>
  );
}

function StatCard({ icon, value, label }: any) {
  return (
    <motion.div className="card-glass" style={{ textAlign: 'center' }} variants={pageVariants}>
      <div className="neon-text" style={{ marginBottom: 10, display: 'flex', justifyContent: 'center' }}>{icon}</div>
      <div className="stat-value">{value}</div>
      <div style={{ color: 'var(--text-dim)', fontSize: 13, fontWeight: 500 }}>{label}</div>
    </motion.div>
  );
}

function AboutPage() {
  return (
    <motion.section className="page-content" variants={pageVariants} initial="initial" animate="animate" exit="exit" style={{ padding: '0 60px' }}>
      <h2 className="section-title">The <span className="neon-text">VC-UY1</span> Mission</h2>
      <div className="card-glass" style={{ lineHeight: 1.8, fontSize: '18px' }}>
        <p>Our research focuses on the unique challenges of **Volunteer Computing (VC)** in Sub-Saharan Africa, specifically targeting the **University of Yaoundé 1** ecosystem.</p>
        <p style={{ marginTop: 20 }}>With power grid instability being a major factor, we implement **TinyML models (GRU/LSTM)** that run locally on volunteer machines to predict availability windows, allowing the global scheduler to make intelligent task distribution decisions.</p>
        <div className="responsive-grid" style={{ marginTop: 40, gap: '30px' }}>
          <div className="card-glass" style={{ padding: '20px', textAlign: 'center' }}>
            <Globe className="neon-text" style={{ marginBottom: 15 }} />
            <h4>Local Relevance</h4>
            <p style={{ fontSize: 14, opacity: 0.7 }}>First dataset modeling Cameroon's specific power cycles.</p>
          </div>
          <div className="card-glass" style={{ padding: '20px', textAlign: 'center' }}>
            <Zap className="neon-text" style={{ marginBottom: 15 }} />
            <h4>Frugal AI</h4>
            <p style={{ fontSize: 14, opacity: 0.7 }}>Inference optimized for low-end hardware and high latency.</p>
          </div>
          <div className="card-glass" style={{ padding: '20px', textAlign: 'center' }}>
            <Lock className="neon-text" style={{ marginBottom: 15 }} />
            <h4>Privacy First</h4>
            <p style={{ fontSize: 14, opacity: 0.7 }}>Fully anonymous MAC-hashing for participant security.</p>
          </div>
        </div>
      </div>
    </motion.section>
  );
}

function VolunteersPage() {
  return (
    <motion.section className="page-content" variants={pageVariants} initial="initial" animate="animate" exit="exit" style={{ padding: '0 60px' }}>
      <h2 className="section-title">Join the <span className="neon-text">Movement</span></h2>
      <p style={{ marginBottom: 30, color: '#aaa', fontSize: 18, maxWidth: 800 }}>Help our academic research by donating small amounts of your computer's spare time. Follow these secure, step-by-step guides to join the grid.</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>

        {/* WINDOWS GUIDE */}
        <div className="guide-card card-glass responsive-flex" style={{ display: 'flex', gap: 40 }}>
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: 20 }}>
              <span style={{ fontSize: 40 }}>🪟</span>
              <h3>Windows Deployment <span className="neon-text">(Recommended)</span></h3>
            </div>

            <div className="card-glass" style={{ padding: '15px 20px', marginBottom: 20, borderColor: 'rgba(255, 189, 46, 0.3)', background: 'rgba(255, 189, 46, 0.05)' }}>
              <p style={{ fontSize: 13, color: '#ffbd2e', display: 'flex', alignItems: 'center', gap: 10 }}>
                <ShieldAlert size={16} />
                <span>Note : Logiciel de recherche certifié par l'UY1, mais non signé numériquement. Un avertissement Windows apparaîtra au premier lancement.</span>
              </p>
            </div>

            <div className="step-list">
              <div className="step"><CheckCircle2 className="neon-text" size={20} /> <span><strong>Étape 1:</strong> Téléchargez l'exécutable natif compilé. Aucune installation requise, c'est un fichier standalone.</span></div>
              <div className="step"><CheckCircle2 className="neon-text" size={20} /> <span><strong>Étape 2:</strong> Double-cliquez pour l'exécuter. Il tournera discrètement en arrière-plan sans ralentir votre PC.</span></div>
              <div className="step"><CheckCircle2 className="neon-text" size={20} /> <span><strong>Étape 3:</strong> La télémétrie locale commence. Le client gère automatiquement les coupures de courant.</span></div>
            </div>

            <a href="/vc-agent-windows.exe" download className="btn-wow" style={{ marginTop: 30, width: '100%', display: 'inline-block', textAlign: 'center' }}>Download vc-agent-windows.exe</a>
            <Link to="/install/windows" className="btn-outline" style={{ marginTop: 15, width: '100%', display: 'inline-block', textAlign: 'center' }}>View Visual Setup Guide</Link>
          </div>

          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img src="/windows_diag.svg" alt="Windows Setup Diagram" style={{ width: '100%', borderRadius: 12, boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }} />
          </div>
        </div>

        {/* LINUX GUIDE */}
        <div className="guide-card card-glass responsive-flex" style={{ display: 'flex', gap: 40, borderColor: '#333' }}>
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: 20 }}>
              <span style={{ fontSize: 40 }}>🐧</span>
              <h3>Linux Terminal / Server</h3>
            </div>

            <div className="step-list">
              <div className="step"><CheckCircle2 className="neon-text" size={20} /> <span><strong>Étape 1:</strong> Download the pre-compiled binary via CLI on your Ubuntu/Debian lab node.</span></div>
              <div className="step"><CheckCircle2 className="neon-text" size={20} /> <span><strong>Étape 2:</strong> Accordez les droits d'exécution avec <code>chmod +x</code>.</span></div>
              <div className="step"><CheckCircle2 className="neon-text" size={20} /> <span><strong>Étape 3:</strong> Démarrez l'agent. Idéal pour les configurations de graphes distribués dans les Amphithéâtres.</span></div>
            </div>

            <div className="code-block" style={{ marginTop: 20, background: '#000', padding: 20, borderRadius: 12, fontSize: 13, border: '1px solid #333', fontFamily: 'monospace' }}>
              <span style={{ color: 'var(--accent-neon)' }}>$</span> wget http://vc-uy1.npe-techs.com/vc-agent-linux<br />
              <span style={{ color: 'var(--accent-neon)' }}>$</span> chmod +x vc-agent-linux<br />
              <span style={{ color: 'var(--accent-neon)' }}>$</span> ./vc-agent-linux
            </div>
            <a href="/vc-agent-linux" download className="btn-outline" style={{ marginTop: 15, display: 'inline-block', width: '100%', textAlign: 'center' }}>Download Binary directly</a>
          </div>

          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img src="/linux_diag.svg" alt="Linux Setup Diagram" style={{ width: '100%', borderRadius: 12, boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }} />
          </div>
        </div>

      </div>
    </motion.section>
  );
}

import DashboardPage from './pages/Dashboard';
import InstallationPage from './pages/Installation';
import DocumentationPage from './pages/Documentation';
import ContactPage from './pages/Contact';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const fd = new FormData();
      fd.append('username', username);
      fd.append('password', password);
      const res = await fetch('/token', { method: 'POST', body: fd });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('vc_token', data.access_token);
        window.location.href = '/dashboard';
      } else {
        setError('Invalid credentials');
      }
    } catch (e) {
      setError('Connection to backend failed');
    }
  };

  return (
    <motion.div className="page-content" variants={pageVariants} initial="initial" animate="animate" exit="exit" style={{ display: 'flex', justifyContent: 'center' }}>
      <div className="card-glass" style={{ maxWidth: 450, width: '100%', textAlign: 'center' }}>
        <div className="icon neon-text" style={{ marginBottom: 20, display: 'inline-block' }}><User size={40} /></div>
        <h2>Admin Access</h2>
        <p style={{ color: '#777', marginTop: 10, marginBottom: 30 }}>Secure area for Master 2 Research Team only.</p>
        {error && <p style={{ color: '#ff5f56', marginBottom: 15 }}>{error}</p>}
        <input type="text" placeholder="Access key or username" value={username} onChange={e => setUsername(e.target.value)} className="input-futuristic" />
        <input type="password" placeholder="System password" value={password} onChange={e => setPassword(e.target.value)} className="input-futuristic" style={{ marginTop: 15 }} />
        <button onClick={handleLogin} className="btn-wow" style={{ marginTop: 30, width: '100%' }}>Establish Connection</button>
      </div>
    </motion.div>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Nav />
        <main style={{ flex: 1, padding: '60px 0' }}>
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/documentation" element={<LandingPage />} /> {/* Placeholder to avoid 404 in dev */}
              <Route path="/volunteers" element={<VolunteersPage />} />
              <Route path="/install/windows" element={<InstallationPage />} />
              <Route path="/docs" element={<DocumentationPage />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
            </Routes>
          </AnimatePresence>
        </main>
        <footer className="footer-premium">
          <div className="footer-line" />
          <p>© 2026 UC-UY1 Laboratory - Advancing Frugal Distributed Computing  By Npe-Techs. </p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
