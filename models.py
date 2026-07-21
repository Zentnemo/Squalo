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
    city = db.Column(db.String(128), default='Berlin')
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
    confirmation_email_sent_at = db.Column(db.DateTime, nullable=True)
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
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(128))
    title = db.Column(db.String(200))
    bio = db.Column(db.Text)
    strengths = db.Column(db.Text)
    swim_style = db.Column(db.Text)
    experience = db.Column(db.Text)
    specialization = db.Column(db.String(200))
    cities_served = db.Column(db.Text)  # comma-separated, e.g. "Berlin,Potsdam"
    image_url = db.Column(db.String(500))
    external_profile_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def cities_list(self):
        """Return cities as a list, parsed from comma-separated string."""
        if self.cities_served:
            return [c.strip() for c in self.cities_served.split(',') if c.strip()]
        return []

    @property
    def display_name(self):
        """Return composed name if first/last available, else full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.name


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


class Invoice(db.Model):
    """A single invoice for one booked swimming session."""
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(32), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, default=50.0)
    currency = db.Column(db.String(8), default='EUR')
    status = db.Column(db.String(32), default='issued')  # issued / paid / void
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_generated_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref='invoices')
    booking = db.relationship('Booking', backref='invoices')

    @staticmethod
    def next_number(year=None):
        """Generate next sequential invoice number: SQ-YYYY-NNNN"""
        if year is None:
            year = datetime.utcnow().year
        prefix = f'SQ-{year}-'
        last = Invoice.query.filter(
            Invoice.invoice_number.like(f'{prefix}%')
        ).order_by(Invoice.invoice_number.desc()).first()
        if last:
            try:
                num = int(last.invoice_number.split('-')[-1]) + 1
            except (ValueError, IndexError):
                num = 1
        else:
            num = 1
        return f'{prefix}{num:04d}'


class SiteSession(db.Model):
    """Lightweight visitor session tracker for the coach panel dashboard.

    Stores minimal, privacy-respecting data:
    - anonymous session ID (from Flask session)
    - user ID (only if logged in)
    - first_seen / last_seen timestamps
    - last visited path
    - role hint (student / admin)
    """
    __tablename__ = 'site_session'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_authenticated = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(32), default='guest')  # guest / student / admin
    last_path = db.Column(db.String(256), default='/')
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ShopOrder(db.Model):
    """A shop equipment order / reservation for the next training session."""
    __tablename__ = 'shop_order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    customer_name = db.Column(db.String(128), nullable=False)
    customer_email = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(32), default='requested')  # requested / confirmed / brought_to_training / cancelled
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='shop_orders')
    items = db.relationship('ShopOrderItem', backref='order', lazy=True, cascade='all, delete-orphan')


class ShopOrderItem(db.Model):
    """A single item within a shop order."""
    __tablename__ = 'shop_order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('shop_order.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_category = db.Column(db.String(128), nullable=True)
    product_link = db.Column(db.String(512), nullable=True)
    quantity = db.Column(db.Integer, default=1)


class CoachApplication(db.Model):
    """A coach application submitted via the /coach-werden landing page."""
    __tablename__ = 'coach_application'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(40))
    city_region = db.Column(db.String(128), nullable=False)
    languages = db.Column(db.Text)
    swim_experience = db.Column(db.Text, nullable=False)
    coaching_experience = db.Column(db.Text)
    licenses = db.Column(db.Text)
    preferred_locations = db.Column(db.Text)
    target_groups = db.Column(db.Text)
    availability = db.Column(db.Text)
    motivation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentFile(db.Model):
    """A file uploaded by a coach for a student – lesson log or training plan PDF."""
    __tablename__ = 'student_file'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True, index=True)
    file_type = db.Column(db.String(32), nullable=False)  # 'lesson_log' | 'training_plan'
    title = db.Column(db.String(256), nullable=False)
    topic = db.Column(db.String(512), nullable=True)
    original_filename = db.Column(db.String(256), nullable=False)
    mime_type = db.Column(db.String(64), nullable=False, default='application/pdf')
    file_size = db.Column(db.Integer, nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_current_plan = db.Column(db.Boolean, default=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='student_files')
    uploaded_by = db.relationship('User', foreign_keys=[uploaded_by_id])
    booking = db.relationship('Booking', foreign_keys=[booking_id], backref='lesson_logs')

