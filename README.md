# Shopping Mart Management System

A Streamlit-based web app for managing products, recording sales, and viewing sales history with user authentication.

## Features
- User registration and login with role-based access (`admin` and `billingMember`)
- Product management (add, update, delete) by admins
- Sales recording with cart, GST, and discount calculations
- Sales transaction tracking and stock updates
- View sales history

## Technologies
- Python, Streamlit
- MySQL (database)
- bcrypt for password hashing
- dotenv for environment variable management

## Setup
1. Configure MySQL and create a database.
2. Set environment variables in `.env`:
    DB_HOST=your_host
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_NAME=your_database
3. Run `models.py` to create necessary database tables.
4. Install dependencies:
    pip install streamlit mysql-connector-python bcrypt python-dotenv
5. Run the app:
    streamlit run app.py

## Usage
- Admins can manage products and record sales.
- Billing members can record sales and view sales history.
- User authentication is required.

## File Overview
- `app.py`: Main Streamlit app interface
- `auth.py`: User login and registration logic
- `billing.py`: Sale and transaction handling
- `inventory.py`: Product CRUD operations
- `db.py`: Database connection management
- `models.py`: Database table creation
- `test_db.py`: Database connection test script

## License
Open source for educational and personal use.
