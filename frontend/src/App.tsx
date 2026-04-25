import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence, type Variants } from 'framer-motion';
import { Activity, Shield, Download, Info, Book, LogIn, Server, Cpu, Zap, ArrowRight, User } from 'lucide-react';
import './App.css';

// --- ANIMATION VARIANTS ---
const pageVariants: Variants = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.6 } },
  exit: { opacity: 0, x: 20, transition: { duration: 0.4 } }
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
      <Link to="/" className="logo">VC-UY1</Link>
      <div className="nav-links">
        <NavLink to="/about" active={location.pathname === '/about'} icon={<Info size={16} />}>About</NavLink>
        <NavLink to="/documentation" active={location.pathname === '/documentation'} icon={<Book size={16} />}>Spec</NavLink>
        <NavLink to="/volunteers" active={location.pathname === '/volunteers'} icon={<Download size={16} />}>Join</NavLink>
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
  return (
    <motion.section
      className="page-content hero-section"
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <div className="hero-grid">
        <div className="hero-text">
          <motion.h1 className="hero-title" initial={{ scale: 0.95 }} animate={{ scale: 1 }}>
            Resilient <br />
            <span className="gradient-text">African VC</span> <br />
            Infrastructure
          </motion.h1>
          <p className="hero-subtitle">
            Harnessing underutilized compute power in resource-constrained environments using frugal TinyML availability prediction.
          </p>
          <div className="hero-actions">
            <Link to="/volunteers" className="btn-wow">Become a Contributor <ArrowRight style={{ marginLeft: 8 }} /></Link>
            <Link to="/about" className="btn-outline">Watch Research Overview</Link>
          </div>
        </div>

        <div className="hero-visual">
          <motion.div
            className="floating-glow"
            animate={{
              y: [0, -20, 0],
              rotate: [0, 5, 0]
            }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
          >
            <div className="visual-card card-glass pulse">
              <Cpu size={80} className="neon-text" />
              <div style={{ marginTop: 20 }}>
                <div style={{ fontSize: 12, opacity: 0.5 }}>INFRASTRUCTURE STATE</div>
                <div style={{ fontSize: 24, fontWeight: 700 }}>OPTIMIZED</div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      <motion.div className="stats-strip" variants={staggerContainer} initial="initial" animate="animate">
        <StatCard icon={<Server />} value="484k" label="Snapshots Collected" />
        <StatCard icon={<Zap />} value="82.4%" label="Prediction F1-Score" />
        <StatCard icon={<Shield />} value="< 8MB" label="Model Footprint" />
      </motion.div>
    </motion.section>
  );
}

function StatCard({ icon, value, label }: any) {
  return (
    <motion.div className="card-glass" variants={pageVariants}>
      <div className="neon-text" style={{ marginBottom: 10 }}>{icon}</div>
      <div className="stat-value">{value}</div>
      <div style={{ color: 'var(--text-dim)', fontSize: 13, fontWeight: 500 }}>{label}</div>
    </motion.div>
  );
}

function VolunteersPage() {
  return (
    <motion.section className="page-content" variants={pageVariants} initial="initial" animate="animate" exit="exit" style={{ padding: '0 60px' }}>
      <h2 className="section-title">Join the <span className="neon-text">Movement</span></h2>
      <div className="guide-layout">
        <div className="guide-card card-glass">
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}><span style={{ fontSize: 32 }}>🪟</span> <h3>Windows Deployment</h3></div>
          <p style={{ marginTop: 15, color: '#999' }}>Download our specialized installer to start contributing. Optimized for Windows 10/11.</p>
          <button className="btn-wow" style={{ marginTop: 20, width: '100%' }}>Fetch Installer (.exe)</button>
          <div className="img-container" style={{ marginTop: 20 }}>
            <img src="/windows_install_step1_1777155391224.png" alt="Setup" style={{ width: '100%', borderRadius: 12 }} />
          </div>
        </div>

        <div className="guide-card card-glass" style={{ borderColor: 'rgba(255,255,255,0.05)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}><span style={{ fontSize: 32 }}>🐧</span> <h3>Linux Terminal Service</h3></div>
          <p style={{ marginTop: 15, color: '#999' }}>Deploy as a background systemd service for maximum uptime and zero interference.</p>
          <div className="code-block" style={{ marginTop: 20, background: '#000', padding: 20, borderRadius: 12, fontSize: 13, border: '1px solid #333' }}>
            <code style={{ color: 'var(--accent-neon)' }}>$ sudo dpkg -i vc-agent.deb</code><br />
            <code style={{ color: 'var(--accent-neon)' }}>$ sudo systemctl enable --now vc-agent</code>
          </div>
          <div className="img-container" style={{ marginTop: 20 }}>
            <img src="/linux_install_terminal_1777155416748.png" alt="Terminal" style={{ width: '100%', borderRadius: 12 }} />
          </div>
        </div>
      </div>
    </motion.section>
  );
}

function LoginPage() {
  return (
    <motion.div className="page-content" variants={pageVariants} initial="initial" animate="animate" exit="exit" style={{ display: 'flex', justifyContent: 'center' }}>
      <div className="card-glass" style={{ maxWidth: 450, width: '100%', textAlign: 'center' }}>
        <div className="icon neon-text" style={{ marginBottom: 20, display: 'inline-block' }}><User size={40} /></div>
        <h2>Admin Access</h2>
        <p style={{ color: '#777', marginTop: 10, marginBottom: 30 }}>Secure area for Master 2 Research Team only.</p>
        <input type="text" placeholder="Access key or username" className="input-futuristic" />
        <input type="password" placeholder="System password" className="input-futuristic" style={{ marginTop: 15 }} />
        <button className="btn-wow" style={{ marginTop: 30, width: '100%' }}>Establish Connection</button>
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
              <Route path="/volunteers" element={<VolunteersPage />} />
              <Route path="/login" element={<LoginPage />} />
              {/* Other routes added here */}
            </Routes>
          </AnimatePresence>
        </main>

        <footer className="footer-premium">
          <div className="footer-line" />
          <p>© 2026 UC-UY1 Laboratory - Advancing Frugal Distributed Computing</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
