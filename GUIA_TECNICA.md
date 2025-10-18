
![SoulFetch Logo](assets/soulfetch_icon.png)
# SoulFetch - Guía Técnica

## Índice
- [1. Introducción técnica](#1-introducción-técnica)
- [2. Estructura de carpetas y módulos](#2-estructura-de-carpetas-y-módulos)
- [3. Arquitectura y patrones](#3-arquitectura-y-patrones)
- [4. Backend: FastAPI Hexagonal](#4-backend-fastapi-hexagonal)
- [5. Frontend: PySide6 MVC](#5-frontend-pyside6-mvc)
- [6. Persistencia y modelo de datos](#6-persistencia-y-modelo-de-datos)
- [7. Testing y automatización](#7-testing-y-automatización)
- [8. Empaquetado y despliegue](#8-empaquetado-y-despliegue)
- [9. Integración de iconos y recursos](#9-integración-de-iconos-y-recursos)
- [10. Seguridad, privacidad y buenas prácticas](#10-seguridad-privacidad-y-buenas-prácticas)
- [11. Extensibilidad y personalización](#11-extensibilidad-y-personalización)
- [12. Colaboración y sincronización](#12-colaboración-y-sincronización)
- [13. Accesibilidad e internacionalización](#13-accesibilidad-e-internacionalización)
- [14. Referencias y recursos](#14-referencias-y-recursos)

---

## 1. Introducción técnica
SoulFetch es un cliente API avanzado, multiplataforma, construido con una arquitectura robusta y modular. El frontend utiliza PySide6 (Qt) bajo el patrón MVC, mientras que el backend emplea FastAPI siguiendo principios hexagonales. Todo el código sigue SOLID, DRY y KISS.

## 2. Estructura de carpetas y módulos
```
backend/
  adapters/      # Routers y endpoints (collections, history, environments, etc.)
  application/   # Lógica de aplicación, casos de uso
  domain/        # Modelos de dominio y entidades
  main.py        # Punto de entrada backend
frontend/
  controllers/   # Lógica de control y orquestación de vistas/modelos
  models/        # Modelos de datos y lógica de negocio frontend
  views/         # Vistas PySide6 (QMainWindow, tabs, widgets)
  main.py        # Punto de entrada frontend
assets/          # Iconos, imágenes, recursos estáticos
SoulFetch.spec   # Configuración PyInstaller para .exe
LICENSE         # Licencia open source
```

## 3. Arquitectura y patrones
- **Frontend:** MVC puro (controllers, models, views). Cada pestaña es un widget desacoplado.
- **Backend:** Hexagonal (puertos y adaptadores). Routers desacoplados de la lógica de dominio.
- **Principios:** SOLID, DRY, KISS, separación de responsabilidades, modularidad, extensibilidad.

## 4. Backend: FastAPI Hexagonal
- **Routers:** Cada recurso (collections, history, environments, etc.) tiene su router en `adapters/`.
- **Dominio:** Modelos y lógica de negocio en `domain/`.
- **Aplicación:** Casos de uso y orquestación en `application/`.
- **Persistencia:** SQLite, acceso directo o vía modelos Pydantic.
- **Mock server:** Router dedicado para pruebas y simulación de APIs.
- **WebSocket:** Soporte para colaboración y sincronización en tiempo real.

## 5. Frontend: PySide6 MVC
- **MainWindow:** Orquesta pestañas, status bar, temas, atajos y notificaciones.
 - **Tabs:** Cada funcionalidad (Request, History, Auth, etc.) es un widget independiente. Las pestañas Mock Server, Cloud Sync, CodeGen, Visualization y Workspace Collaboration se ocultan automáticamente si el endpoint no está disponible o no tienen lógica real. La pestaña Flow Designer ha sido eliminada hasta que exista backend real.
- **Controllers:** Gestionan la lógica de cada vista y la comunicación con modelos y backend.
- **Models:** Encapsulan datos y lógica de negocio local.
- **Vistas:** Widgets PySide6, layouts responsivos, dark theme, accesibilidad.
- **Notificaciones:** Toasts, status bar, mensajes de error y éxito.
- **Shortcuts:** Atajos globales y por pestaña.

## 6. Persistencia y modelo de datos
- **SQLite:** Base de datos local (`db/soulfetch.db`).
- **Tablas:** collections, history, env_vars, users, etc.
- **ORM:** Uso de Pydantic para validación y serialización.
- **Import/export:** Soporte YAML, CSV, JSON para colecciones e historial.

## 7. Testing y automatización
- **Pytest:** Suite completa en `tests/` para backend y frontend.
- **Cobertura:** Pruebas unitarias y de integración, mocks para endpoints externos.
- **Headless:** Tests frontend robustos para entornos sin GUI.
- **CI/CD:** Preparado para integración continua.

## 8. Empaquetado y despliegue
- **PyInstaller:** Archivo `SoulFetch.spec` para generar el .exe con icono y recursos.
- **Icono:** `assets/soulfetch_icon.ico` y `.png` para integración en Windows.
- **Cross-platform:** Compatible con Windows 11 y Linux (Debian).

## 9. Integración de iconos y recursos
- **Ventana principal:** `setWindowIcon(QIcon('assets/soulfetch_icon.png'))`.
- **PyInstaller:** Flag `--icon=assets/soulfetch_icon.ico` en el spec.
- **Assets:** Centralizados en la carpeta `assets/`.

## 10. Seguridad, privacidad y buenas prácticas
- **Privacy mode:** Botón global, desactiva historial y persistencia.
- **Validación:** Entradas validadas en frontend y backend.
- **Errores:** Manejo robusto, logs y feedback al usuario.
- **CORS:** Configurado en backend para desarrollo y producción.
- **Licencia:** MIT con atribución obligatoria.

## 11. Extensibilidad y personalización
- **Plugins:** Pestaña de plugins/scripting para extensiones Python.
- **Codegen:** Generación de snippets multi-lenguaje.
- **Temas:** Selector dark/light, fácil de ampliar.
- **Variables globales:** Panel de entorno editable.

## 12. Colaboración y sincronización
- **Cloud Sync:** Sincronización bidireccional con backend.
- **Workspace Collaboration:** WebSocket y endpoints dedicados.
- **User Management:** Gestión de usuarios, roles y permisos.

## 13. Accesibilidad e internacionalización
- **i18n:** Soporte multi-idioma, fácil de ampliar.
- **Accesibilidad:** Alto contraste, navegación por teclado, tooltips.
- **Visualización:** Gráficas, estadísticas, paneles avanzados.

## 14. Referencias y recursos
- [FastAPI](https://fastapi.tiangolo.com/)
- [PySide6](https://doc.qt.io/qtforpython/)
- [PyInstaller](https://pyinstaller.org/)
- [Burp Suite](https://portswigger.net/burp)
- [Postman](https://www.postman.com/)
- [Apidog](https://apidog.com/)
- [MIT License](LICENSE)

---

**Autor:** DogSoulDev — https://dogsouldev.github.io/Web/

---
# 15. Ejemplos de uso avanzado

## Ejemplo: Crear y ejecutar una colección de peticiones
1. Abre SoulFetch y crea una nueva colección desde la pestaña principal.
2. Añade varias peticiones (GET, POST, etc.) con diferentes entornos.
3. Usa variables de entorno en la URL y el body (`{{API_URL}}`, `{{TOKEN}}`).
4. Ejecuta la colección y visualiza los resultados en la pestaña de History.
5. Exporta la colección a YAML o CSV para compartirla.

## Ejemplo: Automatización y scripting
- Usa la pestaña Test Runner para escribir scripts Python que validen respuestas.
- Programa peticiones recurrentes desde Scheduler/Monitor.
- Añade plugins en la pestaña Plugins/Scripting para extender funcionalidades.

## Ejemplo: Colaboración en tiempo real
- Conecta a un workspace colaborativo desde la pestaña Workspace Collaboration.
- Sincroniza colecciones y entornos con Cloud Sync.
- Gestiona usuarios y permisos desde User Management.

---
# 16. Troubleshooting y preguntas frecuentes

**¿Por qué no veo respuestas o el backend no responde?**
- Verifica que el backend esté corriendo (`python backend/main.py` o con Uvicorn).
- Comprueba la configuración de CORS y el puerto.

**¿Cómo agrego un nuevo tipo de autenticación?**
- Añade la lógica en `frontend/views/auth_tab.py` y expande el backend si es necesario.

**¿Cómo personalizo el tema?**
- Modifica la función `set_dark_theme` en `frontend/views/main_window.py` o añade nuevos estilos.

**¿Cómo empaqueto el programa para Windows?**
- Usa PyInstaller con el spec incluido: `pyinstaller SoulFetch.spec`.

---
# 17. Diagrama de arquitectura (ASCII)

```
┌────────────┐      HTTP/WebSocket      ┌──────────────┐
│  Frontend  │◀───────────────────────▶│   Backend    │
│  PySide6   │                        │   FastAPI    │
├────────────┤                        ├──────────────┤
│ Controllers│                        │  Routers     │
│  Models    │                        │  Domain      │
│  Views     │                        │  Application │
│  Assets    │                        │  DB/SQLite   │
└────────────┘                        └──────────────┘
```

**Flujo típico:**
1. El usuario interactúa con la GUI (PySide6).
2. Los controllers gestionan la lógica y llaman a modelos o al backend.
3. El backend responde con datos, que se muestran en las vistas.
4. Todo es modular, desacoplado y extensible.

---
# 18. Glosario rápido

- **Colección:** Grupo de peticiones guardadas.
- **Entorno:** Conjunto de variables reutilizables.
- **Mock server:** Simula respuestas de API.
- **Scheduler:** Programa peticiones automáticas.
- **Plugin:** Script Python que extiende la app.
- **Workspace:** Espacio colaborativo multiusuario.

---
Para dudas, sugerencias o contribuciones, visita: https://dogsouldev.github.io/Web/
