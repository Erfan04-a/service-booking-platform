# Service Booking Platform (Persian UI)

🚀 Live Demo:
https://service-booking-platform-67xy.onrender.com/

## Overview

Service Booking Platform is a role-based web application built with Flask.

The application interface (UI) is fully in Persian (Farsi), while the backend architecture follows standard web development practices.

Users can register, log in, submit service requests, and track their request status. An administrator can manage all requests through a protected dashboard.

This project focuses on authentication, authorization, session management, and request lifecycle handling.

---

## Features

### User Panel

- User registration
- User login
- Session-based authentication
- Submit service requests
- Add descriptions to requests
- View personal requests
- Track request status:
  - Pending
  - Approved
  - Rejected
- Secure logout
- Users can only access their own data

### Admin Panel

- Separate admin login
- Protected dashboard
- Search functionality
- View all requests
- Approve requests
- Reject requests
- Delete requests
- Secure logout
- Unauthorized users cannot access admin routes

---

## Architecture

- Role-Based Access Control (Admin / User)
- Session Authentication
- Protected Routes
- Request Lifecycle Management
- Data Isolation
- SQLite Database Integration

---

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2
- Git
- GitHub
- Render

---

## Application Flow

1. User registers an account
2. User logs in
3. User submits a service request
4. Request status is automatically set to **Pending**
5. Admin reviews requests
6. Admin updates status
7. User can track request progress

---

## Security Features

- Session validation
- Protected admin routes
- Data isolation per user
- Secure logout
- Admin-only status modification

---

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Erfan04-a/service-booking-platform.git
cd service-booking-platform
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000/
```

---

## Future Improvements

- Password hashing
- Environment variables for credentials
- Better UI/UX
- Email notifications
- PostgreSQL integration
- Docker support

---

## Notes

- The application interface is fully in Persian (Farsi).
- The project was built to demonstrate backend development concepts including authentication, authorization, and request management.
- This is a backend-focused project with role-based access control and request lifecycle handling.

---

## Author

Erfan
Computer Engineering Student
