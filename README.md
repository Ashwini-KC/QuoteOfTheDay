# Quote of the Day - Flask Application

A production-ready Flask web application that serves inspirational quotes. The application supports multiple endpoints to retrieve daily quotes, random quotes, and provides a beautiful web interface.

## Features

- 🌟 **Daily Quote of the Day** - Get the quote for today
- 🎲 **Random Quotes** - Get a random inspirational quote
- 📡 **REST API** - Full-featured JSON API endpoints
- 💅 **Responsive UI** - Beautiful, mobile-friendly interface
- 🔍 **Error Handling** - Centralized error handling with custom error pages
- 📊 **Logging** - Comprehensive application logging
- ✅ **Validation** - Input validation and data integrity
- 🚀 **Caching** - Efficient quote loading with caching
- 🧪 **Testing** - Unit and integration tests with pytest

## Project Structure

```
QuoteOfTheDay/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── quote.py             # Quote data model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Main web routes
│   │   └── api.py               # REST API routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── quote_service.py     # Business logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging setup
│   │   └── validators.py        # Input validation
│   ├── static/
│   │   └── css/
│   │       └── style.css        # Responsive CSS
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Homepage
│       └── errors/
│           ├── 404.html         # 404 error page
│           └── 500.html         # 500 error page
├── data/
│   └── quotes.json              # 365+ unique quotes
├── logs/                        # Application logs
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   └── quotes.json          # Test fixtures
│   ├── test_unit_quotes.py      # Unit tests
│   └── test_integration_api.py  # Integration tests
├── run.py                       # Application entry point
├── config.py                    # Configuration management
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd "YOUR CODE REPO"
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

   The application will start on `http://localhost:5000`

## API Endpoints

### Homepage
- **GET** `/` - Display quote of the day on web interface

### Health Check
- **GET** `/health` - Health check endpoint
  ```json
  {
    "status": "healthy"
  }
  ```

### REST API Endpoints

#### Get Quote of the Day
- **GET** `/api/quote`
  ```json
  {
    "quote": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs",
    "date_index": 0,
    "category": "Motivation",
    "tags": ["work", "inspiration"]
  }
  ```

#### Get Quote by Index
- **GET** `/api/quote/<index>` - Get a specific quote by its index
  ```json
  {
    "quote": "Innovation distinguishes between a leader and a follower.",
    "author": "Steve Jobs",
    "date_index": 1,
    "category": "Innovation",
    "tags": ["leadership", "change"]
  }
  ```

#### Get Random Quote
- **GET** `/api/quote/random` - Get a random quote
  ```json
  {
    "quote": "Success is not final, failure is not fatal.",
    "author": "Winston Churchill",
    "date_index": 6,
    "category": "Success",
    "tags": ["resilience", "perspective"]
  }
  ```

### Error Responses

- **404 Not Found** - Route doesn't exist
- **405 Method Not Allowed** - Wrong HTTP method
- **500 Internal Server Error** - Server-side error

## Configuration

Configuration is managed through `config.py` with support for multiple environments:

### Environment Variables
```bash
FLASK_ENV=development          # development, production, testing
FLASK_APP=run.py
SECRET_KEY=your-secret-key
DEBUG=True                     # Enable debug mode
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Configuration Classes
- **DevelopmentConfig** - Development with debug enabled
- **ProductionConfig** - Production with security hardening
- **TestingConfig** - Testing with in-memory data

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_unit_quotes.py
pytest tests/test_integration_api.py
```

### Run Specific Test
```bash
pytest tests/test_unit_quotes.py::TestQuoteModel::test_quote_creation
```

### Generate Coverage Report
```bash
pytest --cov=app --cov-report=html
```

### Test Coverage
- Unit tests for models, services, and validators
- Integration tests for API endpoints
- Error handling and edge cases
- Security and data validation tests

## Features Explained

### Quote of the Day Logic
- Calculates day of year (0-365)
- Handles leap years gracefully
- Returns same quote for all users on same day
- Updated automatically at midnight

### Caching
- Quotes loaded once and cached in memory
- Cache invalidated when file changes
- Improves performance on repeated requests
- Automatic cache management

### Error Handling
- No stack traces exposed to users
- User-friendly error pages
- Proper HTTP status codes
- Comprehensive error logging

### Validation
- Quote data structure validation
- Quote quote and author validation
- JSON malformed data handling
- Safe data serialization

### Logging
- File-based logging to `logs/app.log`
- Console output for development
- Configurable log levels
- Timestamp and conquote in all logs

## Data Files

### quotes.json Format
```json
[
  {
    "quote": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs",
    "category": "Motivation",
    "tags": ["work", "inspiration"]
  }
]
```

### Requirements
- Minimum 365 unique quotes
- Each quote must have `quote` and `author`
- Optional: `category`, `tags`
- All quotes must be properly formatted JSON

## Development

### Adding New Routes
1. Create new route in `app/routes/`
2. Import and register in `app/__init__.py`
3. Add corresponding tests

### Adding New Services
1. Create service class in `app/services/`
2. Import in relevant routes
3. Add unit tests

### Database Integration
The application is designed to support database integration:
- A `db` object is available in `app/__init__.py`
- Can be extended with SQLAlchemy for persistent storage

## Production Deployment

### Security Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Use HTTPS in production
- [ ] Set up proper logging and monitoring
- [ ] Configure CORS if needed
- [ ] Use a production WSGI server (Gunicorn, uWSGI)

### Deployment Steps
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Troubleshooting

### Import Errors
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check `PYTHONPATH` includes project root

### No Quotes Found
- Verify `data/quotes.json` exists
- Check file path in `config.py`
- Validate JSON syntax

### Cache Issues
- Clear cache: `QuoteService.clear_cache()`
- Check file modification time
- Restart application

### Port Already in Use
```bash
# Change port
export FLASK_ENV=development
# In run.py, modify: app.run(debug=True, port=5001)
```

## Dependencies

- **Flask 3.0.0** - Web framework
- **python-dotenv 1.0.0** - Environment variables
- **pytest 7.4.0** - Testing framework
- **pytest-cov 4.1.0** - Code coverage
- **requests 2.31.0** - HTTP library

## License

Copyright ASHWINI, 2026

## Author

Created by ASHWINI

## Support

For issues or questions, please refer to the error logs in `logs/app.log`.
