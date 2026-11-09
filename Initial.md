# FastAPI – Python Environment Setup

This guide explains how to create a Python project, configure a virtual environment, activate it, install FastAPI and Uvicorn, and manage project dependencies.

## 1. Create a Project Directory

First, create a directory for your FastAPI project.

```bash
mkdir FastAPI
```

**Explanation:**
- `mkdir` stands for *Make Directory*.
- It creates a new folder named `FastAPI`.
- This folder will contain all your project-related files.

Navigate into the newly created directory:

```bash
cd FastAPI
```

**Explanation:**
- `cd` stands for *Change Directory*.
- It moves your terminal's current working location into the `FastAPI` folder.
- All subsequent commands will execute inside this directory.

## 2. Create a Python Virtual Environment

Create a virtual environment using Python:

```bash
python3 -m venv fastapienv
```

**Explanation:**

- `python3`: Executes Python 3.
- `-m`: Runs a Python module as a script.
- `venv`: Python's built-in module for creating virtual environments.
- `fastapienv`: Name of the virtual environment directory.

After executing this command, Python creates a folder named `fastapienv` inside your project directory.

**Project structure:**

```text
FastAPI/
│
└── fastapienv/
    ├── bin/
    ├── include/
    ├── lib/
    └── pyvenv.cfg
```

**Why do we need a virtual environment?**

A virtual environment provides an isolated Python environment for your project.

For example:
- Project A might require FastAPI version 0.100.
- Project B might require FastAPI version 0.115.

Without virtual environments, dependencies installed globally can conflict with each other.

Using a virtual environment ensures that each project maintains its own dependencies without affecting other Python projects.

## 3. Activate the Virtual Environment

To activate the virtual environment on macOS or Linux, execute:

```bash
source fastapienv/bin/activate
```

**Explanation:**

- `source`: Executes a script in the current shell session.
- `fastapienv/bin/activate`: Activation script inside the virtual environment.

Once activated, you will see the environment name in your terminal.

Example:

```bash
(fastapienv) username@machine FastAPI %
```

The `(fastapienv)` prefix indicates that your virtual environment is active.

**Important:** Always activate your virtual environment before installing dependencies or running your FastAPI project.

## 4. Check Installed Dependencies

To see the Python packages installed in your active environment:

```bash
pip list
```

**Explanation:**

- `pip` is Python's package installer.
- `list` displays the installed Python packages and their versions.

Example output:

```text
Package    Version
-----------------------
pip              25.x
```

Initially, you will mostly see `pip` and possibly a few environment-related packages.

After installing FastAPI and Uvicorn, they will also appear in this list.

## 5. Install FastAPI

Install FastAPI using pip:

```bash
pip install fastapi
```

**What is FastAPI?**

FastAPI is a modern Python web framework used to build APIs and backend applications.

Key features:
- High performance.
- Easy-to-write API endpoints.
- Automatic request validation.
- Built-in support for Python type hints.
- Automatic interactive API documentation.
- Support for asynchronous programming using `async` and `await`.

Example use cases:
- Building REST APIs.
- Creating backend services.
- Developing microservices.
- Connecting frontend applications (React, Next.js) with Python backends.

## 6. Install Uvicorn

Install Uvicorn with its standard dependencies:

```bash
pip install "uvicorn[standard]"
```

**What is Uvicorn?**

Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server.

It is responsible for running your FastAPI application and handling incoming HTTP requests.

**Why do we need Uvicorn?**

FastAPI is the framework used to write your API logic, whereas Uvicorn is the server that runs the application.

Think of it this way:

- FastAPI → Defines API routes and handles application logic.
- Uvicorn → Runs the application and listens for incoming requests.

**Why use `[standard]`?**

The `[standard]` option installs additional recommended dependencies that improve Uvicorn's functionality, such as performance optimizations and support for features like automatic reloading.

## 7. Verify Installed Dependencies

After installing FastAPI and Uvicorn, execute:

```bash
pip list
```

You should now see FastAPI, Uvicorn, and their required dependencies.

Example:

```text
Package       Version
------------- -------
annotated-doc ...
annotated-types ...
anyio         ...
fastapi       ...
idna          ...
pydantic      ...
starlette     ...
typing-inspection ...
typing-extensions ...
uvicorn       ...
```

The exact package versions and dependency list may vary.

## 8. Deactivate the Virtual Environment

Once you finish working on your project, you can deactivate the virtual environment:

```bash
deactivate
```

**Explanation:**

- `deactivate` exits the currently active virtual environment.
- Your terminal returns to the system's default Python environment.
- Packages installed inside the virtual environment remain available there, but are no longer active in your current shell session.

To work on the project again, activate it:

```bash
source fastapienv/bin/activate
```

## 9. Complete Setup – All Commands Together

For quick reference, here are all the commands in execution order:

```bash
# 1. Create project directory
mkdir FastAPI

# 2. Navigate into the project
cd FastAPI

# 3. Create virtual environment
python3 -m venv fastapienv

# 4. Activate virtual environment
source fastapienv/bin/activate

# 5. Install FastAPI
pip install fastapi

# 6. Install Uvicorn
pip install "uvicorn[standard]"

# 7. Verify installed dependencies
pip list

# 8. Deactivate virtual environment (when finished)
deactivate
```

## 10. Useful Commands – Quick Reference

| Command | Purpose |
|---|---|
| `mkdir FastAPI` | Create a project directory |
| `cd FastAPI` | Navigate into the project |
| `python3 --version` | Check Python version |
| `python3 -m venv fastapienv` | Create virtual environment |
| `source fastapienv/bin/activate` | Activate virtual environment |
| `pip list` | List installed packages |
| `pip install fastapi` | Install FastAPI |
| `pip install "uvicorn[standard]"` | Install Uvicorn with standard dependencies |
| `pip show fastapi` | Display FastAPI package details |
| `pip freeze` | Display installed dependencies with exact versions |
| `deactivate` | Deactivate virtual environment |

## 11. Important Best Practices

**1. Always activate the virtual environment**

Before installing packages or running your application, ensure that your virtual environment is active.

**2. Use a requirements.txt file**

Once your dependencies are installed, save them using:

```bash
pip freeze > requirements.txt
```

This creates a `requirements.txt` file containing the installed packages and their versions.

Example:

```text
fastapi==...
uvicorn==...
```

This is useful when sharing your project with other developers.

**3. Install dependencies from requirements.txt**

When setting up the same project on another machine:

```bash
pip install -r requirements.txt
```

This installs the dependencies listed in the file.

**4. Add your virtual environment to .gitignore**

Do not push your virtual environment folder to GitHub.

Create a `.gitignore` file:

```text
fastapienv/
__pycache__/
*.pyc
.env
```

The virtual environment can be recreated using the setup commands and `requirements.txt`.

---

## 12. Next Step

After completing the environment setup, you are ready to create your first FastAPI application.

