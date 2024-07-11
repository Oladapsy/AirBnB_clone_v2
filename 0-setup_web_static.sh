#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static

sudo apt-get update -y
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo chown -R ubuntu:ubuntu /data/
echo "Holberton School" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

sudo printf %s "server {
    listen 80;
    listen [::]:80 default_server;

    add_header X-Served-By $HOSTNAME;

    root   /var/www/html;
    index  index.html index.htm;
    rewrite ^/redirect_me https://www.youtube.com/@cryptotechcoder permanent;

    location /hbnb_static {
        alias /data/web_static/current;
	index index.html index.htm;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" | sudo tee /etc/nginx/sites-available/default > /dev/null

sudo service nginx restart
