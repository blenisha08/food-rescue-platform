from flask import Blueprint, render_template
from .models import Food
from .models import Notification, User
from . import db
def create_notification(user_id, message, type):
    notif = Notification(user_id=user_id, message=message, type=type)
    db.session.add(notif)
    db.session.commit()

def notify_role(role, message, type):
    users = User.query.filter_by(role=role).all()
    for user in users:
        create_notification(user.id, message, type)


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/food')
def food():
    # Fetch food items from database
    food_items = Food.query.all()
    return render_template('food.html', food_items=food_items)

@views.route('/map')
def map_view():
    return render_template('map.html')
