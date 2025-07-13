# ALX Travel App

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/django-4.2%2B-green.svg)
![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)

A modern RESTful API backend for a travel accommodation platform, built with Django and Django REST Framework.  
This project powers core features such as property listings, bookings, reviews, and user management, and is designed for extensibility and scalability.

---

## ✨ Features

- 🏡 **Property Listings**: Create, view, update, and delete accommodations
- 📅 **Bookings**: Book stays and manage reservations
- ⭐ **Reviews**: Leave reviews for bookings
- 🔒 **User Authentication**: Secure access and user management (via Django’s auth)
- ⚙️ **Admin Dashboard**: Manage content with Django Admin
- 📖 **Interactive API Docs**: Swagger/OpenAPI UI at `/swagger/`
- 🌍 **CORS Support**: Fully API-ready for frontend clients
- ⚡ **Asynchronous Tasks**: Celery + RabbitMQ integration
- 🛠️ **Environment Variables**: Configuration via `.env`

---

## ⚙️ Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: MySQL
- **Task Queue**: Celery, RabbitMQ
- **API Docs**: drf-yasg (Swagger/OpenAPI)
- **Env Config**: django-environ
- **CORS**: django-cors-headers

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL
- RabbitMQ

### Installation

```bash
# Clone the repository
git clone https://github.com/reuben-idan/alx_travel_app_0x00.git
cd alx_travel_app_0x00/alx_travel_app_0x00

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r alx_travel_app/requirement.txt

# Set up your .env file
cp .env.example .env  # Edit with your DB and RabbitMQ credentials

# Apply migrations
python alx_travel_app/manage.py migrate

# Create a superuser for admin access
python alx_travel_app/manage.py createsuperuser

# (Optional) Seed the database with sample listings
python alx_travel_app/manage.py seed

# Start the development server
python alx_travel_app/manage.py runserver
```

### Running Celery

```bash
celery -A alx_travel_app worker --loglevel=info
```

## Celery & RabbitMQ Setup

1. Install RabbitMQ and ensure it is running.
2. Set the following environment variables in your `.env` file:
   - `CELERY_BROKER_URL=amqp://guest:guest@localhost//`
   - `CELERY_RESULT_BACKEND=rpc://`
3. Start Celery worker:
   ```bash
   celery -A alx_travel_app worker --loglevel=info
   ```

## Email Notification Setup

Set the following environment variables in your `.env` file:
- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`
- `EMAIL_HOST_USER=your_email@example.com`
- `EMAIL_HOST_PASSWORD=your_email_password`
- `DEFAULT_FROM_EMAIL=your_email@example.com`

## Booking Email Notification

When a booking is created, a confirmation email is sent asynchronously using Celery.

---

## 🗂️ Project Structure

```