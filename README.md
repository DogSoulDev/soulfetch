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
└── requirements.txt        # Python dependencies (PySide6, FastAPI, requests, uvicorn, pydantic)
```

## Architecture
- **Frontend:** PySide6, MVC pattern, dark theme inspired by Burp Suite, UX details from Postman/Apidog
- **Backend:** FastAPI, Hexagonal architecture, modular routers
- **Persistence:** SQLite local database
- **Testing:** Full test suite in `tests/` (pytest)

## Main Features
 - Request builder (dynamic endpoint, all HTTP methods)
 - Response viewer (raw, formatted, diff)
 - Terminal/log panel with scroll and auto-expansion
 - History and collections (import/export)
 - Environment variable manager (preview/edit)
 - Auth tab (advanced authentication)
 - Mock server
 - Test runner
 - Flow designer
 - Plugin manager (scripting, extensions)
 - Scheduler/monitor
 - Gemini tab (AI features)
 - Privacy mode (toggle from status bar)
 - Tab reordering and closability (drag, close tabs)
 - Theme selector (dark/light, status bar)
 - Keyboard shortcuts (global)
 - Advanced response visualization
 - Contextual menus, global variables, folders
 - Cloud sync (bi-directional, backend API)
 - Multi-language code generation (Python, JS, Go, Java, C#)
 - Accessibility & i18n (high contrast, language switch)
 - User management (add/remove/list users)
 - Advanced visualization (aggregated stats, method counts)
 - Workspace collaboration (real-time sync, team features)

## Keyboard Shortcuts
- **Send request:** Ctrl+Enter
- **Copy response:** Ctrl+Shift+C
- **Next tab:** Ctrl+Tab
- **Previous tab:** Ctrl+Shift+Tab

## Principles
- SOLID, DRY, KISS
- Professional UX: clear status, error, response, and logs in all panels
- Modular, maintainable, and extensible code

## Usage
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run backend:**
   ```sh
   python backend/main.py
   ```
3. **Run frontend:**
   ```sh
   python frontend/main.py
   ```
4. **Run tests:**
   ```sh
   pytest --disable-warnings --tb=short --cov=frontend --cov=backend --cov-report=term-missing
   ```
5. **Explore all tabs:**
   - Request
   - History
   - Test Runner
   - Mock Server
   - Flow Designer
   - Environments
   - Auth
   - Response Visualizer
   - Scheduler/Monitor
   - Plugins/Scripting
   - Gemini
   - Cloud Sync
   - CodeGen
   - Accessibility/i18n
   - User Management
   - Visualization
   - Workspace Collaboration
   - User Management
   - Visualization

## Compatibility
- Windows 11
- Linux (Debian)

## Screenshots
![Main Window](assets/soulfetch_icon.png)


## Documentation & Contribution
- This README and the entire project are in English for international accessibility and contribution.
- For Spanish-speaking users, a complete technical guide is available: see [`GUIA_TECNICA.md`](GUIA_TECNICA.md).
- For architecture and execution guidelines, see `.github/copilot-instructions.md`.
- All code follows SOLID, DRY, and KISS principles with professional UX.


## License
SoulFetch is open source under the MIT license with attribution. You may use, modify, and distribute it freely, provided you credit the author:

   Created by DogSoulDev (https://dogsouldev.github.io/Web/)

## Status
All tests pass. Full coverage on controllers, backend, mocks, and main features. Ready for production and deployment.