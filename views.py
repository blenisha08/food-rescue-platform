from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Food, Notification, User
from . import db

views = Blueprint('views', __name__)

# 🔔 Notification helpers
def create_notification(user_id, message, type):
    notif = Notification(user_id=user_id, message=message, type=type)
    db.session.add(notif)
    db.session.commit()

def notify_role(role, message, type):
    users = User.query.filter_by(role=role).all()
    for user in users:
        create_notification(user.id, message, type)

# 🏠 Home page
@views.route('/')
def home():
    return render_template('index.html')

# 🍽️ Food listing page
@views.route('/food')
def food():
    food_items = Food.query.all()
    return render_template('food.html', food_items=food_items)

# 🗺️ Map view
@views.route('/map')
def map_view():
    return render_template('map.html')

# 📝 Restaurant posts food + notify NGOs
@views.route('/food/post', methods=['POST'])
@login_required
def post_food():
    if current_user.role != 'Restaurant':
        return jsonify({'status': 'error', 'message': 'Only restaurants can post food!'})

    title = request.form.get('title')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    pickup = request.form.get('pickup')
    image_url = request.form.get('image_url')

    if not title or not pickup:
        return jsonify({'status': 'error', 'message': 'Title and pickup location are required!'})

    food = Food(
        title=title,
        description=description,
        quantity=quantity,
        pickup=pickup,
        restaurant=current_user.name,
        image_url=image_url
    )

    db.session.add(food)
    db.session.commit()

    # 🔔 Notify NGOs
    notify_role('Ngo', f"New food available from {current_user.name}", 'restaurant_offer')

    return jsonify({'status': 'success', 'message': 'Food posted and NGOs notified!'})

# 📬 Get current user's notifications
@views.route('/notifications')
@login_required
def get_notifications():
    notifs = current_user.notifications
    return jsonify([
        {
            'message': n.message,
            'type': n.type,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
        } for n in notifs
    ])
