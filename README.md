# VC-UY1: Volunteer Computing Availability Prediction

Master 2 Recherche Informatique - University of Yaoundé 1
**Option**: Systems and Networks
**Director**: Dr. ADAMOU HAMZA

---

## 🚀 Overview
VC-UY1 is a specialized data collection and prediction platform designed for research into machine availability in resource-constrained environments (specifically focused on West African power grid instability patterns).

## 🛠 Features
- **Intelligent Local Agent**: Python service with hardware monitoring and heartbeat-based power-cut detection.
- **Central Server**: FastAPI-based REST API with PostgreSQL/SQLite support.
- **Research Portal**: High-end UI with admin dashboard, research documentation, and data export (CSV/ZIP).
- **SSL Ready**: Pre-configured for Let's Encrypt / Certbot.

## 📦 Project Structure
- `/agent`: Python background collector.
- `/server`: FastAPI backend and database models.
- `/frontend`: Vite/React/TypeScript production-built portal.
- `/docs`: Technical specifications and research context.

## 🚢 Deployment Guide (VPS)

### 1. Prerequisites
- Python 3.10+
- Apache 2.4+
- Certbot (for SSL)

### 2. Manual SSL Setup
On the server, run:
```bash
sudo apt update
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d vc-uy1.npe-techs.com
```

### 3. Service Management
To start the backend server on port 76123:
```bash
chmod +x start_server.sh
./start_server.sh
```

### 4. Admin Credentials
- **Username**: `admin`
- **Password**: `vc-uy1-recherche`

## 📊 Data Collection
Data is collected every 5 minutes and can be exported from the dashboard for model training (GRU / TinyML).
