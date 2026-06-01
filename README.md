Service Booking Platform (Persian UI)

Live Demo:

https://service-booking-platform-67xy.onrender.com/

Overview:

Service Booking Platform is a role-based web application built with Flask.

The application interface (UI) is fully in Persian (Farsi), while the backend logic and architecture follow standard software engineering practices.

This system allows users to register, log in, submit service requests, and track the status of their requests. An administrator can manage all requests through a protected dashboard.

The project focuses on backend fundamentals such as authentication, authorization, session management, and request lifecycle control.


Key Features

User Panel (Persian Interface):

User registration

Login with session authentication

Access restricted if email is not registered

Submit service requests with description

View personal request history


Track request status:

    Pending (default)
    
    Approved
    
    Rejected
    
Users can only view their own requests (data isolation enforced)

Secure logout (session cleared)


Admin Panel:

Separate admin login

Protected admin dashboard (/admin/dashboard)

Direct URL access without login is restricted

View all user requests

Search functionality

Approve requests

Reject requests

Delete requests

Logout with session clearing


Architecture & Logic:

Role-Based Access Control (Admin / User)

Session-based authentication

Protected routes

Data isolation per user

Default request status set to "Pending"

Only admin can modify request status

Route protection prevents unauthorized access

Secure logout implementation


Tech Stack:

Python

Flask

SQLite

HTML / CSS

Jinja2

Git & GitHub


Render (Live deployment)

Application Flow:

User registers (Persian interface)

User logs in

User submits a service request

Request is automatically created with status: "Pending"

Admin logs into admin panel

Admin reviews and updates request status

User can see updated status in their dashboard


Security Measures:

Session validation before accessing protected routes

Admin routes require authentication

Users cannot access other users' data

Logout clears session data

Status modification restricted to admin



Running Locally:

Clone repository:

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

cd YOUR_REPO_NAME

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run:

python app.py

Open:

http://127.0.0.1:5000/


Future Improvements:

Password hashing improvement

Environment variable management for admin credentials

UI enhancement and design polish

Email notifications for status updates

Pagination for scalability

Migration to PostgreSQL for production-level database

Docker containerization

Notes:
The UI is fully in Persian (Farsi).
The project is designed to demonstrate backend engineering concepts rather than frontend complexity.
This project represents a complete mini production-style system including authentication, authorization, and request lifecycle management.
