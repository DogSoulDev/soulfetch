


# SoulFetch

SoulFetch is a modern, robust API client inspired by Postman, Apidog, and Burp Suite. It is designed for Windows 11 and Linux (Debian), with a professional dark theme and advanced features for API development, testing, and automation.

## Directory Structure

```
├── backend/                # FastAPI backend (Hexagonal architecture)
│   ├── adapters/           # Routers: collections, history, environments, request_exec, mock_server
│   ├── application/
│   ├── domain/
│   └── main.py
├── frontend/               # PySide6 frontend (MVC)
│   ├── controllers/
│   ├── models/
│   ├── views/
│   └── main.py
├── db/                     # SQLite database
│   └── soulfetch.db
├── tests/                  # Automated tests for all modules
├── assets/                 # Icons and static assets
│   └── soulfetch_icon.png
├── .github/copilot-instructions.md # Architecture and execution guidelines
├── README.md
└── (no requirements.txt found)
```

## Architecture
- **Frontend:** PySide6, MVC pattern, dark theme inspired by Burp Suite, UX details from Postman/Apidog
- **Backend:** FastAPI, Hexagonal architecture, modular routers
- **Persistence:** SQLite local database
- **Testing:** Full test suite in `tests/` (pytest)

## Main Features
- Request builder (dynamic endpoint, all HTTP methods)
- Response viewer (raw, formatted, diff)
- Terminal/log panel con scroll y expansión automática para visualizar toda la información de logs y respuestas
- History and collections (import/export)
- Environment variable manager (preview/edit)
- Auth tab (advanced authentication)
- Mock server
- Test runner
- Flow designer
- Plugin manager (scripting, extensions)
- Scheduler/monitor
- Gemini tab (AI features)
- Privacy mode
- Advanced response visualization
- Contextual menus, global variables, folders

## Principles
- SOLID, DRY, KISS
- Professional UX: clear status, error, response, and logs in all panels
- Modular, maintainable, and extensible code

## Usage
1. **Install dependencies:** (No requirements.txt found; ensure PySide6, FastAPI, requests, uvicorn, pydantic are installed)
2. **Run backend:** `python backend/main.py`
3. **Run frontend:** `python frontend/main.py`
4. **Run tests:** `pytest --disable-warnings --tb=short --cov=frontend --cov=backend --cov-report=term-missing`
5. **Explore all tabs:** Request, History, Test Runner, Mock Server, Flow Designer, Environments, Auth, Response Visualizer, Scheduler/Monitor, Plugins/Scripting, Gemini

## Compatibility
- Windows 11
- Linux (Debian)

## Documentation & Contribution
- Keep this README and `.github/copilot-instructions.md` up to date
- See `.github/copilot-instructions.md` for architecture, principles, and execution guidelines
- All code follows SOLID, DRY, KISS, and professional UX standards

## Status
All tests pass. No code errors. Full coverage for controllers, backend, mocks, and main features. Ready for further development, packaging, or deployment.