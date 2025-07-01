#!/usr/bin/env python3
"""
Database Management Script

This script provides commands for database operations like migrations,
seeding, and maintenance.
"""

import click
from app import create_app
from app.models import db, User

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        click.echo('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed the database with initial data."""
    with app.app_context():
        # Create admin user if it doesn't exist
        if User.query.filter_by(username='admin').first() is None:
            from app.models import create_user
            admin_user = create_user('admin', 'admin@example.com', 'admin123')
            click.echo(f'Created admin user: {admin_user.username}')
        else:
            click.echo('Admin user already exists.')
        
        click.echo('Database seeded!')

@app.cli.command()
def list_users():
    """List all users in the database."""
    with app.app_context():
        users = User.query.all()
        if users:
            click.echo('Users in database:')
            for user in users:
                click.echo(f'  - {user.username} ({user.email}) - Created: {user.created_at}')
        else:
            click.echo('No users found in database.')

@app.cli.command()
@click.argument('username')
def delete_user(username):
    """Delete a user by username."""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            click.echo(f'Deleted user: {username}')
        else:
            click.echo(f'User not found: {username}')

if __name__ == '__main__':
    app.cli() 