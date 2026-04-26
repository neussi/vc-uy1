#!/bin/bash
echo "--- VC-UY1 DIAGNOSTIC REPORT ---"
echo "Date: $(date)"

echo "1. Checking if port 76123 is listening..."
netstat -tulpn | grep 76123

echo "2. Checking for running gunicorn processes..."
ps aux | grep gunicorn | grep -v grep

echo "3. Testing local connectivity to backend..."
curl -I http://localhost:76123

echo "4. Checking server logs..."
tail -n 20 server/server.log

echo "5. Checking Apache status..."
systemctl status apache2 | grep Active

echo "6. Checking if frontend/dist exists..."
ls -d frontend/dist && echo "Found" || echo "NOT FOUND"
