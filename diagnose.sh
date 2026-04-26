#!/bin/bash
echo "--- VC-UY1 DIAGNOSTIC REPORT ---"
echo "Date: $(date)"

echo "1. Checking all listening ports..."
ss -tulpn

echo "2. Checking who is on port 80..."
lsof -i :80

echo "3. Checking Apache port configuration..."
grep -r "Listen" /etc/apache2/

echo "4. Checking for Traefik or Docker..."
ps aux | grep -E "traefik|docker" | grep -v grep

echo "4. Checking server logs..."
tail -n 20 server/server.log

echo "5. Checking Apache status..."
systemctl status apache2 | grep Active

echo "6. Checking if frontend/dist exists..."
ls -d frontend/dist && echo "Found" || echo "NOT FOUND"
