# MySQL Installation in CVM

## Install MySQL server

```bash
sudo apt update
sudo apt install mysql-server -y
```

## Secure MySQL (optional but recommended)

```bash
sudo mysql_secure_installation
```

It will ask you:

    Set root password → Yes

    Remove anonymous users → Yes

    Disallow remote root login → Yes

    Remove test database → Yes

## Check if mysql is running

```bash
sudo systemctl status mysql
```

## If it's not running:

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

## Login to mysql

```bash
sudo mysql -u root -p
```

## Install Python Tools

```bash
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
```

#### This is only required before installing mysqlclient, not Django or MySQL itself.

## Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Django

```bash
pip install django
```

## Install MySQL Driver for Django

```bash
pip install mysqlclient
```

#### Note: If you are using UV environment manager

## Create a Virtual Environment

```bash
uv venv
source .venv/bin/activate
```

## Install Django

```bash
uv add Django
```

## Install MySQL Driver for Django

```bash
uv add mysqlclient
```