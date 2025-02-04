# DRF E-Commerce Shop Application

This project is a DRF-based e-commerce web application that includes user authentication, product management, shopping cart functionality, and order processing.
Save caching in the Redis Service is performed.
## Features
- **User Authentication**
   - Custom User Model (registration with email).
    - Signup, login, and logout functionality with JWT.
    - Verify Registration with OTP Code.
    - Automatic creation of user information based on the session.
- **Product Management**
  - Product categorization
- **Shopping Cart**
    - Add and remove products from the cart.
    - Update product quantities in the cart.
    - View cart summary and total cost.

## Project Structure

```bash
.
├── accounts
│   ├── admin.py                    # Accounts admin configuration
│   ├── apps.py                     # Accounts apps configuration
│   ├── authentication.py           # Authentication logic
│   ├── models.py                   # Accounts models (User, Profile, OTPCode)
│   ├── serializers.py              # Serializers for API endpoints
│   ├── urls.py                     # Accounts URL configuration
│   └── views.py                    # Accounts views
├── cart
│   ├── admin.py                    # Cart admin configuration
│   ├── apps.py                     # Cart apps configuration
│   ├── cart.py                     # Cart management logic
│   ├── models.py                   # Cart models (Cart, CartItem)
│   ├── serializers.py              # Serializers for API endpoints
│   ├── urls.py                     # Cart URL configuration
│   └── views.py                    # Cart views
├── core
│   ├── asgi.py                     # ASGI configuration
│   ├── celery_conf.py              # Celery configuration
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Main URL configuration
│   └── wsgi.py                     # WSGI entry point
├── orders
│   ├── admin.py                    # Orders admin configuration
│   ├── apps.py                     # Orders apps configuration
│   ├── models.py                   # Orders models (Order, OrderItem)
│   ├── serializers.py              # Serializers for API endpoints
│   ├── urls.py                     # Orders URL configuration
│   └── views.py                    # Orders views
├── shop
│   ├── admin.py                    # Shop admin configuration
│   ├── apps.py                     # Shop apps configuration
│   ├── models.py                   # Shop models (Product, Category, Tag)
│   ├── serializers.py              # Serializers for API endpoints
│   ├── tasks.py                    # Celery tasks for shop
│   ├── urls.py                     # Shop URL configuration
│   └── views.py                    # Shop views
├── db.sqlite3                      # SQLite database file
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Dockerfile for containerization
├── LICENSE                         # License file
├── manage.py                       # Django's command-line utility
├── requirements.txt                # Python dependencies
└── README.md                       # Project README file
```

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone git@github.com:cyhssin/online-shop.git
   ```

2. Install dependencies:

   ```bash
   python -m venv .env
   source ./.env/bin/activate
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the site at `http://127.0.0.1:8000/`.

## Docker Setup
1. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

2.Access the site at ```http://localhost:8000/.```

## Custom Commands

- **Populate Data**: Use the custom management command to generate fake data for testing:

  ```bash
  python manage.py populate_data
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed by [cyhssin](https://github.com/cyhssin)