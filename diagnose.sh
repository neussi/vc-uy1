#!/bin/bash
echo "--- VC-UY1 DIAGNOSTIC REPORT ---"
echo "Date: $(date)"

echo "1. Checking all listening ports..."
ss -tulpn

echo "2. Checking who is on port 80..."
lsof -i :80

echo "3. Checking Apache port configuration..."
grep -r "Listen" /etc/apache2/

echo "5. Checking active Apache sites..."
ls -la /etc/apache2/sites-enabled/

echo "6. Reading Apache ports configuration..."
cat /etc/apache2/ports.conf

echo "7. Checking for other proxy configs (Nginx/Traefik)..."
ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo "No Nginx"
ls -la /etc/traefik/ 2>/dev/null || echo "No Traefik config at /etc/traefik"

echo "4. Checking server logs..."
tail -n 20 server/server.log

echo "5. Checking Apache status..."
systemctl status apache2 | grep Active

echo "6. Checking if frontend/dist exists..."
ls -d frontend/dist && echo "Found" || echo "NOT FOUND"
