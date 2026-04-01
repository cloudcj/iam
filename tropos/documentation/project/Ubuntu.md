# Ubuntu Setup

## Install Prerequisites

### 1. Ensure Ubuntu is Fresh

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. List of Packages to be installed

1. `python3`
2. `python3-pip`
3. `python3-venv`
4. `build-essential`
5. `default-libmysqlclient-dev`
6. `git`
7. `mysql-server`
8. `nginx`

```bash
sudo apt install -y python3 python3-pip python3-venv build-essential default-libmysqlclient-dev git mysql-server nginx
```

### 3. Install UV on the Ubuntu Operating System

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

#### Add UV to Path

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Check if UV is installed

```bash
uv --version
```

## [Optional] WSL/Ubuntu Setup
```bash
```

## 4. Clone Repository from Git

#### 1. `Proceed to the root directory`

```bash
cd
```

#### 2. `Create a projects folder`
```bash
mkdir projects
```

#### 3. `Proceed to the projects folder`
```bash
cd projects
```

#### 4. `Create a Token from your Github Settings with appropriate permissions`

#### 5. `Clone the repository`
```bash
git clone https://<your-token>@github.com/cict-cloud/django-playground.git
```
<your-token-here>
> Replace the `<your-token>` with your token