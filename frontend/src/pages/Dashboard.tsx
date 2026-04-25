import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Download, Database, ShieldCheck, Activity } from 'lucide-react';

const mockData = [
    { time: '00:00', availability: 80 },
    { time: '04:00', availability: 45 },
    { time: '08:00', availability: 90 },
    { time: '12:00', availability: 70 },
    { time: '16:00', availability: 30 },
    { time: '20:00', availability: 85 },
];

export default function DashboardPage() {
    return (
        <motion.div
            className="page-content"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ padding: '0 60px' }}
        >
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 40 }}>
                <h2 className="section-title" style={{ margin: 0 }}>Research <span className="neon-text">Command Center</span></h2>
                <button className="btn-wow" onClick={() => window.location.href = 'http://vc-uy1.npe-techs.com/export/dataset'}>
                    <Download size={18} style={{ marginRight: 8 }} /> Export Global Dataset
                </button>
            </header>

            <div className="dashboard-grid-premium">
                <div className="card-glass large-chart">
                    <h3 style={{ marginBottom: 20 }}>Temporal Grid Availability Traces</h3>
                    <div style={{ height: 300 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={mockData}>
                                <defs>
                                    <linearGradient id="colorAvail" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-neon)" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="var(--accent-neon)" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                                <XAxis dataKey="time" stroke="#555" />
                                <YAxis stroke="#555" />
                                <Tooltip contentStyle={{ background: '#0a0a12', border: '1px solid #333' }} />
                                <Area type="monotone" dataKey="availability" stroke="var(--accent-neon)" fillOpacity={1} fill="url(#colorAvail)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="stats-column">
                    <DashStat title="Live Nodes" value="12" sub="Active participants" icon={<Database />} />
                    <DashStat title="Sync Health" value="99.2%" sub="Package integrity" icon={<ShieldCheck />} />
                    <DashStat title="Inference Latency" value="4ms" sub="On-device prediction" icon={<Activity />} />
                </div>
            </div>
        </motion.div>
    );
}

function DashStat({ title, value, sub, icon }: any) {
    return (
        <div className="card-glass" style={{ marginBottom: 20, display: 'flex', alignItems: 'center', gap: 20 }}>
            <div className="neon-text">{icon}</div>
            <div>
                <div style={{ fontSize: 12, opacity: 0.5, textTransform: 'uppercase' }}>{title}</div>
                <div className="stat-value" style={{ fontSize: 24 }}>{value}</div>
                <div style={{ fontSize: 11, color: '#666' }}>{sub}</div>
            </div>
        </div>
    );
}
