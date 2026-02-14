# scanner/constants.py

# Structured project detection signals grouped by ecosystem
PROJECT_SIGNALS = {
    "javascript": {
        "package.json",
        "tsconfig.json",
        "next.config.js",
        "vite.config.js",
        "angular.json",
    },
    "python": {
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "Pipfile",
        "environment.yml",
    },
    "java": {
        "pom.xml",
        "build.gradle",
        "settings.gradle",
    },
    "dotnet": {
        ".sln",
        ".csproj",
    },
    "go": {
        "go.mod",
    },
    "rust": {
        "Cargo.toml",
    },
    "php": {
        "composer.json",
    },
    "mobile": {
        "android",
        "ios",
        "app.json",
        "pubspec.yaml",   # Flutter
    },
    "data": {
        "notebook.ipynb",
        ".ipynb_checkpoints",
    },
    "general": {
        "Makefile",
        "Dockerfile",
    },
}

# Git is always strongest signal
GIT_SIGNAL = ".git"

# Folders to ignore during traversal
IGNORE_FOLDERS = {
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".cache",
    "venv",
    "__pycache__",
    ".next",
    ".idea",
    ".vscode",
    ".gradle",
    "target",
}

# Windows system folders to ignore
SYSTEM_IGNORE_FOLDERS = {
    "windows",
    "program files",
    "program files (x86)",
    "$recycle.bin",
    "system volume information",
}

# Maximum recursion depth
MAX_DEPTH = 4

# Status thresholds (days)
STATUS_THRESHOLDS = {
    "ACTIVE": 7,
    "WARM": 30,
    "COLD": 90,
}
