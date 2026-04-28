import { motion } from 'framer-motion';
import { ShieldCheck, BookOpen, Download, ShieldAlert } from 'lucide-react';

const Documentation = () => {
    const modules = [
        {
            id: "01",
            title: "Hardware Specifications",
            img: "/docs_requirements_v3.svg",
            color: "var(--accent-neon)",
            desc: "Spécifications minimales pour une exécution fluide sur les terminaux distribués.",
            rows: [
                { k: "OS Architecture", v: "Windows 10/11 x64 | Linux 20.04+" },
                { k: "Runtime Footprint", v: "Fixed 32MB RAM | < 1% CPU Load" },
                { k: "Local Storage", v: "SQLite Data Lake (Max 50MB)" },
                { k: "Connectivity", v: "Periodic Pulse (TLS 1.3 Encryption)" }
            ]
        },
        {
            id: "02",
            title: "Telemetry Protocol",
            img: "/docs_collection_v3.svg",
            color: "var(--accent-neon)",
            desc: "Architecture d'agrégation locale pour la protection des données brutes.",
            rows: [
                { k: "Sampling Rate", v: "Intra-minute active polling" },
                { k: "Consolidation", v: "Local Mean Calculation (5 mins)" },
                { k: "Data Vectors", v: "CPU-Util / RAM-Usage / Battery" },
                { k: "Stealth Layer", v: "Silent background orchestration" }
            ]
        },
        {
            id: "03",
            title: "Zero-Knowledge Privacy",
            img: "/docs_privacy_v3.svg",
            color: "var(--accent-neon)",
            desc: "Anonymisation cryptographique irréversible des identifiants des volontaires.",
            rows: [
                { k: "Node ID Hash", v: "MAC Address -> Salted SHA-256" },
                { k: "File Protection", v: "Absolute zero-access policy" },
                { k: "Sensor Isolation", v: "Camera / Mic / Keyboard excluded" },
                { k: "Auth Standard", v: "Verified Research Protocol" }
            ]
        },
        {
            id: "04",
            title: "Energy & Availability",
            img: "/docs_impact_v3.svg",
            color: "var(--accent-neon)",
            desc: "Modélisation des cycles de disponibilité énergétique en zone urbaine.",
            rows: [
                { k: "Power Resilience", v: "Auto-reboot / Session recovery" },
                { k: "Inference Mode", v: "Low-Power ECO Cycle" },
                { k: "Cost Impact", v: "Estimated < 0.5 / Day" },
                { k: "Network Data", v: "Compressed Payloads (< 1MB/j)" }
            ]
        },
        {
            id: "05",
            title: "Research Ethics",
            img: "/docs_consent_v3.svg",
            color: "var(--accent-neon)",
            desc: "Conformité totale avec les standards de recherche longitudinale.",
            rows: [
                { k: "Consent Level", v: "Granular UI handshake (1 to 4)" },
                { k: "User Rights", v: "Immediate withdrawal / Deletion" },
                { k: "Focus Area", v: "Distributed Resource Prediction" },
                { k: "Ref Standard", v: "Standardized Protocol" }
            ]
        },
        {
            id: "06",
            title: "Technical Support",
            img: "/docs_support_v3.svg",
            color: "var(--accent-neon)",
            desc: "Canal direct pour la maintenance et le support technique du nœud.",
            rows: [
                { k: "Status Monitoring", v: "Real-time Dashboard Visibility" },
                { k: "Update Policy", v: "Transparent Delta Patching" },
                { k: "Primary Contact", v: "support@node.tech (24/7)" },
                { k: "Node Identity", v: "VC-REARCH-NODE-P256" }
            ]
        }
    ];

    return (
        <motion.div
            className="page-content hero-section"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ paddingBottom: 100 }}
        >
            <div className="hero-text" style={{ marginBottom: 80, textAlign: 'center', width: '100%', maxWidth: 'none' }}>
                <motion.div
                    initial={{ y: -20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    className="neon-text"
                    style={{ fontSize: 11, fontWeight: 900, letterSpacing: 5, textTransform: 'uppercase', marginBottom: 25 }}
                >
                    <ShieldCheck size={16} style={{ verticalAlign: 'middle', marginRight: 12 }} />
                    Research Transparency Protocol V3.1 (Neon Hub)
                </motion.div>
                <h1 className="section-title">Technical <span className="neon-text">Deep Dive</span></h1>
                <p className="hero-subtitle" style={{ margin: '0 auto', fontSize: 18, opacity: 0.7 }}>
                    Spécifications rattachées à l'architecture VC-UY1. <br />
                    Chaque module est optimisé pour garantir l'anonymat total et une consommation nulle.
                </p>
            </div>

            {/* RESPONSIVE GRID FIX */}
            <div className="responsive-grid" style={{ gap: 25 }}>
                {modules.map((m, idx) => (
                    <motion.div
                        key={m.id}
                        className="card-glass"
                        style={{ padding: 40, height: '100%', display: 'flex', flexDirection: 'column' }}
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 30 }}>
                            <div className="neon-text" style={{ fontSize: 14, fontWeight: 900 }}>{m.id}</div>
                            <BookOpen size={16} style={{ color: 'var(--accent-neon)', opacity: 0.2 }} />
                        </div>

                        <div style={{ height: 180, display: 'flex', justifyContent: 'center', marginBottom: 35 }}>
                            <img
                                src={`${m.img}?v=3.1`}
                                style={{ height: '100%', filter: 'drop-shadow(0 0 15px var(--accent-neon)) brightness(1.2)' }}
                                alt={m.title}
                            />
                        </div>

                        <h3 style={{ fontSize: 22, color: '#fff', marginBottom: 12 }}>{m.title}</h3>
                        <p style={{ color: 'var(--text-dim)', fontSize: 13, marginBottom: 25, lineHeight: 1.6 }}>{m.desc}</p>

                        <div style={{ marginTop: 'auto', borderTop: '1px solid rgba(212,255,0,0.05)', paddingTop: 20, display: 'grid', gap: 10 }}>
                            {m.rows.map((row, rIdx) => (
                                <div key={rIdx} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11 }}>
                                    <span style={{ color: '#555', fontWeight: 800, textTransform: 'uppercase' }}>{row.k}</span>
                                    <span style={{ color: 'var(--accent-neon)', fontWeight: 900 }}>{row.v}</span>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* PRIVACY EXCLUSION (Monochrome) */}
            <motion.div
                className="card-glass"
                style={{ marginTop: 80, padding: '60px 40px', borderColor: 'rgba(212,255,0,0.1)', background: 'rgba(212,255,0,0.01)' }}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
            >
                <div style={{ textAlign: 'center', marginBottom: 50 }}>
                    <ShieldAlert size={50} style={{ color: 'var(--accent-neon)', marginBottom: 20, display: 'inline' }} />
                    <h2 style={{ fontSize: 32, marginBottom: 15 }}>Strict Privacy <span className="neon-text">Guarantees</span></h2>
                    <p style={{ color: 'var(--text-dim)', maxWidth: 700, margin: '0 auto' }}>
                        Aucun accès n'est autorisé en dehors des métriques de performance CPU/RAM système.
                    </p>
                </div>

                <div className="responsive-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', gap: 20 }}>
                    {["Fichiers Personnels", "Historique Web", "Captures Caméra", "Frappes Clavier"].map((txt, i) => (
                        <div key={i} className="card-glass" style={{ padding: 25, textAlign: 'center', opacity: 0.4 }}>
                            <div style={{ textDecoration: 'line-through', fontSize: 12, fontWeight: 900, color: '#444' }}>{txt}</div>
                            <div className="neon-text" style={{ fontSize: 10, marginTop: 10 }}>SECURED BLOCK</div>
                        </div>
                    ))}
                </div>
            </motion.div>

            <div className="hero-actions" style={{ marginTop: 80, justifyContent: 'center' }}>
                <div className="card-glass" style={{ padding: '20px 40px', display: 'flex', alignItems: 'center', gap: 20 }}>
                    <Download size={24} className="neon-text" />
                    <div>
                        <div style={{ fontSize: 14, fontWeight: 900 }}>Active Node Hub V2.1</div>
                        <div style={{ fontSize: 10, color: '#555' }}>SHA-256: 4A7B...9E21</div>
                    </div>
                </div>
                <button className="btn-wow" style={{ padding: '0 40px' }}>Contact support</button>
            </div>
        </motion.div>
    );
};

export default Documentation;
