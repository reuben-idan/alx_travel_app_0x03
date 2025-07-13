# ALX Travel App

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/django-4.2%2B-green.svg)
![License](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)

A modern RESTful API backend for a travel accommodation platform, built with Django and Django REST Framework.  
This project powers core features such as property listings, bookings, reviews, and user management, and is designed for extensibility and scalability.

## Features

- 🏡 **Property Listings**: Create, view, update, and delete accommodations
- 📅 **Bookings**: Book stays and manage reservations
- ⭐ **Reviews**: Leave reviews for bookings
- 🔒 **User Authentication**: Secure access and user management (via Django's auth)
- ⚙️ **Admin Dashboard**: Manage content with Django Admin
- 📖 **Interactive API Docs**: Swagger/OpenAPI UI at `/swagger/`
- 🌍 **CORS Support**: Fully API-ready for frontend clients
- ⚡ **Asynchronous Tasks**: Celery + RabbitMQ integration
- 🛠️ **Environment Variables**: Configuration via `.env`

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: MySQL
- **Task Queue**: Celery, RabbitMQ
- **API Docs**: drf-yasg (Swagger/OpenAPI)
- **Env Config**: django-environ
- **CORS**: django-cors-headers

## Getting Started

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

### API Documentation

Visit [http://localhost:8000/swagger/](http://localhost:8000/swagger/) for interactive Swagger UI.

## Project Structure

```
alx_travel_app_0x00/
  └── alx_travel_app/
      ├── listings/        # Listings, bookings, reviews (app)
      ├── settings.py      # Django settings
      ├── urls.py          # URL routing
      ├── requirement.txt  # Requirements
      └── ...
  └── .env                 # Environment configuration
```

## Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

Distributed under the BSD-3-Clause License.

---

_Made with ❤️ by the ALX Travel App Team._

## Chapa Payment Integration

### Setup

1. Register at https://developer.chapa.co/ and obtain your CHAPA_SECRET_KEY.
2. Add your secret key to a `.env` file in the project root:
   ```
   CHAPA_SECRET_KEY=your_chapa_secret_key_here
   ```
3. Install dependencies:
   ```
   pip install django-environ requests djangorestframework
   ```
4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### API Endpoints

- **Initiate Payment:**
  - `POST /api/listings/payments/initiate/`
  - Body: `{ "booking_id": <id>, "amount": <amount>, "email": "user@example.com", "first_name": "...", "last_name": "..." }`
  - Returns: Payment URL and payment object.
- **Verify Payment:**
  - `GET /api/listings/payments/verify/?tx_ref=<transaction_ref>`
  - Returns: Payment status and payment object.

### Testing

- Use Chapa's sandbox environment for testing.
- Check Payment model in admin or via API to confirm status updates.
