# Story-generator: Choose Your Own Adventure Game

A "Choose Your Own Adventure" web application that generates cool and interactive storylines. 
The project is split into a scalable and robust backend built with FastAPI, and a modern frontend built with React and Vite.

## Project Structure

The repository is organized into two main workspaces:
- `backend/`: The Python FastAPI server handling the game logic and API points to generate stories.
- `frontend/`: The React + Vite application serving as the UI to interact with the game.

## Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python
- **Database**: SQLite

### Frontend
- **Framework**: [React](https://react.dev/) (powered by [Vite](https://vitejs.dev/))
- **Language**: JavaScript
- **Routing**: React Router DOM (v7)
- **HTTP Client**: Axios

## Getting Started

### Backend Setup

Navigate to the `backend` directory and set up your Python environment:

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate
# Activate it (Mac/Linux)
# source .venv/bin/activate

# Start the auto-reloading development server
python main.py
```
The FastAPI backend will typically be running closely connected at `http://localhost:8000`, with interactive Swagger UI docs available at `http://localhost:8000/docs`.

### Frontend Setup

Navigate to the `frontend` directory and install the Node module dependencies:

```bash
cd frontend

# Install all dependencies
npm install

# Start the Vite development server
npm run dev
```
The React development server will start, typically available at `http://localhost:5173`. Open this URL in your browser to view the frontend application!

## Features
- **Story Generation**: Dynamic story generation endpoints (`/story` and `/job`).
- **Interactive API Docs**: Explore backend capabilities using `/docs` and `/redoc`.
- **Fast & Modern UI**: Built with a fast React/Vite development experience.
