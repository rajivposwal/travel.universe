# ASRS Travel — Ticket Booking System

A full-stack travel booking web app built with **Flask + SQLite**.

## Features
- ✈️ Search & book Flights, Trains, Buses, Hotels & Food
- 🔐 User authentication (Register / Login / Logout)
- 👤 User profile with photo upload & booking history
- 🎫 Multi-step booking with payment simulation
- 🌙 Dark / Light theme toggle

## Tech Stack
- **Backend:** Python (Flask), SQLite
- **Frontend:** HTML, CSS (Vanilla), JavaScript
- **Auth:** Werkzeug password hashing

## Running Locally
```bash
pip install -r requirements.txt
python init_db.py
python bookticket.py
```
Open http://127.0.0.1:5000

## Default Login
| Username | Password |
|----------|----------|
| admin | asrs2026 |

## Deployment (Render)
- Connect this repo on [Render.com](https://render.com)
- Build Command: `pip install -r requirements.txt && python init_db.py`
- Start Command: `gunicorn bookticket:app`
