import uuid
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):  # type: ignore[name-defined]
    """User model for authentication and profile management"""

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    oauth_provider = db.Column(db.String(50))  # 'google', 'github', etc.
    oauth_id = db.Column(db.String(255))  # OAuth provider's user ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean, default=True)

    def __init__(
        self, username, email, password=None, oauth_provider=None, oauth_id=None
    ):
        self.username = username
        self.email = email
        self.oauth_provider = oauth_provider
        self.oauth_id = oauth_id
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "oauth_provider": self.oauth_provider,
            "oauth_id": self.oauth_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"<User {self.username}>"


# Database helper functions
def create_user(username, email, password=None, oauth_provider=None, oauth_id=None):
    """Create a new user"""
    user = User(
        username=username,
        email=email,
        password=password,
        oauth_provider=oauth_provider,
        oauth_id=oauth_id,
    )
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)


def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()


def get_user_by_oauth(oauth_provider, oauth_id):
    """Get user by OAuth provider and ID"""
    return User.query.filter_by(
        oauth_provider=oauth_provider, oauth_id=oauth_id
    ).first()


def authenticate_user(username, password):
    """Authenticate user with username and password"""
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None


def init_default_user():
    """Initialize a default admin user if no users exist"""
    if User.query.count() == 0:
        admin_user = create_user("admin", "admin@example.com", "admin123")
        print(f"Created default admin user: {admin_user.username}")
        return admin_user
    return None
