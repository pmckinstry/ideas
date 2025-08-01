#!/usr/bin/env python3
"""
Flask Web Application Entry Point

This is the main entry point for the Flask application.
It uses the application factory pattern for better organization.
"""

import os

from app import create_app

# Create the Flask application instance
app = create_app()


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    from flask import render_template

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    from flask import render_template

    return render_template("500.html"), 500


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=5000)  # nosec B104
