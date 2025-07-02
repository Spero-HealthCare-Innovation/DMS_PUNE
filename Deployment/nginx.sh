#!/bin/bash

NGINX_CONF_PATH="/var/www/html/DMS_project/DMS_PUNE/Deployment/nginx_proxy"
LOG_PATH="/var/www/html/DMS_project/DMS_PUNE/logs"

echo "========= Starting NGINX Configuration ========="

# Django NGINX Config
if [ -f "/etc/nginx/sites-available/dms_django_6003.conf" ]; then
    echo "[✓] dms_django_6003.conf already present."
else
    echo "[+] Copying dms_django_6003.conf..."
    sudo cp -f "$NGINX_CONF_PATH/dms_django_6003.conf" /etc/nginx/sites-available/
    sudo ln -sf /etc/nginx/sites-available/dms_django_6003.conf /etc/nginx/sites-enabled/
    echo "[✓] Copied and enabled dms_django_6003.conf"
fi

# React NGINX Config
if [ -f "/etc/nginx/sites-available/dms_goa_react_7000.conf" ]; then
    echo "[✓] dms_goa_react_7000.conf already present."
else
    echo "[+] Copying dms_goa_react_7000.conf..."
    sudo cp -f "$NGINX_CONF_PATH/dms_goa_react_7000.conf" /etc/nginx/sites-available/
    sudo ln -sf /etc/nginx/sites-available/dms_goa_react_7000.conf /etc/nginx/sites-enabled/
    echo "[✓] Copied and enabled dms_goa_react_7000.conf"
fi

# Reload and restart nginx
echo "[~] Testing NGINX configuration..."
sudo nginx -t && {
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    echo "[✓] NGINX restarted and enabled"
} || {
    echo "[✗] NGINX config test failed. Please check errors above."
}

sudo chmod 664 /var/www/html/DMS_project/DMS_PUNE/logs/django_logentry.log 
sudo chown jenkins:www-data /var/www/html/DMS_project/DMS_PUNE/logs/django_logentry.log   

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart dms_uvicorn_fastapi
sudo systemctl status dms_uvicorn_fastapi

echo "========= NGINX Configuration Completed ========="
