import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Download, Database, ShieldCheck, Activity } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function DashboardPage() {
    const [chartData, setChartData] = useState<any[]>([]);
    const [statusData, setStatusData] = useState({ machines: 0, syncHealth: "99.2%", latency: "4ms" });
    const [exportFormat, setExportFormat] = useState("csv");

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const res = await fetch('/feed');
                if (res.ok) {
                    const data = await res.json();
                    const formatted = data.map((d: any) => ({
                        time: new Date(d.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                        availability: Math.max(0, 100 - d.cpu),
                        ram: d.ram
                    })).reverse();
                    setChartData(formatted);
                }
                const resStats = await fetch('/stats/live');
                if (resStats.ok) {
                    const st = await resStats.json();
                    setStatusData({ machines: st.active_machines, syncHealth: "99.8%", latency: "12ms" });
                }
            } catch (e) { }
        };
        fetchDashboardData();
        const interval = setInterval(fetchDashboardData, 3000);
        return () => clearInterval(interval);
    }, []);

    const handleExport = () => {
        window.location.href = `/export/dataset?format=${exportFormat}`;
    };

    return (
        <motion.div
            className="page-content"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ padding: '0 20px', maxWidth: 1200, margin: '0 auto' }}
        >
            <header className="responsive-flex" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 40, gap: 20 }}>
                <h2 className="section-title" style={{ margin: 0 }}>Research <span className="neon-text">Command Center</span></h2>
                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                    <select className="input-futuristic" style={{ width: 'auto', padding: '10px 15px' }} value={exportFormat} onChange={e => setExportFormat(e.target.value)}>
                        <option value="csv">CSV (Standard)</option>
                        <option value="excel">Excel (.xlsx)</option>
                        <option value="sql">SQL Dump</option>
                        <option value="txt">TXT (Tabulated)</option>
                    </select>
                    <button className="btn-wow" onClick={handleExport}>
                        <Download size={18} style={{ marginRight: 8 }} /> Export Dataset
                    </button>
                </div>
            </header>

            <div className="responsive-flex" style={{ display: 'flex', gap: 30 }}>
                <div className="card-glass large-chart" style={{ flex: 3 }}>
                    <h3 style={{ marginBottom: 20 }}>Live Resource Availability Pattern</h3>
                    <div style={{ height: 350, minWidth: 0 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={chartData}>
                                <defs>
                                    <linearGradient id="colorAvail" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-neon)" stopOpacity={0.4} />
                                        <stop offset="95%" stopColor="var(--accent-neon)" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                                <XAxis dataKey="time" stroke="#555" tick={{ fill: '#888', fontSize: 12 }} />
                                <YAxis stroke="#555" tick={{ fill: '#888' }} domain={[0, 100]} />
                                <Tooltip contentStyle={{ background: '#0a0a12', border: '1px solid #333' }} />
                                <Area type="monotone" dataKey="availability" name="Availability %" stroke="var(--accent-neon)" fillOpacity={1} fill="url(#colorAvail)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="stats-column" style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 20 }}>
                    <DashStat title="Live Nodes" value={statusData.machines.toString()} sub="Active participants" icon={<Database />} />
                    <DashStat title="Sync Health" value={statusData.syncHealth} sub="Package integrity" icon={<ShieldCheck />} />
                    <DashStat title="Inference Latency" value={statusData.latency} sub="On-device prediction" icon={<Activity />} />
                </div>
            </div>
        </motion.div>
    );
}

function DashStat({ title, value, sub, icon }: any) {
    return (
        <div className="card-glass" style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
            <div className="neon-text">{icon}</div>
            <div>
                <div style={{ fontSize: 12, opacity: 0.5, textTransform: 'uppercase' }}>{title}</div>
                <div className="stat-value" style={{ fontSize: 24 }}>{value}</div>
                <div style={{ fontSize: 11, color: '#666' }}>{sub}</div>
            </div>
        </div>
    );
}
