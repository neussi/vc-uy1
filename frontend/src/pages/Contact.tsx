import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Send, CheckCircle, AlertCircle, User, MessageSquare, Tag, ShieldCheck } from 'lucide-react';

const Contact = () => {
    const [formData, setFormData] = useState({ name: '', email: '', subject: '', message: '' });
    const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus('loading');
        try {
            const res = await fetch('/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            if (res.ok) {
                setStatus('success');
                setFormData({ name: '', email: '', subject: '', message: '' });
            } else {
                setStatus('error');
            }
        } catch (err) {
            setStatus('error');
        }
    };

    return (
        <motion.div
            className="page-content hero-section"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ paddingBottom: 100 }}
        >
            {/* Background Glow */}
            <div className="floating-glow" style={{ position: 'fixed', top: '20%', left: '10%', opacity: 0.15 }} />

            <motion.header
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
                style={{ marginBottom: 60 }}
            >
                <div className="neon-text" style={{ fontSize: 12, fontWeight: 900, letterSpacing: 4, textTransform: 'uppercase', marginBottom: 20 }}>
                    <ShieldCheck size={18} style={{ verticalAlign: 'middle', marginRight: 10 }} />
                    Research Support Terminal
                </div>
                <h1 className="section-title">Direct <span className="neon-text">Connection</span></h1>
                <p className="hero-subtitle" style={{ margin: '0 auto', fontSize: 20 }}>
                    Une question technique ou éthique ? Contactez directement <br /> l'équipe de recherche.
                </p>
            </motion.header>

            <div className="hero-grid" style={{ alignItems: 'flex-start' }}>
                <div className="contact-info space-y-6">
                    <motion.div
                        className="card-glass"
                        style={{ padding: 40 }}
                        initial={{ x: -30, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                    >
                        <Mail className="neon-text" size={48} style={{ marginBottom: 30 }} />
                        <h3 style={{ fontSize: 24, color: '#fff', marginBottom: 15 }}>Laboratory Email</h3>
                        <p style={{ color: 'var(--text-dim)', fontSize: 16, marginBottom: 20 }}>
                            Notre équipe surveille le cluster 24/7 pour assurer la stabilité des 5000+ nœuds.
                        </p>
                        <div className="neon-text" style={{ fontWeight: 900, fontSize: 18 }}>support.vc-uy1@npe-techs.com</div>
                    </motion.div>

                    <motion.div
                        className="card-glass"
                        style={{ padding: 40 }}
                        initial={{ x: -30, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.1 }}
                    >
                        <h3 style={{ fontSize: 20, color: '#fff', marginBottom: 15 }}>Institution</h3>
                        <p style={{ color: 'var(--text-dim)', fontSize: 14 }}>
                            Université de Yaoundé I<br />
                        </p>
                    </motion.div>
                </div>

                <motion.div
                    className="card-glass"
                    style={{ padding: 50, background: 'rgba(255,255,255,0.02)' }}
                    initial={{ x: 30, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                >
                    <form onSubmit={handleSubmit} style={{ width: '100%' }}>
                        <div className="guide-layout" style={{ gap: 30, marginBottom: 30, marginTop: 0 }}>
                            <div className="field-group">
                                <label style={{ display: 'block', fontSize: 11, fontWeight: 900, color: '#666', textTransform: 'uppercase', marginBottom: 10, letterSpacing: 1 }}>Nom Complet</label>
                                <div style={{ position: 'relative' }}>
                                    <User size={16} style={{ position: 'absolute', left: 20, top: 20, color: '#444' }} />
                                    <input
                                        required
                                        type="text"
                                        placeholder="Votre nom"
                                        style={{ paddingLeft: 50 }}
                                        className="input-futuristic"
                                        value={formData.name}
                                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="field-group">
                                <label style={{ display: 'block', fontSize: 11, fontWeight: 900, color: '#666', textTransform: 'uppercase', marginBottom: 10, letterSpacing: 1 }}>Email</label>
                                <div style={{ position: 'relative' }}>
                                    <Mail size={16} style={{ position: 'absolute', left: 20, top: 20, color: '#444' }} />
                                    <input
                                        required
                                        type="email"
                                        placeholder="votre@email.com"
                                        style={{ paddingLeft: 50 }}
                                        className="input-futuristic"
                                        value={formData.email}
                                        onChange={e => setFormData({ ...formData, email: e.target.value })}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="field-group" style={{ marginBottom: 30 }}>
                            <label style={{ display: 'block', fontSize: 11, fontWeight: 900, color: '#666', textTransform: 'uppercase', marginBottom: 10, letterSpacing: 1 }}>Sujet de la demande</label>
                            <div style={{ position: 'relative' }}>
                                <Tag size={16} style={{ position: 'absolute', left: 20, top: 20, color: '#444' }} />
                                <input
                                    required
                                    type="text"
                                    placeholder="Ex: Correction bug, Question éthique..."
                                    style={{ paddingLeft: 50 }}
                                    className="input-futuristic"
                                    value={formData.subject}
                                    onChange={e => setFormData({ ...formData, subject: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="field-group" style={{ marginBottom: 40 }}>
                            <label style={{ display: 'block', fontSize: 11, fontWeight: 900, color: '#666', textTransform: 'uppercase', marginBottom: 10, letterSpacing: 1 }}>Message</label>
                            <div style={{ position: 'relative' }}>
                                <MessageSquare size={16} style={{ position: 'absolute', left: 20, top: 20, color: '#444' }} />
                                <textarea
                                    required
                                    rows={5}
                                    placeholder="Détaillez votre demande pour un traitement rapide..."
                                    style={{ paddingLeft: 50 }}
                                    className="input-futuristic"
                                    value={formData.message}
                                    onChange={e => setFormData({ ...formData, message: e.target.value })}
                                />
                            </div>
                        </div>

                        <button
                            disabled={status === 'loading'}
                            className="btn-wow"
                            style={{ width: '100%', padding: '22px', fontSize: 16, fontWeight: 900, letterSpacing: 2 }}
                        >
                            {status === 'loading' ? (
                                <span className="animate-pulse">TRANSMISSION...</span>
                            ) : (
                                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 15 }}>
                                    ENVOYER LE MESSAGE <Send size={20} />
                                </span>
                            )}
                        </button>

                        {status === 'success' && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="card-glass"
                                style={{ marginTop: 20, padding: 20, borderColor: '#d4ff0055', textAlign: 'center', color: 'var(--accent-neon)' }}
                            >
                                <CheckCircle size={20} style={{ display: 'inline', marginRight: 10 }} /> Message transmis avec succès !
                            </motion.div>
                        )}

                        {status === 'error' && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="card-glass"
                                style={{ marginTop: 20, padding: 20, borderColor: '#ff5f5655', textAlign: 'center', color: '#ff5f56' }}
                            >
                                <AlertCircle size={20} style={{ display: 'inline', marginRight: 10 }} /> Échec de l'envoi. Veuillez vérifier votre connexion.
                            </motion.div>
                        )}
                    </form>
                </motion.div>
            </div>
        </motion.div>
    );
};

export default Contact;
