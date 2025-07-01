import os
import random
import sys
from datetime import datetime, timedelta

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # nosec

from app import create_app  # noqa: E402
from app.models import Thought, User, db  # noqa: E402

app = create_app()

sample_categories = ["idea", "note", "inspiration", "todo", "question", "project"]
sample_tags = [
    "python",
    "flask",
    "web",
    "ai",
    "ml",
    "fun",
    "test",
    "sample",
    "public",
    "demo",
]

sample_titles = [f"Sample Thought #{i+1}" for i in range(25)]
sample_contents = [
    f"This is the content for sample thought number {i+1}.\nIt is public and generated for pagination testing."
    for i in range(25)
]


def get_or_create_test_user():
    user = User.query.first()
    if not user:
        user = User(
            username="testuser", email="testuser@example.com", password="test1234"
        )
        db.session.add(user)
        db.session.commit()
    return user


def main():
    with app.app_context():
        user = get_or_create_test_user()
        # Remove existing sample thoughts for a clean test
        Thought.query.filter(Thought.title.like("Sample Thought #%")).delete(
            synchronize_session=False
        )
        db.session.commit()
        for i in range(25):
            thought = Thought(
                title=sample_titles[i],
                content=sample_contents[i],
                user_id=user.id,
                category=random.choice(sample_categories),
                tags=", ".join(random.sample(sample_tags, k=3)),
                is_public=True,
            )
            thought.created_at = datetime.utcnow() - timedelta(days=25 - i)
            thought.updated_at = datetime.utcnow() - timedelta(days=25 - i)
            db.session.add(thought)
        db.session.commit()
        print("25 sample public thoughts created for user:", user.username)


if __name__ == "__main__":
    main()
