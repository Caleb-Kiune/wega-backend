# Flask API Project Setup Guide

This guide will help you set up and run the Flask API project with SQLite database integration.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Project Overview

This is a RESTful API built with Flask and SQLite that provides basic user management functionality. The project uses:
- Flask for the web framework
- SQLAlchemy for database ORM
- SQLite for data storage

## Installation Steps

1. **Clone the repository** (if using Git):
   ```bash
   git clone <repository-url>
   cd flask-api-project
   ```

2. **Create a virtual environment**:
   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On Unix/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

The server will start at `http://localhost:5000`

## API Documentation

### User Endpoints

1. **Get All Users**
   - Method: `GET`
   - URL: `/users`
   - Response: List of all users
   - Status Code: 200

2. **Get User by ID**
   - Method: `GET`
   - URL: `/users/<id>`
   - Response: User details
   - Status Code: 200 or 404

3. **Create New User**
   - Method: `POST`
   - URL: `/users`
   - Request Body:
     ```json
     {
       "username": "string",
       "email": "string"
     }
     ```
   - Response: Created user details
   - Status Code: 201 or 400

## Testing the API

You can test the API using curl or any API testing tool like Postman:

1. **Create a new user**:
   ```bash
   curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com"}'
   ```

2. **Get all users**:
   ```bash
   curl http://localhost:5000/users
   ```

3. **Get specific user**:
   ```bash
   curl http://localhost:5000/users/1
   ```

## Project Structure

```
flask_api_project/
├── .venv/              # Virtual environment (not in version control)
├── app.py             # Main Flask application
├── models/
│   └── user.py        # User model definition
├── routes/
│   └── user_routes.py # API endpoints
├── requirements.txt   # Project dependencies
└── .gitignore        # Git ignore rules
```

## Database

The application uses SQLite as the database. The database file (`users.db`) will be created automatically when you first run the application. The database schema includes:

- Users table with fields:
  - id (Primary Key)
  - username (Unique)
  - email (Unique)
  - created_at (Timestamp)

## Error Handling

The API includes basic error handling for:
- Missing required fields
- Invalid data types
- Duplicate entries
- Not found resources

## Development

To modify or extend the project:

1. Make sure you're in the virtual environment
2. Create new models in the `models/` directory
3. Add new routes in the `routes/` directory
4. Update `app.py` to register new blueprints
5. Test your changes locally

## Troubleshooting

Common issues and solutions:

1. **Database errors**:
   - Delete `users.db` and restart the application
   - Check SQLite installation

2. **Import errors**:
   - Ensure you're in the virtual environment
   - Verify all dependencies are installed

3. **Port conflicts**:
   - Change the port in `app.py` if 5000 is in use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License. 