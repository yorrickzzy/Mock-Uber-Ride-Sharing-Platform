
# Mock Uber Ride-Sharing Platform

A full-stack ride-sharing web application built with **Django, PostgreSQL, and Docker**.

Supports ride creation, ride sharing, driver assignment, and ride lifecycle management.

<img width="947" height="435" alt="image" src="https://github.com/user-attachments/assets/02b4268c-dd35-45b6-83eb-bb026d3e85ef" />


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
The database is built on Django ORM and consists of core domain models centered around the Ride entity.

- `Ride`
Core business entity representing ride requests, including owner, destination, arrival time, passenger count, and status.

- `DriverProfile`
One-to-One extension of the built-in User model to separate authentication from driver-specific data.

- `Vehicle`
Stores vehicle information associated with drivers.

- `RideSharers`
Many-to-Many relationship linking rides and participating users.

##  Quick Start

```bash
chmod +x ./web-app/*.sh
sudo docker-compose up
```

##  Visit
http://127.0.0.1:8000/ 

##  Django Configuration
Ensure the following in settings.py:
```bash
ALLOWED_HOSTS = ['web','127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]
```

Author: Zeyuan Zhang, Leo Wei
