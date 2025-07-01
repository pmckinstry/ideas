from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models import authenticate_user, create_user, get_user_by_oauth, get_user_by_email
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.oauth_config import get_google_auth_url, get_google_token, get_google_user_info, is_google_oauth_enabled

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = create_user(form.username.data, form.email.data, form.password.data)
        login_user(user)
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile route"""
    return render_template('auth/profile.html', title='Profile')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password route"""
    # OAuth users can't change password through this form
    if current_user.oauth_provider:
        flash('OAuth users cannot change password through this form.', 'warning')
        return redirect(url_for('auth.profile'))
    
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Current password is incorrect.', 'danger')
    
    return render_template('auth/change_password.html', title='Change Password', form=form)

@auth_bp.route('/login/google')
def google_login():
    """Initiate Google OAuth login"""
    if not is_google_oauth_enabled():
        flash('Google OAuth is not configured.', 'warning')
        return redirect(url_for('auth.login'))
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    redirect_uri = url_for('auth.google_callback', _external=True)
    auth_url = get_google_auth_url(redirect_uri)
    return redirect(auth_url)

@auth_bp.route('/login/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    if not is_google_oauth_enabled():
        flash('Google OAuth is not configured.', 'warning')
        return redirect(url_for('auth.login'))
    
    error = request.args.get('error')
    if error:
        flash(f'Google OAuth error: {error}', 'danger')
        return redirect(url_for('auth.login'))
    
    code = request.args.get('code')
    if not code:
        flash('No authorization code received from Google.', 'danger')
        return redirect(url_for('auth.login'))
    
    try:
        # Exchange code for token
        redirect_uri = url_for('auth.google_callback', _external=True)
        token_data = get_google_token(code, redirect_uri)
        access_token = token_data.get('access_token')
        
        if not access_token:
            flash('Failed to get access token from Google.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Get user info from Google
        user_info = get_google_user_info(access_token)
        google_id = user_info.get('id')
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        
        # Check if user already exists
        user = get_user_by_oauth('google', google_id)
        if not user:
            # Check if email is already registered
            existing_user = get_user_by_email(email)
            if existing_user:
                flash('An account with this email already exists. Please login with your password.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Create new user
            user = create_user(name, email, None, 'google', google_id)
            flash('Account created successfully with Google!', 'success')
        else:
            flash('Welcome back!', 'success')
        
        # Login user
        login_user(user)
        return redirect(url_for('main.index'))
        
    except Exception as e:
        flash(f'Error during Google OAuth: {str(e)}', 'danger')
        return redirect(url_for('auth.login')) 