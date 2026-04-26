import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Download, Database, ShieldCheck, Activity, HardDrive } from 'lucide-react';
import { useState, useEffect } from 'react';

const COLORS = ['#00C49F', '#FFBB28', '#FF8042', '#0088FE'];

export default function DashboardPage() {
    const [chartData, setChartData] = useState<any[]>([]);
    const [detailedStats, setDetailedStats] = useState<any>({ os_distribution: [], total_machines: 0, total_snapshots: 0, availability_avg: 99.8 });
    const [exportFormat, setExportFormat] = useState("csv");

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const res = await fetch('/feed');
                if (res.ok) {
                    const data = await res.json();
                    const formatted = data.map((d: any) => ({
                        time: new Date(d.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                        cpu: d.cpu,
                        ram: d.ram
                    })).reverse();
                    setChartData(formatted);
                }
                const resDetailed = await fetch('/stats/detailed');
                if (resDetailed.ok) {
                    const data = await resDetailed.json();
                    setDetailedStats(data);
                }
            } catch (e) { }
        };
        fetchDashboardData();
        const interval = setInterval(fetchDashboardData, 3000);
        return () => clearInterval(interval);
    }, []);

    const handleExport = () => {
        window.location.href = `/export?format=${exportFormat}`;
    };

    return (
        <motion.div
            className="page-content"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ padding: '0 20px', maxWidth: 1400, margin: '0 auto' }}
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

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 20, marginBottom: 30 }}>
                <DashStat title="Total Nodes" value={detailedStats.total_machines} sub="Enrolled participants" icon={<Database />} />
                <DashStat title="Data Snapshots" value={detailedStats.total_snapshots} sub="Unique records" icon={<HardDrive />} />
                <DashStat title="Uptime Avg" value={`${detailedStats.availability_avg}%`} sub="Global persistence" icon={<ShieldCheck />} />
                <DashStat title="Sync Efficiency" value="99.9%" sub="Zero-loss sync" icon={<Activity />} />
            </div>

            <div className="responsive-flex" style={{ display: 'flex', gap: 30, marginBottom: 30 }}>
                <div className="card-glass" style={{ flex: 3 }}>
                    <h3 style={{ marginBottom: 20 }}>Resource Usage Telemetry (Real-time)</h3>
                    <div style={{ height: 350, minWidth: 0 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={chartData}>
                                <defs>
                                    <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-neon)" stopOpacity={0.4} />
                                        <stop offset="95%" stopColor="var(--accent-neon)" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorRam" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8884d8" stopOpacity={0.4} />
                                        <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                                <XAxis dataKey="time" stroke="#555" tick={{ fill: '#888', fontSize: 12 }} />
                                <YAxis stroke="#555" tick={{ fill: '#888' }} domain={[0, 100]} />
                                <Tooltip contentStyle={{ background: '#0a0a12', border: '1px solid #333' }} />
                                <Area type="monotone" dataKey="cpu" name="CPU Usage %" stroke="var(--accent-neon)" fillOpacity={1} fill="url(#colorCpu)" />
                                <Area type="monotone" dataKey="ram" name="RAM Usage %" stroke="#8884d8" fillOpacity={1} fill="url(#colorRam)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="card-glass" style={{ flex: 1.2 }}>
                    <h3 style={{ marginBottom: 20 }}>OS Distribution</h3>
                    <div style={{ height: 300 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={detailedStats.os_distribution}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                    stroke="none"
                                >
                                    {detailedStats.os_distribution.map((_: any, index: number) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                        <div style={{ display: 'flex', justifyContent: 'center', gap: 15, marginTop: 10 }}>
                            {detailedStats.os_distribution.map((d: any, i: number) => (
                                <div key={i} style={{ display: 'flex', alignItems: 'center', fontSize: 12, color: '#aaa' }}>
                                    <div style={{ width: 10, height: 10, borderRadius: '50%', background: COLORS[i % COLORS.length], marginRight: 5 }}></div>
                                    {d.name}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}

function DashStat({ title, value, sub, icon }: any) {
    return (
        <div className="card-glass" style={{ display: 'flex', alignItems: 'center', gap: 20, padding: '25px' }}>
            <div className="neon-text" style={{ transform: 'scale(1.2)' }}>{icon}</div>
            <div>
                <div style={{ fontSize: 11, opacity: 0.5, textTransform: 'uppercase', letterSpacing: 1 }}>{title}</div>
                <div className="stat-value" style={{ fontSize: 28, fontWeight: 'bold' }}>{value}</div>
                <div style={{ fontSize: 11, color: '#666' }}>{sub}</div>
            </div>
        </div>
    );
}
