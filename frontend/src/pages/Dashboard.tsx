import { useState, useEffect } from 'react';
import { Download, Activity, Server, Zap } from 'lucide-react';

export default function DashboardPage({ }: { token: string }) {
    const [stats, setStats] = useState({ active_machines: 0 });

    useEffect(() => {
        fetch('http://vc-uy1.npe-techs.com/stats/live')
            .then(res => res.json())
            .then(data => setStats(data))
            .catch(console.error);
    }, []);

    const handleExport = () => {
        window.location.href = 'http://vc-uy1.npe-techs.com/export/dataset';
    };

    return (
        <div className="dashboard-content">
            <header className="dashboard-header">
                <h1 className="section-title">Research <span className="neon-text">Insight</span></h1>
                <button className="btn-primary" onClick={handleExport}>
                    <Download size={20} style={{ marginRight: '8px' }} />
                    Export Complete Dataset (ZIP)
                </button>
            </header>

            <div className="stats-grid">
                <div className="stat-card glass">
                    <div className="icon neon-text"><Server /></div>
                    <div className="value">{stats.active_machines}</div>
                    <div className="label">Observed Machines</div>
                </div>
                <div className="stat-card glass">
                    <div className="icon neon-text"><Zap /></div>
                    <div className="value">3.4s</div>
                    <div className="label">Avg. Power-cut Duration</div>
                </div>
                <div className="stat-card glass">
                    <div className="icon neon-text"><Activity /></div>
                    <div className="value">88%</div>
                    <div className="label">Prediction Confidence</div>
                </div>
            </div>

            <div className="main-grid">
                <section className="heatmap-container glass">
                    <h3>Temporal Availability Distribution</h3>
                    <div className="heatmap-mock">
                        {/* Real visualization would go here (e.g. Chart.js) */}
                        <p>Training data population in progress...</p>
                    </div>
                </section>

                <section className="log-container glass">
                    <h3>Recent Synchronization Events</h3>
                    <ul className="log-list">
                        <li><span className="ts">10:42 PM</span> Machine <b>#8fe2</b> synced 12 snapshots <span className="status ok">OK</span></li>
                        <li><span className="ts">10:39 PM</span> Machine <b>#2da1</b> registered <span className="status ok">OK</span></li>
                        <li><span className="ts">10:35 PM</span> Machine <b>#f41b</b> heartbeat offline <span className="status err">LOST</span></li>
                    </ul>
                </section>
            </div>
        </div>
    );
}
