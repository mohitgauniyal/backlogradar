# scanner/constants.py

# Strong project detection signals
STRONG_SIGNALS = {
    ".git",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "composer.json",
    "pom.xml",
    "build.gradle",
    "Makefile",
    "Dockerfile",
    "tsconfig.json",
}

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
}

# Windows system folders to ignore
SYSTEM_IGNORE_FOLDERS = {
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "$Recycle.Bin",
    "System Volume Information",
}

# Maximum recursion depth
MAX_DEPTH = 4

# Status thresholds (days)
STATUS_THRESHOLDS = {
    "ACTIVE": 7,
    "WARM": 30,
    "COLD": 90,
}