# Personal Metrics API
A local REST API built with Python and Flask to track my daily habits, including fitness, study sessions, and gaming.

## Features Currently Built
* **POST /api/logs:** Add a new activity log.
* **GET /api/logs:** Retrieve logs (supports `?category=` and `?limit=` filters).
* **DELETE /api/logs/<id>:** Remove a specific log.
* **GET /api/summary:** Get total duration and log count grouped by category.

## Tech Stack
* Python 3
* Flask
* SQLite3