# UV Python Manager Guide

UV is a modern Python package manager for managing project dependencies, virtual environments, and development workflows.

---

## 1. Basic Setup

### 1.1 Install UV

Install UV using Python's package manager `pip`:

```bash
pip install uv
```

### 1.2 Initialize a New Project

```bash
uv init my_project
```

* Creates a new project directory `my_project`.
* Generates `pyproject.toml` and `uv.lock` for dependency management.

### 1.3 Configure Virtual Environment

```bash
uv venv
```
* Creates a virtual environment using Python's latest version



#### [Optional] Configure Python version

```bash
uv config set python 3.11
```

* Sets the Python version for the project.
* Creates a virtual environment automatically using the specified Python version.

### 1.4 Activate Virtual Environment

```bash
source .venv/Scripts/activate
# or
source .venv/bin/activate
```

* Activates the project-specific virtual environment.

### 1.5 Deactivate Virtual Environment

```bash
deactivate
```

* Exits the UV shell and deactivates the environment.

---

## 2. Add a Package

### 2.1 Regular Dependency

```bash
uv add requests
```

* Adds the `requests` package to the project.
* Updates `pyproject.toml` and locks versions in `uv.lock`.

### 2.2 Development Dependency

```bash
uv add --dev pytest
```

* Adds `pytest` as a development dependency.

---

## 3. Remove a Package

```bash
uv remove requests
```

* Removes the package and updates `pyproject.toml` and `uv.lock`.

---

## 4. See the Dependency Tree

```bash
uv tree
```

* Displays a hierarchical view of installed dependencies.

---

## 5. Update Packages

```bash
uv update requests
```

* Updates the specified package to the latest version according to version constraints.

```bash
uv update --all
```

* Updates all project dependencies.

---

## 6. Install from `pyproject.toml`

```bash
uv sync
```

* Installs all dependencies exactly as specified in `pyproject.toml`.
* Ensures consistent environments across machines.

---

## 7. Additional Configuration Options


### Development vs Production

* Add packages with `--dev` for development-only dependencies.
* Default installs are production dependencies.

---

## 8. Recommended Workflow

1. `uv init` – create a new project.
2. `uv add <package>` – add dependencies.
3. `uv source .venv/bin/activate` – activate virtual environment.
4. `uv sync` – install dependencies on a new machine.
5. `uv update <package>` – keep dependencies up to date.
6. `uv remove <package>` – remove unneeded dependencies.
