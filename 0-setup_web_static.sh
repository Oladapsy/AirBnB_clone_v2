#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static

sudo apt-get update -y
sudo apt-get install -y nginx
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "<html>
  <head>
    </head>
      <body>
          Holberton School
	    </body>
	    </html>" > /data/web_static/releases/test/index.html
rm -rf /data/web_static/current
ln -s /data/web_static/current /data/web_static/releases/test/
sudo chown -R uubuntu:ubuntu /data/

#update Nginx configuration
echo "server {

	location /hbnb_static {
		alias /data/web_static/current/;
	}

}" >> /etc/nginx/sites-available/default

sudo nginx -s reload
sudo service nginx restart
