from flask import render_template
from app.main import main_bp

@main_bp.route('/')
def index():
    """Main page route"""
    return render_template('main/index.html', title='Welcome to My Web App')

@main_bp.route('/about')
def about():
    """About page route"""
    return render_template('main/about.html', title='About') 