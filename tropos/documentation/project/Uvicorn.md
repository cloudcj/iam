'''bash
Path: /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon for Django project
After=network.target

[Service]
User=your_linux_user
Group=www-data
WorkingDirectory=/home/your_linux_user/yourproject
ExecStart=/home/your_linux_user/yourproject/.venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/your_linux_user/yourproject/gunicorn.sock \
          yourproject.wsgi:application

[Install]
WantedBy=multi-user.target
'''

###
'''bash
/etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/home/your_linux_user/yourproject/gunicorn.sock

[Install]
WantedBy=sockets.target
'''

###
'''bash
/etc/nginx/sites-available/yourproject

server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/your_linux_user/yourproject;
    }

    location /media/ {
        root /home/your_linux_user/yourproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/your_linux_user/yourproject/gunicorn.sock;
    }
}
'''

'''bash
Enable it:

sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled
'''


'''bash
sudo systemctl daemon-reload

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

sudo systemctl start uvicorn
sudo systemctl enable uvicorn

sudo systemctl restart nginx
'''

'''bash
2️⃣ Gunicorn systemd (WSGI)
[Unit]
Description=Gunicorn daemon (WSGI)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/user/project
ExecStart=/home/user/project/.venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/user/project/gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target

3️⃣ Uvicorn systemd (ASGI)
[Unit]
Description=Uvicorn daemon (ASGI)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/user/project
ExecStart=/home/user/project/.venv/bin/uvicorn project.asgi:application \
          --uds /home/user/project/uvicorn.sock \
          --workers 4

[Install]
WantedBy=multi-user.target

4️⃣ Nginx configuration
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        root /home/user/project;
    }

    location /media/ {
        root /home/user/project;
    }

    # Async / WebSocket URLs go to Uvicorn
    location /ws/ {
        proxy_pass http://unix:/home/user/project/uvicorn.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Everything else goes to Gunicorn (WSGI)
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/project/gunicorn.sock;
    }
}
'''