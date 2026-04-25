

export default function VolunteersPage() {
    return (
        <div className="page-content volunteers-page">
            <h1 className="section-title">Join the <span className="neon-text">Movement</span></h1>
            <p className="hero-subtitle">Help us build the first large-scale availability dataset in Africa.</p>

            <div className="guide-section">
                <h2 className="neon-text">Windows Installation Guide</h2>
                <div className="step-grid">
                    <div className="step glass">
                        <h3>1. Download & Launch</h3>
                        <p>Download the installer and double-click to start.</p>
                        <img src="/windows_install_step1_1777155391224.png" alt="Windows Setup Step 1" className="step-img" />
                    </div>
                    <div className="step glass">
                        <h3>2. Verification</h3>
                        <p>The agent will appear in your system tray once active.</p>
                        <img src="/windows_install_step2_1777155404006.png" alt="Windows Setup Step 2" className="step-img" />
                    </div>
                </div>
            </div>

            <div className="guide-section" style={{ marginTop: '80px' }}>
                <h2 className="neon-text">Linux Installation Guide</h2>
                <div className="step glass large-step">
                    <h3>Terminal Setup</h3>
                    <p>Run the following commands to install and enable the service.</p>
                    <div className="terminal-preview">
                        <img src="/linux_install_terminal_1777155416748.png" alt="Linux Terminal Setup" className="step-img" />
                    </div>
                </div>
            </div>
        </div>
    );
}
