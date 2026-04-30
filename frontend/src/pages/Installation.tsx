// V3.2.1 - Cluster Ready
import { motion } from 'framer-motion';
import { CheckCircle2, ShieldAlert, Monitor, Terminal, Database, Activity, ArrowRight, ArrowLeft } from 'lucide-react';
import { useState } from 'react';
import { Copy, Terminal as TerminalIcon, Check } from 'lucide-react';

interface Step {
    title: string;
    icon: any;
    desc: string;
    details?: string[];
    action?: any;
    isCommand?: boolean;
    commands?: string[];
}

const windowsSteps: Step[] = [
    {
        title: "Démarrage & Pré-requis",
        icon: <ShieldAlert className="neon-text" size={32} />,
        desc: "Préparez votre environnement pour une contribution optimale à la recherche scientifique.",
        details: [
            "Assurez-vous d'être sur Windows 10/11 (64-bit).",
            "Niveaux de Consentement (GLOBECOM 2023) :",
            "1. Essentiel - 2. Système - 3. Recherche - 4. Feedback",
            "Par défaut : Niveau 3 (Modèles Recherche Anonymisés)."
        ]
    },
    {
        title: "Bootstrap de l'Agent",
        icon: <Database className="neon-text" size={32} />,
        desc: "Ouvrez PowerShell en tant qu'administrateur et exécutez ces commandes.",
        isCommand: true,
        commands: [
            "Set-ExecutionPolicy Bypass -Scope Process -Force",
            "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12",
            "Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://vc-uy1.npe-techs.com/install-windows.ps1'))"
        ]
    },
    {
        title: "Installation Silencieuse",
        icon: <Terminal className="neon-text" size={32} />,
        desc: "Exécutez le fichier téléchargé pour activer votre nœud dans le cluster.",
        details: [
            "Clic-droit sur 'vc-agent-windows.exe'.",
            "Sélectionnez 'Exécuter en tant qu'administrateur'.",
            "Indispensable pour l'installation du Service de Persistance."
        ]
    },
    {
        title: "Sécurité & Confiance",
        icon: <ShieldAlert className="neon-text" size={32} />,
        desc: "Note sur l'avertissement de sécurité Windows (SmartScreen).",
        details: [
            "L'agent est un prototype de recherche non signé numériquement.",
            "Windows affichera 'Éditeur inconnu' : c'est normal.",
            "Cliquez sur 'Plus d'infos' puis 'Exécuter quand même'.",
            "Cette étape n'arrive qu'une seule fois au premier lancement."
        ]
    },
    {
        title: "Vérification de la Persistance",
        icon: <CheckCircle2 className="neon-text" size={32} />,
        desc: "Le système est désormais autonome et résistant aux redémarrages.",
        details: [
            "L'agent s'installe comme un 'Service Système' Windows.",
            "Il se relancera seul dès le démarrage (Boot), même sans login.",
            "Suivez votre contribution en direct sur le Dashboard."
        ]
    }
];

const linuxSteps: Step[] = [
    {
        title: "Environnement de Recherche",
        icon: <TerminalIcon className="neon-text" size={32} />,
        desc: "L'agent Linux est conçu pour fonctionner nativement sous Ubuntu, Debian et Kali.",
        details: [
            "Compatible Glibc 2.31+ (Ubuntu 20.04+).",
            "Nécessite Python 3.10 ou supérieur.",
            "Installation via script de bootstrap sécurisé."
        ]
    },
    {
        title: "Bootstrap de l'Agent",
        icon: <Database className="neon-text" size={32} />,
        desc: "Copiez et collez ces 3 commandes pour activer votre nœud immédiatement.",
        isCommand: true,
        commands: [
            "wget -O install-vc.sh https://vc-uy1.npe-techs.com/install-linux.sh",
            "chmod +x install-vc.sh",
            "./install-vc.sh"
        ]
    },
    {
        title: "Activation en Arrière-plan",
        icon: <Activity className="neon-text" size={32} />,
        desc: "Une fois lancé, l'agent se détache automatiquement pour ne pas encombrer votre terminal.",
        details: [
            "Support natif de systemd pour la persistance.",
            "Vérification via : systemctl --user status vc-agent",
            "Auto-update intégré lors de chaque démarrage."
        ]
    }
];

export default function InstallationPage() {
    const [currentStep, setCurrentStep] = useState(0);
    const [os, setOs] = useState<'windows' | 'linux'>('windows');
    const [copied, setCopied] = useState(false);

    const steps = os === 'windows' ? windowsSteps : linuxSteps;

    const copyAll = () => {
        const currentSteps = os === 'windows' ? windowsSteps : linuxSteps;
        const cmdStep = currentSteps.find(s => s.isCommand);
        const cmds = cmdStep?.commands?.join('\n') || '';
        navigator.clipboard.writeText(cmds);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <motion.section
            className="page-content"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ padding: '0 40px' }}
        >
            <div style={{ textAlign: 'center', marginBottom: 50 }}>
                <h2 className="section-title">Setup Center : <span className="neon-text">{os === 'windows' ? 'Windows' : 'Linux'} Edition</span></h2>
                <p style={{ color: '#888', fontSize: 18 }}>Guide de déploiement pour les nœuds de recherche scientifique</p>

                {/* OS Toggle */}
                <div style={{ display: 'flex', justifyContent: 'center', gap: 20, marginTop: 30 }}>
                    <button
                        className={os === 'windows' ? 'btn-wow' : 'btn-outline'}
                        onClick={() => { setOs('windows'); setCurrentStep(0); }}
                        style={{ width: 180 }}
                    >
                        <Monitor size={18} style={{ marginRight: 8 }} /> Windows
                    </button>
                    <button
                        className={os === 'linux' ? 'btn-wow' : 'btn-outline'}
                        onClick={() => { setOs('linux'); setCurrentStep(0); }}
                        style={{ width: 180 }}
                    >
                        <TerminalIcon size={18} style={{ marginRight: 8 }} /> Linux
                    </button>
                </div>
            </div>

            <div className="installation-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 40, minHeight: 500 }}>
                {/* Steps Sidebar */}
                <div className="card-glass" style={{ padding: 20 }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 15 }}>
                        {steps.map((step, idx) => (
                            <div
                                key={idx}
                                onClick={() => setCurrentStep(idx)}
                                style={{
                                    padding: '15px 20px',
                                    borderRadius: 12,
                                    cursor: 'pointer',
                                    background: idx === currentStep ? 'rgba(204, 255, 0, 0.1)' : 'transparent',
                                    border: idx === currentStep ? '1px solid var(--accent-neon)' : '1px solid transparent',
                                    transition: 'all 0.3s ease'
                                }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                                    <span style={{ fontSize: 14, fontWeight: 'bold', color: idx === currentStep ? 'var(--accent-neon)' : '#555' }}>0{idx + 1}</span>
                                    <span style={{ fontSize: 15, fontWeight: 500, color: idx === currentStep ? '#fff' : '#888' }}>{step.title}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Main Step Content */}
                <div className="card-glass" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <motion.div
                        key={currentStep}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.4 }}
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginBottom: 30 }}>
                            <div className="icon-glow" style={{ padding: 20, borderRadius: '50%', background: 'rgba(204, 255, 0, 0.05)' }}>
                                {steps[currentStep].icon}
                            </div>
                            <h3 style={{ fontSize: 28 }}>{steps[currentStep].title}</h3>
                        </div>

                        <p style={{ fontSize: 19, color: '#ccc', marginBottom: 40, borderLeft: '4px solid var(--accent-neon)', paddingLeft: 20 }}>
                            {steps[currentStep].desc}
                        </p>

                        <div className="step-details" style={{ marginBottom: 40 }}>
                            {steps[currentStep].isCommand ? (
                                <div className="terminal-block" style={{
                                    background: '#0a0a0a',
                                    padding: '25px',
                                    borderRadius: '12px',
                                    border: '1px solid #333',
                                    position: 'relative'
                                }}>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontFamily: 'monospace', color: 'var(--accent-neon)' }}>
                                        {steps[currentStep].commands?.map((cmd: string, cIdx: number) => (
                                            <div key={cIdx} style={{ display: 'flex', gap: 15 }}>
                                                <span style={{ opacity: 0.3 }}>$</span>
                                                <span>{cmd}</span>
                                            </div>
                                        ))}
                                    </div>
                                    <button
                                        className="btn-wow"
                                        onClick={copyAll}
                                        style={{
                                            position: 'absolute',
                                            top: 15,
                                            right: 15,
                                            padding: '8px 15px',
                                            fontSize: 12,
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: 6
                                        }}
                                    >
                                        {copied ? <Check size={14} /> : <Copy size={14} />}
                                        {copied ? "Copié !" : "Tout Copier"}
                                    </button>
                                </div>
                            ) : (
                                steps[currentStep].details?.map((detail, dIdx) => (
                                    <div key={dIdx} style={{ display: 'flex', alignItems: 'flex-start', gap: 10, marginBottom: 15, color: '#aaa' }}>
                                        <div style={{ marginTop: 6, width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-neon)' }} />
                                        <span>{detail}</span>
                                    </div>
                                ))
                            )}
                            {steps[currentStep].action}
                        </div>
                    </motion.div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #222', paddingTop: 20 }}>
                        <button
                            className="btn-outline"
                            disabled={currentStep === 0}
                            onClick={() => setCurrentStep(prev => prev - 1)}
                            style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: currentStep === 0 ? 0.3 : 1 }}
                        >
                            <ArrowLeft size={16} /> Précédent
                        </button>
                        <button
                            className="btn-wow"
                            disabled={currentStep === steps.length - 1}
                            onClick={() => setCurrentStep(prev => prev + 1)}
                            style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: currentStep === steps.length - 1 ? 0.3 : 1 }}
                        >
                            {currentStep === steps.length - 1 ? "Configuration Terminée" : "Étape Suivante"} <ArrowRight size={16} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Visual Decorative elements */}
            <div style={{ marginTop: 100, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 30 }}>
                <div className="card-glass" style={{ textAlign: 'center', padding: 30 }}>
                    <Monitor className="neon-text" style={{ marginBottom: 15 }} />
                    <h5>Natif & Frugal</h5>
                    <p style={{ fontSize: 13, opacity: 0.6 }}>Optimisé par PyInstaller pour une empreinte RAM minimale ( \u003c 10MB ).</p>
                </div>
                <div className="card-glass" style={{ textAlign: 'center', padding: 30 }}>
                    <Activity className="neon-text" style={{ marginBottom: 15 }} />
                    <h5>Télémétrie 5 min</h5>
                    <p style={{ fontSize: 13, opacity: 0.6 }}>Collecte périodique sans impact sur les performances de vos tâches personnelles.</p>
                </div>
                <div className="card-glass" style={{ textAlign: 'center', padding: 30 }}>
                    <Database className="neon-text" style={{ marginBottom: 15 }} />
                    <h5>Persistance Totale</h5>
                    <p style={{ fontSize: 13, opacity: 0.6 }}>Résistance logicielle aux coupures de courant et aux redémarrages système.</p>
                </div>
            </div>
        </motion.section>
    );
}
