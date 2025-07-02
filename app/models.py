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


class Thought(db.Model):  # type: ignore[name-defined]
    """Thought model for storing ideas and thoughts"""

    __tablename__ = "thoughts"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # e.g., 'idea', 'note', 'inspiration', 'todo'
    tags = db.Column(db.String(500))  # comma-separated tags
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Foreign key to User
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("thoughts", lazy=True))

    def __init__(
        self, title, content, user_id, category=None, tags=None, is_public=False
    ):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.category = category
        self.tags = tags
        self.is_public = is_public

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": [tag.strip() for tag in self.tags.split(",")] if self.tags else [],
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
        }

    def __repr__(self):
        return f"<Thought {self.title}>"


# Thought helper functions
def create_thought(title, content, user_id, category=None, tags=None, is_public=False):
    """Create a new thought"""
    thought = Thought(
        title=title,
        content=content,
        user_id=user_id,
        category=category,
        tags=tags,
        is_public=is_public,
    )
    db.session.add(thought)
    db.session.commit()
    return thought


def get_thought_by_id(thought_id):
    """Get thought by ID"""
    return Thought.query.get(thought_id)


def get_user_thoughts(user_id, page=1, per_page=10):
    """Get thoughts for a user with pagination"""
    query = Thought.query.filter_by(user_id=user_id).order_by(Thought.created_at.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_public_thoughts(page=1, per_page=10):
    """Get public thoughts with pagination"""
    query = Thought.query.filter_by(is_public=True).order_by(Thought.created_at.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)


def update_thought(
    thought_id, title=None, content=None, category=None, tags=None, is_public=None
):
    """Update a thought"""
    thought = get_thought_by_id(thought_id)
    if thought:
        if title is not None:
            thought.title = title
        if content is not None:
            thought.content = content
        if category is not None:
            thought.category = category
        if tags is not None:
            thought.tags = tags
        if is_public is not None:
            thought.is_public = is_public
        db.session.commit()
    return thought


def delete_thought(thought_id):
    """Delete a thought"""
    thought = get_thought_by_id(thought_id)
    if thought:
        db.session.delete(thought)
        db.session.commit()
        return True
    return False


def search_thoughts(user_id, query, page=1, per_page=10):
    """Search thoughts by title or content with pagination"""
    search_term = f"%{query}%"
    query_filter = Thought.query.filter(
        Thought.user_id == user_id,
        db.or_(
            Thought.title.ilike(search_term),
            Thought.content.ilike(search_term),
            Thought.tags.ilike(search_term),
        ),
    ).order_by(Thought.created_at.desc())

    return query_filter.paginate(page=page, per_page=per_page, error_out=False)


def get_thoughts_by_tag(user_id, tag, page=1, per_page=10):
    """Get thoughts filtered by a specific tag for a user"""
    tag_pattern = f"%{tag}%"
    query_filter = Thought.query.filter(
        Thought.user_id == user_id, Thought.tags.ilike(tag_pattern)
    ).order_by(Thought.created_at.desc())

    return query_filter.paginate(page=page, per_page=per_page, error_out=False)


def get_public_thoughts_by_tag(tag, page=1, per_page=10):
    """Get public thoughts filtered by a specific tag"""
    tag_pattern = f"%{tag}%"
    query_filter = Thought.query.filter(
        Thought.is_public.is_(True), Thought.tags.ilike(tag_pattern)
    ).order_by(Thought.created_at.desc())

    return query_filter.paginate(page=page, per_page=per_page, error_out=False)
