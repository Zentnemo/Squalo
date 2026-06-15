from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location_type = db.Column(db.String(64))
    address = db.Column(db.String(256))
    district = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    official_status = db.Column(db.String(64))
    verified_status = db.Column(db.String(64))
    water_temperature = db.Column(db.String(64))
    crowd_level = db.Column(db.String(64))
    maps_url = db.Column(db.String(512))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(128))
    description = db.Column(db.Text)
    price_label = db.Column(db.String(128))
    variant_label = db.Column(db.String(128))
    note = db.Column(db.Text)
    image_path = db.Column(db.String(512))
    button_label = db.Column(db.String(64), default="Anfragen")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Legacy fields kept for backward compat
    price = db.Column(db.Float)
    external_url = db.Column(db.String(512))


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Priority: time, location, balanced
    priority_type = db.Column(db.String(32), default='balanced')
    # Time options (1 required, 2+3 optional)
    date_option_1 = db.Column(db.Date)
    time_option_1 = db.Column(db.Time)
    date_option_2 = db.Column(db.Date)
    time_option_2 = db.Column(db.Time)
    date_option_3 = db.Column(db.Date)
    time_option_3 = db.Column(db.Time)
    # Legacy single datetime (kept for backward compat)
    requested_start = db.Column(db.DateTime)
    # Location preferences
    preferred_location_1_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    preferred_location_2_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    preferred_location_3_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    # Confirmed by coach
    confirmed_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    confirmed_date = db.Column(db.Date)
    confirmed_time = db.Column(db.Time)
    # Details
    training_goal = db.Column(db.String(128))
    user_note = db.Column(db.Text)
    admin_note = db.Column(db.Text)
    # Duration & pricing
    duration_minutes = db.Column(db.Integer, default=60)
    duration_slots = db.Column(db.Integer, default=2)
    estimated_price = db.Column(db.Float, default=50.0)
    # Coach preference
    preferred_coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=True)
    status = db.Column(db.String(32), default='angefragt')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    preferred_location_1 = db.relationship('Location', foreign_keys=[preferred_location_1_id])
    preferred_location_2 = db.relationship('Location', foreign_keys=[preferred_location_2_id])
    preferred_location_3 = db.relationship('Location', foreign_keys=[preferred_location_3_id])
    confirmed_location = db.relationship('Location', foreign_keys=[confirmed_location_id])
    preferred_coach = db.relationship('Coach', foreign_keys=[preferred_coach_id])


class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    title = db.Column(db.String(200))
    bio = db.Column(db.Text)
    strengths = db.Column(db.Text)
    swim_style = db.Column(db.Text)
    experience = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    external_profile_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CoachReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    source = db.Column(db.String(80), default='squalo')
    author_name = db.Column(db.String(120))
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coach = db.relationship('Coach', backref='reviews')
    user = db.relationship('User', backref='reviews')


class FeedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text)
    image_path = db.Column(db.String(512))
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='feed_posts')


class TrainingNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AppSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), unique=True, nullable=False)
    value = db.Column(db.Text)

    @staticmethod
    def get(key, default=None):
        s = AppSetting.query.filter_by(key=key).first()
        return s.value if s else default

    @staticmethod
    def set(key, value):
        s = AppSetting.query.filter_by(key=key).first()
        if s:
            s.value = value
        else:
            s = AppSetting(key=key, value=value)
            db.session.add(s)
        db.session.commit()

