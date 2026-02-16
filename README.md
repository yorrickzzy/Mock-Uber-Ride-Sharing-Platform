# Mock Uber Ride-Sharing Platform

A full-stack ride-sharing web application built with **Django, PostgreSQL, and Docker**.

Supports ride creation, ride sharing, driver assignment, and ride lifecycle management.


## Features

- User authentication & role-based access control  
- Ride creation with sharable ride support  
- Driver profile & vehicle management  
- Ride status lifecycle (Open → Confirmed → Completed)  
- Email notification via SendGrid  
- Fully containerized deployment (Docker Compose)  
- Persistent PostgreSQL storage using Docker volumes  

## Tech Stack

- **Backend:** Django 5.x, Python  
- **Database:** PostgreSQL  
- **DevOps:** Docker, Docker Compose  
- **Email:** SendGrid API
  
## Database Design

Custom domain models:

- `Ride` (core entity)  
- `DriverProfile` (One-to-One with User)  
- `Vehicle`  
- Many-to-Many relationship for ride sharers  

Designed with normalized schema and referential integrity.

##  Quick Start

```bash
chmod +x ./web-app/*.sh
sudo docker-compose up
```

##  Visit
http://<your-vcm-hostname>:8000/  or   http://127.0.0.1:8000/ (if local)

##  Django Configuration (Local)
Ensure the following in settings.py:
```bash
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]
```

Author: Zeyuan Zhang, Leo Wei
