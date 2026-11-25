# CineVerse

CineVerse is a movie search and review web application built with **Python, Flask, SQLite, Jinja2, HTML, CSS, and JavaScript**. It uses the OMDb API to look up movie information.

## Features

- User registration and login with password hashing
- Session-protected home and review routes
- Movie search through the OMDb REST API
- Movie posters, release years, genres, plots, and IMDb ratings
- User-submitted movie ratings and reviews stored in SQLite
- Responsive, movie-themed interface

## Technology

- **Language:** Python
- **Backend:** Flask
- **Database:** SQLite
- **Templates:** Jinja2
- **Frontend:** HTML, CSS, JavaScript
- **External API:** OMDb

## Local setup

1. Clone the repository and open the project folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`.
5. Generate a random Flask secret (for example, run `python -c "import secrets; print(secrets.token_hex(32))"`) and place it in `FLASK_SECRET_KEY`. Add your OMDb key to `OMDB_API_KEY`.
6. Start the application:
   ```bash
   python app.py
   ```
7. Open http://127.0.0.1:5001.

## Configuration

The application reads configuration from environment variables (loaded from `.env` for local development):

- `FLASK_SECRET_KEY`: a private, random value used to sign Flask sessions. Never commit your real value.
- `OMDB_API_KEY`: your OMDb API key. Never commit your real value.
- `FLASK_DEBUG`: optional; set to `true` only during local development.

The `.env` file and local SQLite database are excluded by `.gitignore`.

## Security and project scope

This is a learning/portfolio project, not a production-ready authentication service. Passwords are hashed. Existing legacy plaintext passwords are upgraded to hashes on a successful login. Production deployment would also require HTTPS, CSRF protection, login rate limiting, secure cookie settings, and a managed secret store.

If an API key or secret was previously committed, remove it from the current code **and revoke/rotate it with its provider**. Deleting a value from the latest commit does not remove it from Git history.

## License

All rights reserved. This repository and its code are for personal portfolio review and viewing purposes only.
