

# SoulFetch

SoulFetch is a Python project compatible with Windows 11 and Linux (Debian).

## Structure
- `frontend/`: Graphical interface (PySide6, MVC, dark theme inspired by Burp Suite)
- `backend/`: API and business logic (FastAPI, Hexagonal architecture)
- `db/`: Local persistence (SQLite)
- `tests/`: Automated tests
- `.github/copilot-instructions.md`: Checklist and project rules

## Principles
- SOLID
- DRY
- KISS

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run backend: `python backend/main.py`
3. Run frontend: `python frontend/main.py`
4. Run tests: `pytest tests/`

## Compatibility
- Windows 11
- Linux (Debian)

## Documentation
Keep this file and `.github/copilot-instructions.md` up to date.