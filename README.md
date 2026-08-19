# Quizly Backend

## Description

Quizly Backend is a REST API built with Django and Django REST Framework.

The application generates quizzes automatically from YouTube videos. The video audio is processed using yt-dlp and FFmpeg, transcribed with OpenAI Whisper, and converted into structured quiz data using the Google Gemini API.

Authentication is implemented using JWT access and refresh tokens stored in HTTP-only cookies.

---

## Features

* User registration
* User login and logout
* JWT authentication using HTTP-only cookies
* Access token refresh
* Refresh token blacklisting
* Quiz generation from YouTube videos
* Audio transcription with OpenAI Whisper
* AI-based quiz generation with Google Gemini
* Quiz listing and detail views
* Quiz updating and deletion
* User-specific quiz permissions

---

## Tech Stack

* Python 3.14+
* Django 6.1
* Django REST Framework
* Simple JWT
* SQLite3
* OpenAI Whisper
* Google Gemini API
* yt-dlp
* FFmpeg
* django-cors-headers
* python-dotenv

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd Quizly
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## External Requirements

Quizly requires **FFmpeg** to be installed separately.

### Windows

```bash
winget install --id Gyan.FFmpeg -e --source winget
```

### macOS

```bash
brew install ffmpeg
```

### Linux

```bash
sudo apt install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
```

---

## Environment Variables

Create a `.env` file in the project root based on the provided `.env.template`.

**Windows**

```bash
Copy-Item .env.template .env
```

**Linux / macOS**

```bash
cp .env.template .env
```

Add your own values to the copied `.env` file.

The project automatically loads environment variables using `python-dotenv`.

The `.env` file is excluded from version control.

---

## Database Setup

Apply the migrations:

```bash
python manage.py migrate
```

Create a superuser if required:

```bash
python manage.py createsuperuser
```

---

## Run the Development Server

```bash
python manage.py runserver
```

The server will be available at:

```text
http://127.0.0.1:8000/
```

---

## Authentication

The API uses **JWT authentication**.

Access and refresh tokens are stored in HTTP-only cookies after a successful login.

The access token is used for authenticated requests. The refresh token can be used to request a new access token and is blacklisted during logout.

---

## API Endpoints

### Authentication

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/register/`      |
| POST   | `/api/login/`         |
| POST   | `/api/logout/`        |
| POST   | `/api/token/refresh/` |

### Quizzes

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | `/api/quizzes/`      |
| POST   | `/api/quizzes/`      |
| GET    | `/api/quizzes/{id}/` |
| PATCH  | `/api/quizzes/{id}/` |
| DELETE | `/api/quizzes/{id}/` |

---

## Quiz Generation

Creating a quiz requires a YouTube URL:

```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

The backend processes the video using the following workflow:

```text
YouTube
   ↓
yt-dlp / FFmpeg
   ↓
Whisper
   ↓
Gemini
   ↓
Quiz
```

Generated quizzes contain a title, description, source video URL, and multiple-choice questions.

---

## Permissions

Quiz endpoints require authentication.

Users can:

* create quizzes
* view their own quizzes
* update their own quizzes
* delete their own quizzes

Users cannot access or modify quizzes belonging to another user.

---

## Testing

The project was developed using a **Test Driven Development (TDD)** workflow.

Tests are organized into **Happy Path** and **Unhappy Path** scenarios to verify successful requests, validation errors, authentication, permissions, and missing resources.

Run all tests:

```bash
python manage.py test
```

Run authentication tests:

```bash
python manage.py test authentication
```

Run quiz tests:

```bash
python manage.py test quiz
```

External quiz generation is mocked in the API tests so endpoint behavior can be tested independently.

---

## Development Notes

The project follows:

* Test Driven Development (TDD)
* Django REST Framework
* RESTful API design
* JWT authentication
* HTTP-only authentication cookies
* User-specific permissions
* Separation of concerns
* Dedicated service layer
* Environment variables using `python-dotenv`

---

## Notes

* SQLite is used as the default database.
* FFmpeg must be installed separately.
* A valid Google Gemini API key is required.
* The `.env` file is excluded from version control.
* Create your own `.env` using the provided `.env.template`.
* Quiz generation requires an active internet connection.

---

## Author

Nadine Bauer
