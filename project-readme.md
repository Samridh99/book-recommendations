# Book Recommendations Platform

This is a community-driven platform for sharing and exploring book recommendations, built with Django and Django Rest Framework.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/book-recommendations.git
   cd book-recommendations
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

- Access the admin interface at `http://localhost:8000/admin/`
- View the API documentation at `http://localhost:8000/swagger/` or `http://localhost:8000/redoc/`
- Access the main application at `http://localhost:8000/`

## API Endpoints

- `/api/books/`: List and create books
- `/api/books/search/`: Search for books using the Google Books API
- `/api/recommendations/`: List and create book recommendations
- `/api/recommendations/{id}/like/`: Like a recommendation
- `/api/recommendations/{id}/unlike/`: Unlike a recommendation

## Running Tests

To run the test suite:

```
python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
