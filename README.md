# Ideas - Personal Thought Management System

A modern, responsive web application for capturing, organizing, and managing your thoughts and ideas. Built with Flask, featuring secure authentication, public/private thoughts, tagging, search functionality, and Google OAuth integration.

## ✨ Features

### 💭 Thought Management
- **Create & Edit**: Rich text thoughts with titles, content, categories, and tags
- **Organization**: Categorize thoughts (ideas, notes, inspiration, todos) with custom tags
- **Privacy Control**: Mark thoughts as public or private
- **Search**: Full-text search across titles, content, and tags
- **Tag Filtering**: Browse thoughts by specific tags
- **Pagination**: Efficient browsing of large thought collections

### 🔐 Authentication & Security
- **Dual Authentication**: Username/password + Google OAuth integration
- **User Management**: Registration, login, profile management, password changes
- **Security**: Password hashing, CSRF protection, session management
- **Access Control**: Private thoughts are only visible to their owners

### 🌐 Public Sharing
- **Public Thoughts**: Share selected thoughts publicly
- **Public Browse**: Explore public thoughts from all users
- **Tag Discovery**: Browse public thoughts by tags

### 🎨 User Experience
- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **Modern UI**: Clean, professional design with smooth interactions
- **Intuitive Navigation**: Easy-to-use interface for all features
- **Real-time Feedback**: Flash messages for user actions

### 🔧 Technical Features
- **RESTful API**: Basic API endpoints for integration
- **Database Migrations**: Alembic-powered database versioning
- **Testing Suite**: Comprehensive test coverage
- **Development Tools**: Code formatting, linting, and type checking

## 🚀 Quick Start

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

### 4. Initialize Database

```bash
python manage.py init-db
```

### 5. Run the Application

```bash
python run.py
```

Visit [http://localhost:5000](http://localhost:5000)

## 🔑 Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
├── run.py                 # Application entry point
├── manage.py              # Database management commands
├── app/                   # Main application package
│   ├── __init__.py        # Application factory
│   ├── models.py          # User and Thought models
│   ├── forms.py           # WTForms for validation
│   ├── oauth_config.py    # Google OAuth configuration
│   ├── auth/              # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Auth routes (login, register, profile)
│   ├── main/              # Main application blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Thought CRUD and main pages
│   ├── api/               # API blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Basic API endpoints
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template with navigation
│   │   ├── auth/          # Authentication templates
│   │   ├── main/          # Main page templates
│   │   │   ├── thoughts/  # Thought management templates
│   │   │   │   ├── list.html      # User's thoughts list
│   │   │   │   ├── public.html    # Public thoughts browse
│   │   │   │   ├── detail.html    # Thought detail view
│   │   │   │   ├── form.html      # Create/edit form
│   │   │   │   ├── search.html    # Search results
│   │   │   │   ├── tag.html       # User thoughts by tag
│   │   │   │   └── public_tag.html # Public thoughts by tag
│   │   │   ├── index.html
│   │   │   └── about.html
│   │   ├── 404.html       # Error pages
│   │   └── 500.html
│   └── static/            # Static assets
│       ├── css/style.css  # Custom styles
│       └── js/main.js     # JavaScript utilities
├── migrations/            # Database migrations
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 💭 Using the Thought System

### Creating Thoughts
1. Log in to your account
2. Navigate to "My Thoughts" → "New Thought"
3. Fill in title, content, category, and tags
4. Choose privacy setting (private/public)
5. Save your thought

### Organizing Thoughts
- **Categories**: Use predefined categories like 'idea', 'note', 'inspiration', 'todo'
- **Tags**: Add comma-separated tags for flexible organization
- **Search**: Use the search bar to find thoughts by content
- **Filter by Tags**: Click on any tag to see related thoughts

### Sharing Thoughts
- Mark thoughts as "Public" to share with others
- Public thoughts appear in the "Public Thoughts" section
- Others can browse your public thoughts by tags

## 🔌 API Endpoints

- `GET /api/hello` - Simple hello message
- `GET /api/data` - Get sample data
- `POST /api/data` - Submit data (JSON)

*Note: The API is currently basic. Future versions will include full CRUD operations for thoughts.*

## 🛠️ Development

### Database Management

Available management commands:

```bash
# Initialize database tables
python manage.py init-db

# Seed database with sample data
python manage.py seed-db

# List all users
python manage.py list-users

# Delete a user
python manage.py delete-user <username>
```

### Code Quality Tools

The project includes comprehensive development tools:

```bash
# Code formatting
make format

# Linting
make lint

# Type checking
make type-check

# Run tests
make test
```

### Database Migrations

Using Flask-Migrate for database versioning:

```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Downgrade migrations
flask db downgrade
```

## 🚀 Production Deployment

### Environment Setup
1. Set `FLASK_DEBUG=False`
2. Use a strong, unique `SECRET_KEY`
3. Configure a production database (PostgreSQL recommended)
4. Set up HTTPS with SSL certificates
5. Use a production WSGI server (Gunicorn)
6. Configure reverse proxy (Nginx)

### Database Configuration
For production, update your `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost/ideas_db
```

### Security Considerations
- Regular database backups
- Monitor for security updates
- Use environment variables for all secrets
- Enable proper logging and monitoring
- Consider rate limiting for API endpoints

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_basic_test.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

MIT License - feel free to use this project as a starting point for your own idea management system!

## 🎯 Future Enhancements

- **Rich Text Editor**: WYSIWYG editor for thought content
- **File Attachments**: Attach images and documents to thoughts
- **Collaboration**: Share thoughts with specific users
- **Export/Import**: Backup and restore thought collections
- **Mobile App**: Native mobile applications
- **Advanced Search**: Full-text search with filters and sorting
- **Thought Templates**: Predefined templates for different thought types
- **Analytics**: Insights into your thinking patterns and productivity
