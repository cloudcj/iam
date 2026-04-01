# Gunicorn Configuration

## 1. Gunicorn Config File

### 1. Add a `gunicorn.conf.py` in the root directory
```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"  # or "0.0.0.0:8000" for public access
workers = 17
accesslog = "-"
errorlog = "-"
```


### 2. Execute Gunicorn to host production server
```bash
gunicorn -c gunicorn.conf.py playground.wsgi:application
```


### 3. Create Gunicorn Service
'''bash
sudo nano /etc/systemd/system/gunicorn.service
'''

### gunicorn.service
'''nano
[Unit]
Description= #insert description
After=network.target

[Service]
User= #your user_name
Group=www-data
WorkingDirectory=/path/to/your-app \
ExecStart=/path/to/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/root/user/repository-name/gunicorn.sock \
    name-myapp.wsgi:application

[Install]
WantedBy=multi-user.target
'''


### 4. Create Gunicorn Socket
'''bash
sudo nano /etc/systemd/system/gunicorn.socket
'''

### gunicorn.socket
'''nano
[Unit]
Description= #insert description
After=network.target

[Socket]
ListenStream=/run/gunicorn.sock
SocketUser= #user_name
SocketGroup=www-data
SocketMode=0660

[Install]
WantedBy=sockets.target
'''


### 5. Start and Enable Gunicorn
'''bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
'''

### 5. Check Socket Permissions
'''bash
ls -l /home/user/root/gunicorn.sock
'''

### if permissions are incorrect:
'''bash
sudo chown user:www-data /home/user/root/gunicorn.sock
sudo chmod 660 /home/user/root/gunicorn.sock
'''
### for directory permissions:
'''bash
sudo chown -R user:user /home/user
sudo chmod 750 /home/user
sudo chmod 750 /home/user/root
'''


### 6. Checking for Nginx Error Logs
'''bash
sudo tail -n 20 /var/log/nginx/error.log
'''


### 7. Checking of gunincon status
'''bash
sudo systemctl status gunicorn
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn.service
'''


### 8. Configure Nginx
'''bash
sudo nano /etc/nginx/site-available/your-app
'''

### Nginx Configuration
'''bash
server {
    listen 80;
    server_name ; #your ip or domanin name

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forward-Proto $scheme;
    }
}
'''

### Enable site
'''bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
'''


### 8. When updating the code run this first to reload Gunicorn
'''bash
gunicorn --bind 0.0.0.0:8001 your-app.wsgi.application
sudo systemctl restart gunicorn
'''

