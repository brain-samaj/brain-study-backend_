"""
Brain Study Backend Pre-Deployment Checker

Validates the backend before deployment.
Compatible with pyproject.toml projects.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"

errors: list[dict[str, str]] = []
warnings: list[str] = []


def check(name: str, fn):
    print(f"\nChecking: {name}")
    try:
        fn()
        print(f"{PASS} {name}")
    except Exception as e:
        print(f"{FAIL} {name}")
        print(e)
        errors.append(
            {
                "check": name,
                "error": str(e),
            }
        )


def python_version():
    print(sys.version)


def required_files():
    required = [
        "pyproject.toml",
        "app/main.py",
        "app/core/config.py",
        "app/database/base.py",
        "app/database/session.py",
    ]

    for file in required:
        if not Path(file).exists():
            raise FileNotFoundError(f"Missing {file}")


def dependencies():
    packages = [
        "fastapi",
        "sqlalchemy",
        "uvicorn",
        "pydantic",
    ]

    for package in packages:
        importlib.import_module(package)


def imports():
    modules = [
        "app.main",
        "app.database.base",
        "app.database.session",
        "app.ai.analyzers.models",
    ]

    for module in modules:
        importlib.import_module(module)


def fastapi_startup():
    from app.main import app

    if app is None:
        raise RuntimeError("FastAPI application not found.")


def routes():
    from app.main import app

    registered = []

    for route in app.routes:
        path = getattr(route, "path", None)

        if path:
            registered.append(path)

    if not registered:
        raise RuntimeError("No API routes registered.")

    print(f"Found {len(registered)} routes.")


def environment():
    required = [
        "DATABASE_URL",
    ]

    for key in required:
        if not os.getenv(key):
            warnings.append(f"{key} missing")


def database():
    from app.database.session import engine

    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")


def models():
    importlib.import_module("app.database.models")


def main():
    print(
        """
==================================
Brain Study Deployment Checker
==================================
"""
    )

    checks = [
        ("Python version", python_version),
        ("Required files", required_files),
        ("Dependencies", dependencies),
        ("Module imports", imports),
        ("FastAPI startup", fastapi_startup),
        ("API routes", routes),
        ("Environment", environment),
        ("Database connection", database),
        ("Database models", models),
    ]

    for name, fn in checks:
        check(name, fn)

    print(
        """
==============================
Deployment Report
==============================
"""
    )

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"{WARN} {warning}")

    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"{FAIL} {error['check']}")
            print(f"    {error['error']}")
        sys.exit(1)

    print(f"\n{PASS} Backend looks ready for deployment.")


if __name__ == "__main__":
    main()
