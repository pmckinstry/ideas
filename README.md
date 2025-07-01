# Flask Web App with Authentication

A modern, responsive web application built with Flask, featuring both traditional username/password authentication and Google OAuth integration.

## Features

- 🔐 **Dual Authentication**: Username/password + Google OAuth
- 👤 **User Management**: Registration, login, profile management
- 🗄️ **Database**: SQLite database with SQLAlchemy ORM
- 🔒 **Security**: Password hashing, CSRF protection, session management
- 📱 **Responsive Design**: Mobile-first Bootstrap 5 interface
- 🎨 **Modern UI**: Clean, professional design with animations
- 🔧 **API Endpoints**: RESTful API for testing and integration

## Quick Start

### 1. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///app.db

# Google OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

### 3. Google OAuth Setup (Optional)

To enable Google OAuth:

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:5000/login/google/callback` (development)
   - `https://yourdomain.com/login/google/callback` (production)
7. Copy the Client ID and Client Secret to your `.env` file

### 4. Initialize Database (First Time Only)

```bash
python manage.py init-db
```

### 5. Run the Application

```bash
python run.py
```

Visit [http://localhost:5000](http://localhost:5000)

## Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## Project Structure

```
├── run.py                 # Application entry point
├── manage.py              # Database management commands
├── app/                   # Main application package
│   ├── __init__.py        # Application factory
│   ├── config.py          # Configuration settings
│   ├── models.py          # User model and database functions
│   ├── forms.py           # WTForms for user input validation
│   ├── oauth_config.py    # Google OAuth configuration
│   ├── auth/              # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Auth routes (login, register, profile)
│   ├── main/              # Main application blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Core pages (index, about)
│   ├── api/               # API blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # REST API endpoints
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template with navigation
│   │   ├── auth/          # Authentication templates
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── profile.html
│   │   │   └── change_password.html
│   │   ├── main/          # Main page templates
│   │   │   ├── index.html
│   │   │   └── about.html
│   │   ├── 404.html       # Error page
│   │   └── 500.html       # Server error page
│   └── static/            # Static assets
│       ├── css/
│       │   └── style.css  # Custom styles
│       └── js/
│           └── main.js    # JavaScript utilities
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Authentication Flow

### Traditional Login
1. User registers with email/password
2. User logs in with credentials
3. Session is created and maintained

### Google OAuth
1. User clicks "Continue with Google"
2. Redirected to Google for authorization
3. Google returns authorization code
4. App exchanges code for access token
5. App fetches user info from Google
6. User is created/logged in automatically

## API Endpoints

- `GET /api/hello` - Simple hello message
- `GET /api/data` - Get sample data
- `POST /api/data` - Submit data (JSON)

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Secure OAuth flow with state validation
- Input validation and sanitization

## Development

### Adding New OAuth Providers

1. Add provider configuration to `oauth_config.py`
2. Create new routes in `app.py`
3. Update templates to include new provider buttons
4. Add provider-specific user creation logic

### Database Management

The app uses SQLite with SQLAlchemy ORM. Available commands:

```bash
# Initialize database tables
python manage.py init-db

# Seed database with initial data
python manage.py seed-db

# List all users
python manage.py list-users

# Delete a user
python manage.py delete-user <username>
```

### Database Integration

The app now uses SQLite database with SQLAlchemy ORM. For production:

1. Configure a production database (PostgreSQL, MySQL)
2. Update `DATABASE_URL` in environment
3. Run database migrations
4. Set up database backups

## Production Deployment

1. Set `FLASK_DEBUG=False`
2. Use a strong `SECRET_KEY`
3. Configure proper database
4. Set up HTTPS
5. Use production WSGI server (Gunicorn)
6. Configure reverse proxy (Nginx)

## License

MIT License - feel free to use this project as a starting point for your own applications! 