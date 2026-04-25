import React, { useState } from 'react';

export default function LoginPage({ onLogin }: { onLogin: (token: string) => void }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const res = await fetch('http://vc-uy1.npe-techs.com/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });
            if (res.ok) {
                const data = await res.json();
                onLogin(data.access_token);
            } else {
                setError('Invalid credentials. Remember, this is for research admins only.');
            }
        } catch (err) {
            setError('Connection failure.');
        }
    };

    return (
        <div className="login-container glass">
            <h2 className="neon-text">Admin Login</h2>
            <p className="subtitle">M2 Recherche - VC Availability Prediction</p>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label>Username</label>
                    <input type="text" value={username} onChange={e => setUsername(e.target.value)} required />
                </div>
                <div className="input-group">
                    <label>Password</label>
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="btn-primary">Connect to Dashboard</button>
            </form>
        </div>
    );
}
