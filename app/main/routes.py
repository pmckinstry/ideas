import random

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.main import main_bp
from app.models import (
    create_thought,
    delete_thought,
    get_public_thoughts,
    get_public_thoughts_by_tag,
    get_thought_by_id,
    get_thoughts_by_tag,
    get_user_thoughts,
    search_thoughts,
    update_thought,
)


def get_random_inspirational_quote():
    """Get a random inspirational quote"""
    quotes = [
        {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
        },
        {
            "text": "Innovation distinguishes between a leader and a follower.",
            "author": "Steve Jobs",
        },
        {
            "text": "Your time is limited, don't waste it living someone else's life.",
            "author": "Steve Jobs",
        },
        {
            "text": "The future belongs to those who believe in the beauty of their dreams.",
            "author": "Eleanor Roosevelt",
        },
        {
            "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "author": "Winston Churchill",
        },
        {
            "text": "The mind is everything. What you think you become.",
            "author": "Buddha",
        },
        {
            "text": "The best way to predict the future is to create it.",
            "author": "Peter Drucker",
        },
        {
            "text": "Don't watch the clock; do what it does. Keep going.",
            "author": "Sam Levenson",
        },
        {
            "text": "The only limit to our realization of tomorrow is our doubts of today.",
            "author": "Franklin D. Roosevelt",
        },
        {
            "text": "What you get by achieving your goals is not as important as what you become by achieving your goals.",
            "author": "Zig Ziglar",
        },
        {
            "text": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
            "author": "Nelson Mandela",
        },
        {
            "text": "Life is what happens when you're busy making other plans.",
            "author": "John Lennon",
        },
        {
            "text": "The way to get started is to quit talking and begin doing.",
            "author": "Walt Disney",
        },
        {
            "text": "It is during our darkest moments that we must focus to see the light.",
            "author": "Aristotle",
        },
        {
            "text": "Whoever is happy will make others happy too.",
            "author": "Anne Frank",
        },
    ]
    return random.choice(quotes)


@main_bp.route("/")
def index():
    """Main page route"""
    inspirational_quote = get_random_inspirational_quote()
    return render_template(
        "main/index.html", title="Welcome to Ideas", quote=inspirational_quote
    )


@main_bp.route("/about")
def about():
    """About page route"""
    return render_template("main/about.html", title="About")


# Thought CRUD routes
@main_bp.route("/thoughts")
@login_required
def thoughts_list():
    """List all thoughts for the current user"""
    page = request.args.get("page", 1, type=int)
    per_page = 10

    # Get thoughts with database-level pagination
    pagination = get_user_thoughts(current_user.id, page=page, per_page=per_page)

    return render_template(
        "main/thoughts/list.html",
        thoughts=pagination.items,
        pagination=pagination,
        page=page,
        per_page=per_page,
        title="My Thoughts",
    )


@main_bp.route("/thoughts/public")
def public_thoughts():
    """List all public thoughts"""
    page = request.args.get("page", 1, type=int)
    per_page = 10

    # Get public thoughts with database-level pagination
    pagination = get_public_thoughts(page=page, per_page=per_page)

    return render_template(
        "main/thoughts/public.html",
        thoughts=pagination.items,
        pagination=pagination,
        page=page,
        per_page=per_page,
        title="Public Thoughts",
    )


@main_bp.route("/thoughts/new", methods=["GET", "POST"])
@login_required
def thought_create():
    """Create a new thought"""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip()
        tags = request.form.get("tags", "").strip()
        is_public = request.form.get("is_public") == "on"

        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template("main/thoughts/form.html", title="New Thought")

        try:
            thought = create_thought(
                title=title,
                content=content,
                user_id=current_user.id,
                category=category if category else None,
                tags=tags if tags else None,
                is_public=is_public,
            )
            flash("Thought created successfully!", "success")
            return redirect(url_for("main.thought_detail", thought_id=thought.id))
        except Exception as e:
            flash(f"Error creating thought: {str(e)}", "error")

    return render_template("main/thoughts/form.html", title="New Thought")


@main_bp.route("/thoughts/<thought_id>")
def thought_detail(thought_id):
    """View a specific thought"""
    thought = get_thought_by_id(thought_id)
    if not thought:
        flash("Thought not found.", "error")
        return redirect(url_for("main.thoughts_list"))

    # Check if user can view this thought
    if not thought.is_public and (
        not current_user.is_authenticated or thought.user_id != current_user.id
    ):
        flash("You don't have permission to view this thought.", "error")
        return redirect(url_for("main.thoughts_list"))

    return render_template(
        "main/thoughts/detail.html", thought=thought, title=thought.title
    )


@main_bp.route("/thoughts/<thought_id>/edit", methods=["GET", "POST"])
@login_required
def thought_edit(thought_id):
    """Edit a thought"""
    thought = get_thought_by_id(thought_id)
    if not thought:
        flash("Thought not found.", "error")
        return redirect(url_for("main.thoughts_list"))

    # Check if user owns this thought
    if thought.user_id != current_user.id:
        flash("You don't have permission to edit this thought.", "error")
        return redirect(url_for("main.thoughts_list"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip()
        tags = request.form.get("tags", "").strip()
        is_public = request.form.get("is_public") == "on"

        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template(
                "main/thoughts/form.html", thought=thought, title="Edit Thought"
            )

        try:
            update_thought(
                thought_id=thought.id,
                title=title,
                content=content,
                category=category if category else None,
                tags=tags if tags else None,
                is_public=is_public,
            )
            flash("Thought updated successfully!", "success")
            return redirect(url_for("main.thought_detail", thought_id=thought.id))
        except Exception as e:
            flash(f"Error updating thought: {str(e)}", "error")

    return render_template(
        "main/thoughts/form.html", thought=thought, title="Edit Thought"
    )


@main_bp.route("/thoughts/<thought_id>/delete", methods=["POST"])
@login_required
def thought_delete(thought_id):
    """Delete a thought"""
    thought = get_thought_by_id(thought_id)
    if not thought:
        flash("Thought not found.", "error")
        return redirect(url_for("main.thoughts_list"))

    # Check if user owns this thought
    if thought.user_id != current_user.id:
        flash("You don't have permission to delete this thought.", "error")
        return redirect(url_for("main.thoughts_list"))

    try:
        delete_thought(thought_id)
        flash("Thought deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting thought: {str(e)}", "error")

    return redirect(url_for("main.thoughts_list"))


@main_bp.route("/thoughts/search")
@login_required
def thought_search():
    """Search thoughts"""
    query = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 10

    if not query:
        return redirect(url_for("main.thoughts_list"))

    # Search thoughts with database-level pagination
    pagination = search_thoughts(current_user.id, query, page=page, per_page=per_page)

    return render_template(
        "main/thoughts/search.html",
        thoughts=pagination.items,
        pagination=pagination,
        query=query,
        page=page,
        per_page=per_page,
        title=f"Search Results for '{query}'",
    )


@main_bp.route("/thoughts/tag/<tag>")
@login_required
def thoughts_by_tag(tag):
    """List thoughts filtered by a specific tag for the current user"""
    page = request.args.get("page", 1, type=int)
    per_page = 10

    # Get thoughts by tag with database-level pagination
    pagination = get_thoughts_by_tag(current_user.id, tag, page=page, per_page=per_page)

    return render_template(
        "main/thoughts/tag.html",
        thoughts=pagination.items,
        pagination=pagination,
        tag=tag,
        page=page,
        per_page=per_page,
        title=f"Thoughts tagged '{tag}'",
    )


@main_bp.route("/thoughts/public/tag/<tag>")
def public_thoughts_by_tag(tag):
    """List public thoughts filtered by a specific tag"""
    page = request.args.get("page", 1, type=int)
    per_page = 10

    # Get public thoughts by tag with database-level pagination
    pagination = get_public_thoughts_by_tag(tag, page=page, per_page=per_page)

    return render_template(
        "main/thoughts/public_tag.html",
        thoughts=pagination.items,
        pagination=pagination,
        tag=tag,
        page=page,
        per_page=per_page,
        title=f"Public thoughts tagged '{tag}'",
    )
