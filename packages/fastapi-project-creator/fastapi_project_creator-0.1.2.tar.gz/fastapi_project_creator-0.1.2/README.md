# FastAPI Generator

A simple CLI tool to generate FastAPI project structure, inspired because I haven't found a way to quickly create the folder structure.

## Installation

```bash
# Install from PyPI
pip install fastapi-project-creator

# Or install directly from GitHub
pip install git+https://github.com/raihanhd12/fastapi-project-creator.git
```

## Usage

```bash
# Create a new FastAPI project
create-fastapi-app my-project-name
```

This will generate a complete FastAPI project structure with the following features:

- Organized directory structure following best practices
- Pre-configured API router setup
- Database connection with SQLAlchemy
- Environment variable configuration
- Ready-to-use project structure

## Project Structure

```
my-project-name/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── api.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── tests/
├── .env
├── requirements.txt
└── README.md
```

## Getting Started

After creating your project:

```bash
cd my-project-name
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://localhost:8000 in your browser.

## Development

To contribute to this project:

1. Clone the repository

```bash
git clone https://github.com/raihanhd12/fastapi-project-creator.git
cd fastapi-project-creator
```

2. Install in development mode

```bash
pip install -e .
```

3. Make your changes and test them with

```bash
create-fastapi-app test-project
```

## License

MIT
