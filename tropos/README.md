# Project Tropos: Converge Cloud Data Center Inventory System for Backend

A Django-based backend API system for managing cloud data center inventory and infrastructure resources. Features comprehensive tracking of equipment, assets, and components with Redis integration for optimized caching and session management. Built with modern Python development practices using UV package manager for fast dependency resolution and streamlined development workflows. Includes Docker containerization for Redis services and automated startup scripts for seamless deployment and development environment setup.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for Redis)
- Git

## Quick Start

### 1. Install UV Package Manager

Choose one of the following methods:

**Via pip:**
```bash
pip install uv
```

**Via curl (recommended):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Set Up Virtual Environment

Create a new virtual environment using UV:
```bash
uv venv
```

### 3. Activate Virtual Environment

**On Windows:**
```bash
source .venv/Scripts/activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Sync Dependencies

Once the virtual environment is activated, sync all project dependencies:
```bash
uv sync
```

This will install all dependencies defined in your `pyproject.toml` or `requirements.txt` file.

## Running the Application

### Option 1: Using the Start Script (Recommended)

We've provided a convenient bash script that handles the complete startup process:

```bash
./start.sh
```

This script will:
1. Start Redis using Docker Compose
2. Run the Django development server with `python manage.py runserver`

### Option 2: Manual Setup

If you prefer to run services manually:

1. **Start Redis:**
   ```bash
   docker-compose up -d
   ```

2. **Run the Django server:**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
.
├── .venv/                 # Virtual environment (created by uv venv)
├── documentation/
│   ├── UV.md              # Detailed UV package manager documentation
│   └── docker/            # Docker-related documentation        
├── docker-compose.yml     # Redis container configuration
├── start.sh               # Executable startup script
├── pyproject.toml         # Project dependencies and configuration
└── manage.py              # Django management script
```

## Documentation

For more detailed information, check out the documentation folder:

- **UV Package Manager**: See `documentation/UV.md` for comprehensive UV usage and features
- **Docker Setup**: Check the `documentation/Docker.md` folder for Docker-related configurations and troubleshooting

## Why UV?

UV is a fast Python package installer and resolver, written in Rust. Key benefits include:

- ⚡ **Speed**: Significantly faster than pip
- 🔒 **Reliability**: Better dependency resolution
- 🎯 **Modern**: Built for modern Python development workflows
- 🔄 **Compatibility**: Works with existing pip and PyPI ecosystem

## Troubleshooting

### Virtual Environment Issues

If you encounter issues with the virtual environment:
```bash
# Remove existing venv
rm -rf .venv

# Create new venv
uv venv

# Reactivate and sync
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
uv sync
```

### Docker Issues

If Redis container fails to start:
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs

# Restart services
docker-compose restart
```