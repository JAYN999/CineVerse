# CineVerse 🎬

A full-stack movie search and review platform built with **Flask, Jinja2, SQLite, and JavaScript**. 

> ⚠️ **Note:** This project is currently **under active development**. 

## Features
- **Live Movie Search:** Integrated with the **OMDb REST API** to retrieve live ratings, genres, poster designs, and plot summaries.
- **User Authentication:** Session-based authentication workflow featuring secure registration, login, protected routes, and duplicate account checks.
- **Star-Rating & Review System:** Allows users to leave reviews and persistent star-ratings stored locally in SQLite.
- **Movie-Themed UI:** Responsive user interface enhanced with custom CSS transitions and animations.

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templates
- **Database:** SQLite3
- **APIs:** OMDb REST API

## Setup Instructions (Local Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JAYN999/CineVerse.git
   cd CineVerse
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install flask requests
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

## 📄 License
All rights reserved. This repository and its code are for personal portfolio review and viewing purposes only. No permission is granted to copy, modify, distribute, or use this code for any other purpose.
