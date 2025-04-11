#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path


def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)
    print(f"Created: {path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: create-fastapi-app <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]
    target_dir = Path(os.getcwd()) / project_name

    # Check if directory exists
    if target_dir.exists():
        reply = input(f"Directory {project_name} already exists. Overwrite? (y/n): ")
        if reply.lower() != "y":
            print("Aborted.")
            sys.exit(1)
        shutil.rmtree(target_dir)

    # Create main structure
    folders = [
        "",
        "app",
        "app/api",
        "app/api/endpoints",
        "app/core",
        "app/db",
        "app/models",
        "app/schemas",
        "app/utils",
        "tests",
    ]

    for folder in folders:
        folder_path = target_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        if folder.startswith("app"):
            create_file(folder_path / "__init__.py", "")

    # Create basic files
    create_file(target_dir / "app" / "main.py", MAIN_PY)
    create_file(target_dir / "app" / "api" / "api.py", API_PY)
    create_file(target_dir / "app" / "core" / "config.py", CONFIG_PY)
    create_file(target_dir / "app" / "db" / "session.py", DB_SESSION_PY)
    create_file(target_dir / ".env", ENV_FILE)
    create_file(target_dir / "requirements.txt", REQUIREMENTS_TXT)
    create_file(target_dir / "README.md", README_MD.format(project_name=project_name))

    print(f"\n✅ FastAPI project created in {project_name}/")
    print(f"\nTo start your app:")
    print(f"  cd {project_name}")
    print(f"  pip install -r requirements.txt")
    print(f"  uvicorn app.main:app --reload\n")


# Templates
MAIN_PY = """from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}
"""

API_PY = """from fastapi import APIRouter

api_router = APIRouter()

# Include your routers here
# from app.api.endpoints import items
# api_router.include_router(items.router, prefix="/items", tags=["items"])
"""

CONFIG_PY = """from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    DESCRIPTION: str = "FastAPI application"
    VERSION: str = "0.1.1"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: Optional[str] = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

    class Config:
        env_file = ".env"

settings = Settings()
"""

DB_SESSION_PY = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

ENV_FILE = """PROJECT_NAME="FastAPI App"
DESCRIPTION="FastAPI application"
VERSION="0.1.1"
DATABASE_URL="sqlite:///./app.db"
"""

REQUIREMENTS_TXT = """fastapi>=0.95.0
uvicorn>=0.22.0
sqlalchemy>=2.0.0
pydantic>=1.10.0
python-dotenv>=1.0.0
"""

README_MD = """# {project_name}

## Installation

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the API documentation.
"""

if __name__ == "__main__":
    main()
