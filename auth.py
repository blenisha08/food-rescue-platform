from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Generic signup route (keeps your existing functionality)
@auth.route('/signup/<role>', methods=['POST'])
def signup(role):
    role = role.capitalize()
    if role not in ['Ngo', 'Restaurant', 'Common']:
        return jsonify({'status': 'error', 'message': 'Invalid role!'})

    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # Validation
    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'})

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'})

    user = User(name=name, email=email, phone=phone, role=role)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'{role} registered successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'})

# Specific NGO signup route
@auth.route('/signup/ngo', methods=['POST'])
def signup_ngo():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # Validation
    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'})

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'})

    # Create NGO user using your existing User model
    user = User(name=name, email=email, phone=phone, role='Ngo')
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'NGO registered successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'})

# Specific Restaurant signup route
@auth.route('/signup/restaurant', methods=['POST'])
def signup_restaurant():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # Validation
    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'})

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'})

    # Create Restaurant user using your existing User model
    user = User(name=name, email=email, phone=phone, role='Restaurant')
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Restaurant registered successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'})

# Specific Common People signup route
@auth.route('/signup/common', methods=['POST'])
def signup_common():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # Validation
    if not all([name, email, phone, password]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'})

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered!'})

    # Create Common user using your existing User model
    user = User(name=name, email=email, phone=phone, role='Common')
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Registration completed successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'})

# Login route
@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required!'})
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'status': 'success', 
            'message': 'Logged in successfully!',
            'user': {
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })
    else:
        return jsonify({'status': 'error', 'message': 'Invalid email or password!'})

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logged out successfully!'})

# Get current user info (useful for frontend)
@auth.route('/user/current', methods=['GET'])
@login_required
def current_user():
    from flask_login import current_user as user
    return jsonify({
        'status': 'success',
        'user': {
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        }
    })

# Check if email exists (for validation)
@auth.route('/check-email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required!'})
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'status': 'exists', 'message': 'Email already registered!'})
    else:
        return jsonify({'status': 'available', 'message': 'Email is available!'})

# Password reset request (basic implementation)
@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')
    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required!'})
    
    user = User.query.filter_by(email=email).first()
    if user:
        # Here you would typically send a password reset email
        # For now, just return success
        return jsonify({'status': 'success', 'message': 'Password reset instructions sent to your email!'})
    else:
        return jsonify({'status': 'error', 'message': 'Email not found!'})