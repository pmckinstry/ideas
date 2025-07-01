from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.main import main_bp
from app.models import (
    create_thought,
    delete_thought,
    get_public_thoughts,
    get_thought_by_id,
    get_user_thoughts,
    search_thoughts,
    update_thought,
)


@main_bp.route("/")
def index():
    """Main page route"""
    return render_template("main/index.html", title="Welcome to Ideas")


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

    # Get thoughts with pagination
    thoughts = get_user_thoughts(current_user.id)
    total = len(thoughts)
    thoughts = thoughts[(page - 1) * per_page : page * per_page]

    return render_template(
        "main/thoughts/list.html",
        thoughts=thoughts,
        page=page,
        total=total,
        per_page=per_page,
        title="My Thoughts",
    )


@main_bp.route("/thoughts/public")
def public_thoughts():
    """List all public thoughts"""
    page = request.args.get("page", 1, type=int)
    per_page = 10

    thoughts = get_public_thoughts()
    total = len(thoughts)
    thoughts = thoughts[(page - 1) * per_page : page * per_page]

    return render_template(
        "main/thoughts/public.html",
        thoughts=thoughts,
        page=page,
        total=total,
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
    if not query:
        return redirect(url_for("main.thoughts_list"))

    thoughts = search_thoughts(current_user.id, query)

    return render_template(
        "main/thoughts/search.html",
        thoughts=thoughts,
        query=query,
        title=f"Search Results for '{query}'",
    )
