"""Minimal Squalo Flask application (clean single-file app factory).

Provides small runnable Flask app that re-uses project's models and templates.
Includes minimal auth (register/login), required pages and CLI helpers.
"""

import io
import os
import smtplib
import time as time_mod
from datetime import datetime, date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zoneinfo import ZoneInfo
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file, Response, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pathlib import Path

from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from models import db, User, Location, Booking, FeedPost, TrainingNote, AppSetting, Coach, CoachReview, SiteSession, Invoice, ShopOrder, ShopOrderItem
from location_status import compute_location_status

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


# ── Shop products (MVP – hardcoded for now) ───────────────────────
SHOP_PRODUCTS = [
    # ── Schwimmbrillen ──
    {
        "id": "brille-arena-cobra",
        "name": "Arena Cobra Swipe Gold",
        "category": "Schwimmbrillen",
        "description": "Premium verspiegelte Wettkampfbrille für ambitioniertes und sportliches Schwimmen. Hervorragende Sicht unter Wasser.",
        "link": "https://www.decathlon.de/p/schwimmbrille-verspiegelt-arena-cobra-swipe-gold/X8653040/c1m8653040",
        "image": "images/shop/brille-arena-cobra-gold.png",
        "price": 45.0,
        "note": "",
    },
    {
        "id": "brille-speedo-biofuse",
        "name": "Speedo Biofuse 2.0 Schwimmbrille",
        "category": "Schwimmbrillen",
        "description": "Komfortable Schwimmbrille mit getönten Gläsern. Gute Allround-Option für regelmäßiges Training.",
        "link": "https://www.decathlon.de/p/schwimmbrille-speedo-getont-biofuse-2-0-schwarz/X8815095/c1m8815095",
        "image": "images/shop/brille-speedo-biofuse-black.png",
        "price": 25.0,
        "note": "",
    },
    # ── Flossen & Handpaddles ──
    {
        "id": "flossen-silifins",
        "name": "Schwimmflossen",
        "category": "Flossen & Handpaddles",
        "description": "Kurze Schwimmflossen für Techniktraining, Beinschlag und Wasserlage. Gut geeignet für Kraultechnik und erste Technikübungen im Training.",
        "link": "https://www.decathlon.de/p/schwimmflossen-silifins-blau-gelb/122646/c209c86c132m8574328",
        "image": "images/shop/flossen-black.png",
        "price": 25.0,
        "note": "",
    },
    {
        "id": "flossen-handpaddles",
        "name": "Handpaddles",
        "category": "Flossen & Handpaddles",
        "description": "Trainingshilfe für Wassergefühl, Armzug und Druckphase. Nur nach Absprache im Training verwenden.",
        "link": "",
        "image": "images/shop/handpaddles-black.png",
        "price": 30.0,
        "note": "Link wird ergänzt",
    },
    # ── Trainingsausrüstung ──
    {
        "id": "trainig-pullbuoy",
        "name": "Pullbuoy",
        "category": "Trainingsausrüstung",
        "description": "Pullbuoy für Techniktraining, Wasserlage und isoliertes Armtraining. Besonders hilfreich für Kraultechnik und Triathlontraining.",
        "link": "https://www.decathlon.de/p/pull-buoy-grosse-m-500-schwarz-gelb/336080/c382c132m8666065",
        "image": "images/shop/pullbuoy-black-yellow.png",
        "price": 10.0,
        "note": "",
    },
    {
        "id": "trainig-schwimmbrett",
        "name": "Schwimmbrett",
        "category": "Trainingsausrüstung",
        "description": "Klassisches Schwimmbrett für Beinschlagtraining, Technikübungen und Wasserlage.",
        "link": "https://www.decathlon.de/p/schwimmbrett-blau/351550/c195m8853957",
        "image": "images/shop/schwimmbrett-blue.png",
        "price": 10.0,
        "note": "",
    },
]


# ── Confirmed-status helpers ──────────────────────────────────────
CONFIRMED_STATUSES = ('bestaetigt', 'bestätigt', 'confirmed', 'accepted', 'angenommen')


def is_confirmed_status(status):
    """Return True if *status* counts as a confirmed/accepted booking."""
    return (status or '').lower() in CONFIRMED_STATUSES


def get_effective_date(booking):
    """Return the best available date for a booking.

    Priority: confirmed_date → date_option_1 → requested_start.date()
    Returns None only if all are missing.
    """
    if booking.confirmed_date:
        return booking.confirmed_date
    if booking.date_option_1:
        return booking.date_option_1
    if booking.requested_start:
        return booking.requested_start.date() if hasattr(booking.requested_start, 'date') else booking.requested_start
    return None


def get_effective_time(booking):
    """Return the best available time for a booking.

    Priority: confirmed_time → time_option_1 → requested_start.time()
    Returns None only if all are missing.
    """
    if booking.confirmed_time:
        return booking.confirmed_time
    if booking.time_option_1:
        return booking.time_option_1
    if booking.requested_start:
        return booking.requested_start.time() if hasattr(booking.requested_start, 'time') else None
    return None

# ── Default admin email ───────────────────────────────────────────
DEFAULT_ADMIN_EMAIL = "zentner.moritz@gmail.com"


def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_admin_email():
    """Return the admin notification email from settings or env, with fallback."""
    return (
        os.environ.get("BOOKING_NOTIFICATION_EMAIL")
        or AppSetting.get("booking_notification_email")
        or DEFAULT_ADMIN_EMAIL
    )


def send_email(subject, recipient, body_text, body_html=None):
    """Send an email via SMTP. Falls back to console logging if SMTP is not configured.

    SMTP is configured via environment variables:
        MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS, MAIL_DEFAULT_SENDER
    If none are set, the email is printed to the console (development mode).
    """
    mail_server = os.environ.get("MAIL_SERVER")
    mail_port = int(os.environ.get("MAIL_PORT", "587"))
    mail_username = os.environ.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD")
    mail_use_tls = os.environ.get("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
    mail_sender = os.environ.get("MAIL_DEFAULT_SENDER", mail_username or "noreply@squalo.app")

    if not mail_server or not mail_username or not mail_password:
        # ── Console fallback (development) ──
        print("\n" + "=" * 60)
        print(f"SIMULIERTE E-MAIL (kein SMTP konfiguriert)")
        print(f"Von:    {mail_sender}")
        print(f"An:     {recipient}")
        print(f"Betreff: {subject}")
        print("-" * 60)
        print(body_text)
        if body_html:
            print("-" * 60)
            print("[HTML-Version verfügbar, wird in Konsole nicht angezeigt]")
        print("=" * 60 + "\n")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = mail_sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain", "utf-8"))
        if body_html:
            msg.attach(MIMEText(body_html, "html", "utf-8"))

        with smtplib.SMTP(mail_server, mail_port, timeout=15) as server:
            if mail_use_tls:
                server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(mail_sender, [recipient], msg.as_string())
        print(f"[MAIL] E-Mail gesendet an {recipient}: {subject}")
        return True
    except Exception as e:
        print(f"[MAIL-FEHLER] Konnte E-Mail nicht senden: {e}")
        # Fallback: log the email content so it's not lost
        print(f"  Betreff: {subject}")
        print(f"  An: {recipient}")
        print(f"  Text: {body_text[:300]}")
        return False


def send_booking_notification(booking):
    """Send admin notification when a new booking request is submitted."""
    admin_email = get_admin_email()
    user = User.query.get(booking.user_id)
    subject = AppSetting.get('tpl_new_subject', 'Neue Squalo-Terminanfrage')

    time_options = []
    if booking.date_option_1:
        t1 = booking.time_option_1.strftime('%H:%M') if booking.time_option_1 else '?'
        time_options.append(f"  - {booking.date_option_1.strftime('%d.%m.%Y')} {t1} Uhr")
    if booking.date_option_2:
        t2 = booking.time_option_2.strftime('%H:%M') if booking.time_option_2 else '?'
        time_options.append(f"  - {booking.date_option_2.strftime('%d.%m.%Y')} {t2} Uhr")
    if booking.date_option_3:
        t3 = booking.time_option_3.strftime('%H:%M') if booking.time_option_3 else '?'
        time_options.append(f"  - {booking.date_option_3.strftime('%d.%m.%Y')} {t3} Uhr")
    if not time_options and booking.requested_start:
        time_options.append(f"  - {booking.requested_start.strftime('%d.%m.%Y %H:%M')} Uhr")

    locs = []
    for lid in [booking.preferred_location_1_id, booking.preferred_location_2_id, booking.preferred_location_3_id]:
        if lid:
            loc = Location.query.get(lid)
            if loc:
                locs.append(loc.name)

    duration_map = {30: "30 Min", 60: "1 Std", 90: "1,5 Std", 120: "2 Std",
                    180: "3 Std", 240: "4 Std", 300: "5 Std (Paket)"}
    duration_str = duration_map.get(booking.duration_minutes, f"{booking.duration_minutes} Min")

    body = _render_template_from_settings('tpl_new_body',
        name=user.name if user else 'unbekannt',
        email=user.email if user else 'unbekannt',
        zeitoptionen=chr(10).join(time_options) if time_options else '  keine',
        wunschorte=', '.join(locs) if locs else 'keine',
        coach=booking.preferred_coach.name if booking.preferred_coach else 'egal',
        dauer=duration_str,
        ziel=booking.training_goal or 'keines',
        notiz=booking.user_note or 'keine',
        preis=f"{int(booking.estimated_price)} €",
    ) or _default_tpl_new().replace('{{name}}', user.name if user else 'unbekannt')

    send_email(subject, admin_email, body)


def send_customer_confirmation_email(booking, force=False):
    """Send customer email when a booking is confirmed.

    Tracks confirmation_email_sent_at to prevent duplicate sends.
    Use force=True to resend (not yet exposed in UI, but safe if called).
    Returns True if email was sent (or already sent), False on failure.
    """
    # ── Duplicate protection ──
    if booking.confirmation_email_sent_at and not force:
        print(f"[MAIL] Bestaetigungsmail fuer Booking #{booking.id} bereits gesendet "
              f"({booking.confirmation_email_sent_at.strftime('%d.%m.%Y %H:%M')}). "
              f"Ueberspringe.")
        return True

    user = User.query.get(booking.user_id)
    if not user or not user.email:
        print(f"[MAIL] Booking #{booking.id}: Kein gueltiger User/E-Mail gefunden. "
              f"Ueberspringe.")
        return False

    # ── Resolve effective date/time/location ──
    eff_date = booking.confirmed_date or booking.date_option_1 or (
        booking.requested_start.date() if booking.requested_start else None
    )
    eff_time = booking.confirmed_time or booking.time_option_1 or (
        booking.requested_start.time() if booking.requested_start else None
    )
    eff_location = None
    if booking.confirmed_location_id:
        loc = Location.query.get(booking.confirmed_location_id)
        if loc:
            eff_location = loc.name
    if not eff_location and booking.preferred_location_1_id:
        loc = Location.query.get(booking.preferred_location_1_id)
        if loc:
            eff_location = loc.name

    coach_name = 'Moritz'
    if booking.preferred_coach_id:
        coach = Coach.query.get(booking.preferred_coach_id)
        if coach:
            coach_name = coach.display_name

    # ── Format duration ──
    duration_map = {30: "30 Minuten", 60: "1 Stunde", 90: "1,5 Stunden",
                    120: "2 Stunden", 180: "3 Stunden", 240: "4 Stunden",
                    300: "5 Stunden"}
    duration_str = duration_map.get(booking.duration_minutes,
                                    f"{booking.duration_minutes} Minuten")

    # ── Extract first name ──
    first_name = user.name.split()[0] if user.name else 'Hallo'

    # ── Build dashboard URL ──
    base_url = get_public_base_url()
    dashboard_url = f"{base_url}/dashboard"

    subject = AppSetting.get('tpl_confirm_subject',
                             'Dein Squalo Schwimmtraining wurde bestaetigt')

    body = _render_template_from_settings('tpl_confirm_body',
        name=user.name,
        first_name=first_name,
        datum=eff_date.strftime('%d.%m.%Y') if eff_date else 'TBD',
        uhrzeit=eff_time.strftime('%H:%M') if eff_time else 'TBD',
        ort=eff_location or 'TBD',
        coach=coach_name,
        dauer=duration_str,
        training_goal=booking.training_goal or '',
        customer_note=booking.user_note or '',
        dashboard_url=dashboard_url,
    ) or _build_confirm_email(
        first_name=first_name,
        date_str=eff_date.strftime('%d.%m.%Y') if eff_date else 'TBD',
        time_str=eff_time.strftime('%H:%M') if eff_time else 'TBD',
        location=eff_location or 'TBD',
        duration=duration_str,
        coach=coach_name,
        training_goal=booking.training_goal,
        customer_note=booking.user_note,
        dashboard_url=dashboard_url,
    )

    success = send_email(subject, user.email, body)

    # ── Track send time to prevent duplicates ──
    if success:
        booking.confirmation_email_sent_at = datetime.utcnow()
        db.session.commit()
        print(f"[MAIL] Bestaetigungsmail gesendet an {user.email} fuer Booking #{booking.id}")
    else:
        print(f"[MAIL-FEHLER] Bestaetigungsmail fehlgeschlagen fuer Booking #{booking.id}")

    return success


def send_customer_rejection_email(booking, admin_note=None):
    """Send customer email when a booking is rejected."""
    user = User.query.get(booking.user_id)
    if not user or not user.email:
        return

    subject = AppSetting.get('tpl_reject_subject', 'Deine Squalo Terminanfrage')

    note_line = ""
    if admin_note:
        note_line = f"\nKommentar vom Coach:\n{admin_note}\n"

    body = _render_template_from_settings('tpl_reject_body',
        name=user.name,
        notiz=note_line,
    ) or _default_tpl_reject().replace('{{name}}', user.name).replace('{{notiz}}', note_line)

    send_email(subject, user.email, body)


# ── Shop order emails ─────────────────────────────────────────────
def _send_shop_customer_email(order, products):
    """Send confirmation email to customer after shop order."""
    first_name = order.customer_name.split()[0] if order.customer_name else 'Hallo'
    product_lines = []
    total = 0.0
    for p in products:
        price = p.get('price', 0)
        total += price
        line = f"- {p['name']} ({p['category']})"
        if price:
            line += f" – {price:.0f} €"
        product_lines.append(line)
    product_list = "\n".join(product_lines)

    total_line = f"\nGesamtpreis (ca.): {total:.0f} €\n" if total > 0 else ""

    body = (
        f"Hallo {first_name},\n"
        f"\n"
        f"deine Produktauswahl für das nächste Schwimmtraining wurde gespeichert.\n"
        f"\n"
        f"Ausgewählte Produkte:\n"
        f"{product_list}\n"
        f"{total_line}"
        f"Ich bringe dir die ausgewählten Produkte zur nächsten passenden Schwimmstunde mit. "
        f"Wir schauen dann gemeinsam, ob sie gut zu deinem Training und deinem Level passen.\n"
        f"\n"
        f"Falls du noch Fragen zum Equipment hast, kannst du einfach auf diese Mail antworten.\n"
        f"\n"
        f"Bis bald im Wasser!\n"
        f"\n"
        f"Moritz\n"
        f"Squalo Schwimmcoaching"
    )

    subject = "Deine Squalo Produktauswahl wurde gespeichert"
    send_email(subject, order.customer_email, body)


def _send_shop_admin_email(order, products):
    """Send notification to admin/coach about new shop order."""
    admin_email = get_admin_email()
    product_lines = []
    total = 0.0
    for p in products:
        price = p.get('price', 0)
        total += price
        line = f"  - {p['name']} ({p['category']})"
        if price:
            line += f" – {price:.0f} €"
        product_lines.append(line)
    product_list = "\n".join(product_lines)

    total_line = f"\nGesamtpreis (ca.): {total:.0f} €" if total > 0 else ""
    now_str = order.created_at.strftime('%d.%m.%Y %H:%M') if order.created_at else '–'

    body = (
        f"Neue Shop-Bestellung eingegangen.\n"
        f"\n"
        f"Kunde: {order.customer_name}\n"
        f"E-Mail: {order.customer_email}\n"
        f"Zeitpunkt: {now_str}\n"
        f"\n"
        f"Ausgewählte Produkte:\n"
        f"{product_list}\n"
        f"{total_line}"
        f"\nHinweis: Zum nächsten Training mitbringen.\n"
    )

    if order.note:
        body += f"\nNachricht des Kunden: {order.note}\n"

    subject = "Neue Squalo Shop-Auswahl"
    send_email(subject, admin_email, body)


# ── Default mail templates (fallback when AppSetting is empty) ───────
def _default_tpl_new():
    return """Hallo Moritz,

eine neue Terminanfrage ist eingegangen.

Kunde: {{name}}
E-Mail: {{email}}

Zeitoptionen:
{{zeitoptionen}}

Wunschorte: {{wunschorte}}
Coach-Wunsch: {{coach}}
Dauer: {{dauer}}
Trainingsziel: {{ziel}}
Notiz: {{notiz}}
Geschätzter Preis: {{preis}}

Link: /admin

Viele Grüße
Squalo Benachrichtigungssystem"""

def _default_tpl_confirm():
    return """Hallo {{first_name}},

super, ich freue mich auf unser gemeinsames Schwimmtraining.

Dein Termin ist bestätigt:

Datum:     {{datum}}
Uhrzeit:   {{uhrzeit}}
Ort:       {{ort}}
Dauer:     {{dauer}}
Coach:     {{coach}}

Bitte bring, falls vorhanden, eine gut sitzende Schwimmbrille mit.
Wenn du hast, sind kurze Schwimmflossen und ein Pullbuoy ebenfalls hilfreich.
Wenn du diese Sachen noch nicht hast, ist das aber kein Problem – wir können auch ohne Zusatzmaterial starten.

Du findest den Termin auch in deinem Squalo-Dashboard. Dort kannst du ihn direkt in deinen Kalender exportieren.

Bis bald im Wasser!

Moritz
Squalo Schwimmcoaching"""

def _default_tpl_reject():
    return """Hallo {{name}},

leider konnte deine gewünschte Terminanfrage nicht wie gewünscht umgesetzt werden.

Das bedeutet aber nicht, dass du kein Schwimmtraining bekommst!
Du kannst jederzeit einen neuen Termin anfragen unter /booking – wähle einfach andere Zeiten oder Orte.

{{notiz}}

Viele Grüße
Dein Squalo-Team"""

def _default_tpl_alternative():
    return """Hallo {{name}},

wir haben einen Alternativvorschlag für dein Squalo Schwimmtraining:

Datum:   {{datum}}
Uhrzeit: {{uhrzeit}}

Kommentar:
{{kommentar}}

Falls dieser Termin passt, antworte einfach auf diese E-Mail oder kontaktiere uns über dein Dashboard.

Viele Grüße
Dein Squalo-Team"""


def _render_template_from_settings(tpl_key, **kwargs):
    """Render a mail template from AppSetting, falling back to default."""
    import re
    tpl_text = AppSetting.get(tpl_key, "")
    if not tpl_text:
        return None
    # Replace {{placeholder}} with values
    for key, val in kwargs.items():
        tpl_text = tpl_text.replace("{{" + key + "}}", str(val))
    return tpl_text


def _build_confirm_email(first_name, date_str, time_str, location, duration,
                         coach, training_goal=None, customer_note=None,
                         dashboard_url=None):
    """Build the customer confirmation email body (default text).

    This is the primary confirmation email text. It is used when no custom
    template is stored in AppSettings (tpl_confirm_body).
    """
    if not dashboard_url:
        dashboard_url = '/dashboard'

    lines = [
        f"Hallo {first_name},",
        "",
        "super, ich freue mich auf unser gemeinsames Schwimmtraining.",
        "",
        "Dein Termin ist bestätigt:",
        "",
        f"Datum:     {date_str}",
        f"Uhrzeit:   {time_str}",
        f"Ort:       {location}",
        f"Dauer:     {duration}",
        f"Coach:     {coach}",
    ]

    # Optional: training goal
    if training_goal and training_goal.strip():
        lines.extend([
            "",
            "Ich habe gesehen, dass du besonders an folgendem Thema arbeiten möchtest:",
            training_goal.strip(),
        ])

    # Optional: customer note
    if customer_note and customer_note.strip():
        lines.extend([
            "",
            "Deine zusätzliche Notiz habe ich ebenfalls gesehen und berücksichtige sie im Training:",
            customer_note.strip(),
        ])

    lines.extend([
        "",
        "Für die erste Stunde brauchst du dich beim Equipment nicht zu stressen.",
        "Ich bringe immer Basisequipment mit, damit wir direkt starten können.",
        "",
        "Wenn du eigenes Material hast, bring es gerne mit.",
        "Am besten geeignet sind:",
        "- eine gut sitzende Schwimmbrille",
        "- kurze Schwimmflossen",
        "- ein Pullbuoy / eine Poolboje",
        "",
        "Wenn du noch nichts davon hast, ist das überhaupt kein Problem.",
        "Du kannst das Equipment auch direkt über unseren Squalo-Shop bestellen.",
        "Ich habe die empfohlenen Produkte vorrätig und kann sie dir",
        "dann direkt zur nächsten Stunde mitbringen.",
        "Alternativ kannst du dir das Material natürlich auch",
        "selbst bis zur nächsten Stunde organisieren.",
        "",
        "Du findest deinen Termin auch in deinem Squalo-Dashboard.",
        "Dort kannst du ihn direkt in deinen Kalender exportieren.",
        f"Dashboard: {dashboard_url}",
        "",
        "Bis bald im Wasser!",
        "",
        "Moritz",
        "Squalo Schwimmcoaching",
    ])

    return "\n".join(lines)


def get_public_base_url():
    """Return the public base URL for absolute links.

    Priority: PUBLIC_BASE_URL env var → request.host_url → fallback.
    Always returns without trailing slash.
    """
    configured = os.environ.get('PUBLIC_BASE_URL', '').rstrip('/')
    if configured:
        return configured
    try:
        from flask import request
        return request.host_url.rstrip('/')
    except RuntimeError:
        return 'http://127.0.0.1:5000'


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # ── ProxyFix: trust Render's reverse proxy for correct host_url ──
    # Only enable in production (behind Render proxy)
    if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER'):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    # Ensure instance directory exists for SQLite database
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    uploads_path = os.path.join(os.path.dirname(__file__), "static", "uploads")
    os.makedirs(uploads_path, exist_ok=True)

    db.init_app(app)

    # ── Make get_public_base_url available in all templates ──
    @app.context_processor
    def inject_public_base_url():
        return dict(get_public_base_url=get_public_base_url)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # ── Session tracking (privacy-respecting) ─────────────────────
    import uuid as _uuid
    from datetime import datetime as _dt, timedelta as _td

    @app.before_request
    def track_visitor():
        """Track anonymous/authenticated sessions for coach panel stats."""
        # Skip static files and API endpoints
        if request.path.startswith('/static/') or request.path.endswith('.ics'):
            return
        try:
            # Get or create session ID
            if '_sid' not in session:
                session['_sid'] = _uuid.uuid4().hex[:16]
            sid = session['_sid']

            now = _dt.utcnow()
            record = SiteSession.query.filter_by(session_id=sid).first()

            if record:
                record.last_seen = now
                record.last_path = request.path
                if current_user.is_authenticated:
                    record.user_id = current_user.id
                    record.is_authenticated = True
                    record.role = getattr(current_user, 'role', 'student')
                else:
                    record.user_id = None
                    record.is_authenticated = False
                    record.role = 'guest'
            else:
                user_id = current_user.id if current_user.is_authenticated else None
                role = 'guest'
                if current_user.is_authenticated:
                    role = getattr(current_user, 'role', 'student')
                record = SiteSession(
                    session_id=sid,
                    user_id=user_id,
                    is_authenticated=current_user.is_authenticated,
                    role=role,
                    last_path=request.path,
                    first_seen=now,
                    last_seen=now,
                )
                db.session.add(record)
            db.session.commit()
        except Exception:
            # Never crash the app because of tracking
            try:
                db.session.rollback()
            except Exception:
                pass

    # Initialize database and seed data if needed
    with app.app_context():
        # ── Log which database is in use (never log full URL/password) ──
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('postgresql'):
            print("[DB] Database: PostgreSQL via DATABASE_URL")
        elif db_uri.startswith('sqlite'):
            print("[DB] Database: local SQLite fallback")
        else:
            print("[DB] Database: custom URI")

        db.create_all()
        
        # ── Migration: Neue Spalten für Booking (duration, pricing) ──
        try:
            with db.engine.connect() as conn:
                # Check if column exists – if not, add it
                import sqlalchemy as sa
                inspector = sa.inspect(db.engine)
                columns = [c['name'] for c in inspector.get_columns('booking')]
                if 'duration_minutes' not in columns:
                    conn.execute(sa.text("ALTER TABLE booking ADD COLUMN duration_minutes INTEGER DEFAULT 60"))
                    conn.execute(sa.text("ALTER TABLE booking ADD COLUMN duration_slots INTEGER DEFAULT 2"))
                    conn.execute(sa.text("ALTER TABLE booking ADD COLUMN estimated_price FLOAT DEFAULT 50.0"))
                    conn.commit()
                    print("[MIGRATION] Spalten duration_minutes, duration_slots, estimated_price hinzugefügt")
        except Exception as e:
            print(f"[MIGRATION] Fehler beim Hinzufügen der Spalten (ignoriert): {e}")
        
        # ── Migration: Coach-Präferenz in Booking ───────────────────
        try:
            with db.engine.connect() as conn:
                import sqlalchemy as sa
                inspector = sa.inspect(db.engine)
                columns = [c['name'] for c in inspector.get_columns('booking')]
                if 'preferred_coach_id' not in columns:
                    conn.execute(sa.text("ALTER TABLE booking ADD COLUMN preferred_coach_id INTEGER REFERENCES coach(id)"))
                    conn.commit()
                    print("[MIGRATION] Spalte preferred_coach_id hinzugefügt")
        except Exception as e:
            print(f"[MIGRATION] Fehler (ignoriert): {e}")

        # ── Migration: Neue Coach-Spalten (email, cities, etc.) ─────
        try:
            with db.engine.connect() as conn:
                import sqlalchemy as sa
                inspector = sa.inspect(db.engine)
                columns = [c['name'] for c in inspector.get_columns('coach')]
                new_cols = {
                    'first_name': "ALTER TABLE coach ADD COLUMN first_name VARCHAR(80)",
                    'last_name': "ALTER TABLE coach ADD COLUMN last_name VARCHAR(80)",
                    'email': "ALTER TABLE coach ADD COLUMN email VARCHAR(128)",
                    'cities_served': "ALTER TABLE coach ADD COLUMN cities_served TEXT",
                    'specialization': "ALTER TABLE coach ADD COLUMN specialization VARCHAR(200)",
                }
                added = 0
                for col_name, ddl in new_cols.items():
                    if col_name not in columns:
                        conn.execute(sa.text(ddl))
                        added += 1
                if added:
                    conn.commit()
                    print(f"[MIGRATION] Coach-Spalten hinzugefügt: {added}")
        except Exception as e:
            print(f"[MIGRATION] Coach-Spalten (ignoriert): {e}")

        # ── Migration: confirmation_email_sent_at on booking ─────
        try:
            with db.engine.connect() as conn:
                import sqlalchemy as sa
                inspector = sa.inspect(db.engine)
                columns = [c['name'] for c in inspector.get_columns('booking')]
                if 'confirmation_email_sent_at' not in columns:
                    conn.execute(sa.text(
                        "ALTER TABLE booking ADD COLUMN confirmation_email_sent_at TIMESTAMP"
                    ))
                    conn.commit()
                    print("[MIGRATION] Spalte confirmation_email_sent_at hinzugefuegt")
        except Exception as e:
            print(f"[MIGRATION] confirmation_email_sent_at (ignoriert): {e}")

        # ── Migration: Location city column ─────────────────────────
        try:
            import sqlalchemy as sa
            with db.engine.connect() as conn:
                inspector = sa.inspect(db.engine)
                columns = [c['name'] for c in inspector.get_columns('location')]
                if 'city' not in columns:
                    conn.execute(sa.text("ALTER TABLE location ADD COLUMN city VARCHAR(128) DEFAULT 'Berlin'"))
                    conn.commit()
                    print("[MIGRATION] Spalte city zu Location hinzugefuegt")
                    # Set city='Berlin' for all existing locations without city
                    conn.execute(sa.text("UPDATE location SET city = 'Berlin' WHERE city IS NULL"))
                    conn.commit()
                    print("[MIGRATION] Alle vorhandenen Locations auf city='Berlin' gesetzt")
                else:
                    print("[MIGRATION] Location city existiert bereits")
        except Exception as e:
            print(f"[MIGRATION] Location city (ignoriert): {e}")

        # ── Migration: Fix default notification email ─────────────
        try:
            current_email_val = AppSetting.get("booking_notification_email")
            if current_email_val and current_email_val != DEFAULT_ADMIN_EMAIL:
                AppSetting.set("booking_notification_email", DEFAULT_ADMIN_EMAIL)
                print(f"[MIGRATION] Benachrichtigungs-Email korrigiert: {current_email_val} -> {DEFAULT_ADMIN_EMAIL}")
        except Exception:
            pass
        
        # ── Admin-User ──────────────────────────────────────────────
        # Admin-E-Mail (fest, kann später über ENV geändert werden)
        admin_email = os.environ.get("ADMIN_EMAIL", "zentner.moritz@gmail.com")
        # Admin-Passwort: via ENV (Render) oder lokaler Dev-Fallback
        admin_password = os.environ.get("ADMIN_INITIAL_PASSWORD", "admin123")
        
        admin_user = User.query.filter_by(email=admin_email).first()
        if admin_user:
            # Existiert → Rolle und Passwort aktualisieren
            admin_user.role = "admin"
            admin_user.password_hash = generate_password_hash(admin_password)
            print(f"[OK] Admin aktualisiert: {admin_email} (Rolle: admin)")
        else:
            # Neu anlegen
            admin_user = User(
                name="Admin",
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                role="admin"
            )
            db.session.add(admin_user)
            print(f"[OK] Admin neu angelegt: {admin_email}")
            
        # ── Demo-User ───────────────────────────────────────────────
        if not User.query.filter_by(email="user@squalo.local").first():
            user = User(
                name="Max Mustermann", 
                email="user@squalo.local", 
                password_hash=generate_password_hash("password"), 
                role="user"
            )
            db.session.add(user)
            
        # ── Standorte seeden (idempotent: vorhandene werden aktualisiert) ──
        try:
            from seed_data import SWIM_LOCATIONS as SEED_LOCATIONS
        except ImportError:
            SEED_LOCATIONS = []
            print("[WARN] seed_data.py nicht gefunden – keine Locations geseedet")
        
        seed_count_new = 0
        seed_count_upd = 0
        for data in SEED_LOCATIONS:
            existing = Location.query.filter_by(name=data["name"]).first()
            if existing:
                # Update existing location
                changed = False
                for field in ["location_type", "district", "address", "latitude", "longitude",
                              "official_status", "verified_status", "water_temperature", "crowd_level",
                              "maps_url", "city"]:
                    val = data.get(field)
                    if val is not None and getattr(existing, field) != val:
                        setattr(existing, field, val)
                        changed = True
                if changed:
                    seed_count_upd += 1
            else:
                loc = Location(
                    name=data["name"],
                    location_type=data["location_type"],
                    district=data["district"],
                    city=data.get("city", "Berlin"),
                    address=data.get("address", ""),
                    latitude=data.get("latitude"),
                    longitude=data.get("longitude"),
                    official_status=data["official_status"],
                    verified_status=data["verified_status"],
                    water_temperature=data["water_temperature"],
                    crowd_level=data["crowd_level"],
                    maps_url=data["maps_url"]
                )
                db.session.add(loc)
                seed_count_new += 1
        
        if seed_count_new or seed_count_upd:
            print(f"[OK] Standorte: {seed_count_new} neu, {seed_count_upd} aktualisiert")
        else:
            print(f"[OK] Alle {len(SEED_LOCATIONS)} Standorte bereits aktuell")
        
        # ── Coach seeden: Moritz Zentner ────────────────────────────
        coach_slug = "moritz-zentner"
        existing_coach = Coach.query.filter_by(slug=coach_slug).first()
        if existing_coach:
            # Update existing
            existing_coach.name = "Moritz Zentner"
            existing_coach.title = "Schwimmlehrer – 24 Jahre Erfahrung, Rettungsschwimmer"
            existing_coach.bio = (
                "Ich bin Moritz, 28 Jahre alt und studiere Humanoide Robotik. "
                "Schwimmen ist meine große Leidenschaft – ich schwimme jeden Tag und "
                "gebe die Technik, die ich in über 22 Jahren gesammelt habe, mit Freude "
                "an dich weiter. Ich war Mitglied in 3 verschiedenen Schwimmvereinen und "
                "konnte so viele Coaching-Stile aufnehmen, um genau den anzuwenden, der "
                "zu dir passt. Egal ob Anfänger, Wiedereinsteiger oder Fortgeschrittener – "
                "mit Geduld und einem geschulten Auge verbessern wir gemeinsam deine Technik."
            )
            existing_coach.strengths = (
                "• 🏊 24 Jahre Schwimmerfahrung – aktiver Tages-Schwimmer\n"
                "• 🏆 2 Jahre Einzelcoaching – individuell auf dich abgestimmt\n"
                "• 🏆 3 Schwimmvereine – breit gefächertes Coaching-Know-how\n"
                "• 🧘 Ruhige, geduldige Anleitung – individuelles Tempo\n"
                "• 🎯 Gezielte Technikverbesserung – Wasserlage, Atmung, Bewegungsökonomie\n"
                "• 📍 Flexible Trainingsorte – jedes Bad & jeder See in Berlin\n"
                "• 📋 Individuelle Trainingspläne – auch für außerhalb der Stunden"
            )
            existing_coach.swim_style = (
                "Ich bin geduldig und aufmerksam und schaue mir deine Technik genau an, "
                "um gezielt die Lagen zu verbessern, an denen du arbeiten möchtest. "
                "Egal, ob du gerade erst anfängst zu schwimmen oder nur noch den letzten "
                "Feinschliff brauchst – wir definieren ein Ziel und arbeiten Bahn für Bahn "
                "darauf hin. Falls dir neben der Technik auch deine Fitness wichtig ist, "
                "erstelle ich dir einen individuellen Trainingsplan, der dich auch außerhalb "
                "unserer Stunden fit hält."
            )
            existing_coach.experience = (
                "🏅 24 Jahre Schwimmerfahrung\n"
                "🏅 2 Jahre Einzelcoaching-Erfahrung\n"
                "🏅 Mitglied in 3 Schwimmvereinen\n"
                "🏅 Rettungsschwimmer\n"
                "🏅 49+ Schüler erfolgreich trainiert\n"
                "🏅 5,0 ⭐ Bewertungen (8 Bewertungen)"
            )
            existing_coach.external_profile_url = "https://www.superprof.de/jahre-schwimmerfahrung-rettungschwimmer-und-viel-geduld-mit-mir-lernst-deinem-individuellen-tempo-deine-technik.html"
            existing_coach.cities_served = "Berlin"
            existing_coach.image_url = "/static/images/moritz-zentner.jpg"
            existing_coach.is_active = True
            print(f"[OK] Coach aktualisiert: {existing_coach.name}")
        else:
            coach = Coach(
                name="Moritz Zentner",
                slug=coach_slug,
                title="Schwimmlehrer – 24 Jahre Erfahrung, Rettungsschwimmer",
                image_url="/static/images/moritz-zentner.jpg",
                bio=(
                    "Ich bin Moritz, 28 Jahre alt und studiere Humanoide Robotik. "
                    "Schwimmen ist meine große Leidenschaft – ich schwimme jeden Tag und "
                    "gebe die Technik, die ich in über 22 Jahren gesammelt habe, mit Freude "
                    "an dich weiter. Ich war Mitglied in 3 verschiedenen Schwimmvereinen und "
                    "konnte so viele Coaching-Stile aufnehmen, um genau den anzuwenden, der "
                    "zu dir passt. Egal ob Anfänger, Wiedereinsteiger oder Fortgeschrittener – "
                    "mit Geduld und einem geschulten Auge verbessern wir gemeinsam deine Technik."
                ),
                strengths=(
                    "• 🏊 24 Jahre Schwimmerfahrung – aktiver Tages-Schwimmer\n"
                    "• 🏆 2 Jahre Einzelcoaching – individuell auf dich abgestimmt\n"
                    "• 🏆 3 Schwimmvereine – breit gefächertes Coaching-Know-how\n"
                    "• 🧘 Ruhige, geduldige Anleitung – individuelles Tempo\n"
                    "• 🎯 Gezielte Technikverbesserung – Wasserlage, Atmung, Bewegungsökonomie\n"
                    "• 📍 Flexible Trainingsorte – jedes Bad & jeder See in Berlin\n"
                    "• 📋 Individuelle Trainingspläne – auch für außerhalb der Stunden"
                ),
                swim_style=(
                    "Ich bin geduldig und aufmerksam und schaue mir deine Technik genau an, "
                    "um gezielt die Lagen zu verbessern, an denen du arbeiten möchtest. "
                    "Egal, ob du gerade erst anfängst zu schwimmen oder nur noch den letzten "
                    "Feinschliff brauchst – wir definieren ein Ziel und arbeiten Bahn für Bahn "
                    "darauf hin. Falls dir neben der Technik auch deine Fitness wichtig ist, "
                    "erstelle ich dir einen individuellen Trainingsplan, der dich auch außerhalb "
                    "unserer Stunden fit hält."
                ),
                experience=(
                    "🏅 24 Jahre Schwimmerfahrung\n"
                    "🏅 2 Jahre Einzelcoaching-Erfahrung\n"
                    "🏅 Mitglied in 3 Schwimmvereinen\n"
                    "🏅 Rettungsschwimmer\n"
                    "🏅 49+ Schüler erfolgreich trainiert\n"
                    "🏅 5,0 ⭐ Bewertungen (8 Bewertungen)"
                ),
                external_profile_url="https://www.superprof.de/jahre-schwimmerfahrung-rettungschwimmer-und-viel-geduld-mit-mir-lernst-deinem-individuellen-tempo-deine-technik.html",
                is_active=True,
            )
            db.session.add(coach)
            print(f"[OK] Coach neu angelegt: {coach.name}")
        
        # ── Coach seeden: Clara Zentner (Freiburg) ──────────────
        coach_slug_fb = "clara-zentner"
        existing_coach_fb = Coach.query.filter_by(slug=coach_slug_fb).first()
        # Also check for old slug to migrate
        if not existing_coach_fb:
            old_fb = Coach.query.filter_by(slug="anna-platzhalter").first()
            if old_fb:
                old_fb.slug = coach_slug_fb
                existing_coach_fb = old_fb
                print("[OK] Anna Platzhalter Slug zu clara-zentner migriert")
        if existing_coach_fb:
            existing_coach_fb.name = "Clara Zentner"
            existing_coach_fb.slug = coach_slug_fb
            existing_coach_fb.first_name = "Clara"
            existing_coach_fb.last_name = "Zentner"
            existing_coach_fb.title = "Schwimmtrainerin in Freiburg \u2013 Trainerlizenz B, Rettungsschwimmerin, Medizin & Biomechanik"
            existing_coach_fb.bio = (
                "Clara Zentner ist Schwimmtrainerin in Freiburg und Umgebung. "
                "Sie verbindet langj\u00e4hrige Schwimmerfahrung mit Trainerlizenz B, "
                "Rettungsschwimmer-Qualifikation sowie einem Hintergrund in "
                "Biomechanik und Medizin. Sie unterst\u00fctzt Anf\u00e4nger, "
                "Wiedereinsteiger, Kinder, Erwachsene und fortgeschrittene Schwimmer "
                "dabei, ihre Wasserlage, Atmung, Technik und Sicherheit im Wasser "
                "gezielt zu verbessern."
            )
            existing_coach_fb.strengths = (
                "\u2022 Rund 20 Jahre Schwimmerfahrung\n"
                "\u2022 5 Jahre Coaching-Erfahrung im Einzel- und Gruppentraining\n"
                "\u2022 Trainerlizenz B Schwimmen\n"
                "\u2022 Rettungsschwimmerin\n"
                "\u2022 Hintergrund in Biomechanik und Medizin\n"
                "\u2022 Ruhige, geduldige Anleitung in individuellem Tempo\n"
                "\u2022 Gezielte Technikverbesserung: Wasserlage, Atmung, Bewegungs\u00f6konomie\n"
                "\u2022 Flexible Trainingsorte in Freiburg und Umgebung\n"
                "\u2022 Individuelle Trainingspl\u00e4ne auch au\u00dferhalb der Stunden\n"
                "\u2022 \u00dcber 100 erfolgreich trainierte Sch\u00fcler"
            )
            existing_coach_fb.swim_style = (
                "Mein Coaching verbindet ruhige Anleitung mit einem genauen Blick f\u00fcr "
                "Bewegungsabl\u00e4ufe. Durch meinen biomechanischen und medizinischen "
                "Hintergrund analysiere ich deine Technik pr\u00e4zise und erkl\u00e4re dir "
                "verst\u00e4ndlich, woran wir arbeiten. Dabei geht es nicht darum, m\u00f6glichst "
                "schnell m\u00f6glichst viel zu schwimmen, sondern deine Technik so zu "
                "verbessern, dass du effizienter, entspannter und sicherer durchs Wasser "
                "kommst.\n\n"
                "Wir passen das Training an dein Level und dein Ziel an: Kraulen lernen, "
                "Wasserlage verbessern, Atmung koordinieren, Technikfehler reduzieren, "
                "sicherer werden oder deine Schwimmleistung f\u00fcr Fitness und Triathlon "
                "verbessern. Wenn du zus\u00e4tzlich au\u00dferhalb unserer Stunden trainieren "
                "m\u00f6chtest, kann ich dir passende \u00dcbungen und Trainingspl\u00e4ne mitgeben."
            )
            existing_coach_fb.experience = (
                "\U0001F3C5 Rund 20 Jahre Schwimmerfahrung\n"
                "\U0001F3C5 5 Jahre Erfahrung als Schwimmtrainerin\n"
                "\U0001F3C5 Einzel- und Gruppentraining\n"
                "\U0001F3C5 Trainerlizenz B Schwimmen\n"
                "\U0001F3C5 Rettungsschwimmerin\n"
                "\U0001F3C5 Studium der Biomechanik\n"
                "\U0001F3C5 Medizinstudium\n"
                "\U0001F3C5 \u00dcber 100 erfolgreich trainierte Sch\u00fcler\n"
                "\U0001F4CD Verf\u00fcgbar in Freiburg und Umgebung"
            )
            existing_coach_fb.specialization = (
                "Schwimmtechnik, Kraultechnik, Wasserlage, Atmung, Kinder- und "
                "Erwachsenentraining, Techniktraining, medizinisch/biomechanisch "
                "fundierte Bewegungsanalyse"
            )
            existing_coach_fb.cities_served = "Freiburg,Merzhausen,Gundelfingen,Denzlingen,Emmendingen,Teningen,Bad Krozingen"
            existing_coach_fb.image_url = "/static/images/squalo-logo.png"
            existing_coach_fb.is_active = True
            print(f"[OK] Coach aktualisiert: {existing_coach_fb.name}")
        else:
            coach_fb = Coach(
                name="Clara Zentner",
                slug=coach_slug_fb,
                first_name="Clara",
                last_name="Zentner",
                title="Schwimmtrainerin in Freiburg \u2013 Trainerlizenz B, Rettungsschwimmerin, Medizin & Biomechanik",
                bio=(
                    "Clara Zentner ist Schwimmtrainerin in Freiburg und Umgebung. "
                    "Sie verbindet langj\u00e4hrige Schwimmerfahrung mit Trainerlizenz B, "
                    "Rettungsschwimmer-Qualifikation sowie einem Hintergrund in "
                    "Biomechanik und Medizin. Sie unterst\u00fctzt Anf\u00e4nger, "
                    "Wiedereinsteiger, Kinder, Erwachsene und fortgeschrittene Schwimmer "
                    "dabei, ihre Wasserlage, Atmung, Technik und Sicherheit im Wasser "
                    "gezielt zu verbessern."
                ),
                strengths=(
                    "\u2022 Rund 20 Jahre Schwimmerfahrung\n"
                    "\u2022 5 Jahre Coaching-Erfahrung im Einzel- und Gruppentraining\n"
                    "\u2022 Trainerlizenz B Schwimmen\n"
                    "\u2022 Rettungsschwimmerin\n"
                    "\u2022 Hintergrund in Biomechanik und Medizin\n"
                    "\u2022 Ruhige, geduldige Anleitung in individuellem Tempo\n"
                    "\u2022 Gezielte Technikverbesserung: Wasserlage, Atmung, Bewegungs\u00f6konomie\n"
                    "\u2022 Flexible Trainingsorte in Freiburg und Umgebung\n"
                    "\u2022 Individuelle Trainingspl\u00e4ne auch au\u00dferhalb der Stunden\n"
                    "\u2022 \u00dcber 100 erfolgreich trainierte Sch\u00fcler"
                ),
                swim_style=(
                    "Mein Coaching verbindet ruhige Anleitung mit einem genauen Blick f\u00fcr "
                    "Bewegungsabl\u00e4ufe. Durch meinen biomechanischen und medizinischen "
                    "Hintergrund analysiere ich deine Technik pr\u00e4zise und erkl\u00e4re dir "
                    "verst\u00e4ndlich, woran wir arbeiten. Dabei geht es nicht darum, m\u00f6glichst "
                    "schnell m\u00f6glichst viel zu schwimmen, sondern deine Technik so zu "
                    "verbessern, dass du effizienter, entspannter und sicherer durchs Wasser "
                    "kommst.\n\n"
                    "Wir passen das Training an dein Level und dein Ziel an: Kraulen lernen, "
                    "Wasserlage verbessern, Atmung koordinieren, Technikfehler reduzieren, "
                    "sicherer werden oder deine Schwimmleistung f\u00fcr Fitness und Triathlon "
                    "verbessern. Wenn du zus\u00e4tzlich au\u00dferhalb unserer Stunden trainieren "
                    "m\u00f6chtest, kann ich dir passende \u00dcbungen und Trainingspl\u00e4ne mitgeben."
                ),
                experience=(
                    "\U0001F3C5 Rund 20 Jahre Schwimmerfahrung\n"
                    "\U0001F3C5 5 Jahre Erfahrung als Schwimmtrainerin\n"
                    "\U0001F3C5 Einzel- und Gruppentraining\n"
                    "\U0001F3C5 Trainerlizenz B Schwimmen\n"
                    "\U0001F3C5 Rettungsschwimmerin\n"
                    "\U0001F3C5 Studium der Biomechanik\n"
                    "\U0001F3C5 Medizinstudium\n"
                    "\U0001F3C5 \u00dcber 100 erfolgreich trainierte Sch\u00fcler\n"
                    "\U0001F4CD Verf\u00fcgbar in Freiburg und Umgebung"
                ),
                specialization=(
                    "Schwimmtechnik, Kraultechnik, Wasserlage, Atmung, Kinder- und "
                    "Erwachsenentraining, Techniktraining, medizinisch/biomechanisch "
                    "fundierte Bewegungsanalyse"
                ),
                cities_served="Freiburg,Merzhausen,Gundelfingen,Denzlingen,Emmendingen,Teningen,Bad Krozingen",
                image_url="/static/images/squalo-logo.png",
                is_active=True,
            )
            db.session.add(coach_fb)
            print(f"[OK] Coach neu angelegt: {coach_fb.name}")
        
        db.session.commit()

        # ── Bewertungen seeden (idempotent) ────────────────────────
        coach_moritz = Coach.query.filter_by(slug=coach_slug).first()
        if coach_moritz:
            existing_review_texts = {r.text for r in coach_moritz.reviews if r.source == 'superprof'}
            reviews_data = [
                {
                    "author_name": "David",
                    "rating": 5,
                    "text": "Perfekt! Ich habe es in kürzester Zeit von einem kompletten Anfänger zu einem fortgeschrittenen Schwimmer geschafft. Natürlich ist selbstständig Training ebenfalls wichtig, aber ohne Moritz hätte ich es nicht geschafft. Er ist sehr geduldig und ruhig beim Erklären und variiert die Unterrichtsstunden stark, je nachdem welcher Fokus noch nötig ist.",
                },
                {
                    "author_name": "Maarten",
                    "rating": 5,
                    "text": "Perfekt! Moritz ist ein ausgesprochen angenehmer und ruhiger Schwimmlehrer. Er nimmt sich viel Zeit und zeigt große Geduld, besonders wenn man bestimmte Dinge nicht sofort umsetzen kann. Dabei gibt er wertvolle Tipps und konkrete Vorschläge – und betrachtet deine Schwimmtechnik mit einem geschulten Auge. Ich habe mich nie gehetzt gefühlt, sondern im Gegenteil: jede Übung hat Sinn gemacht und wurde mit Geduld vermittelt. Absolut empfehlenswert!",
                },
                {
                    "author_name": "Arman",
                    "rating": 5,
                    "text": "Perfekt! Moritz ist ein sehr guter Schwimmlehrer. Er erklärt alles gut und verständlich, ist sehr geduldig und nett. Er weist genau auf Fehler hin und gibt direkt Lösungsansätze, wie man es besser machen kann. Das Training mit ihm war sehr angenehm und hat viel Spaß gemacht.",
                },
                {
                    "author_name": "Tim",
                    "rating": 5,
                    "text": "Perfekt! Hat mir sehr gut gefallen! Sehr sympathisch und kompetent!",
                },
                {
                    "author_name": "Anne",
                    "rating": 5,
                    "text": "Ich bin wirklich begeistert von meinem Moritz! Er ist äußerst kompetent und versteht es hervorragend, an meinen Ressourcen anzusetzen. Seine Anleitung ist super klar und motivierend, was mir immer richtig Spaß macht und mich voranbringt. Besonders schätze ich sein Verständnis und die Bereitschaft, auf meine Wünsche einzugehen. Außerdem ist er zeitlich sehr flexibel, was die Terminplanung erleichtert. Ich freue mich schon sehr auf die nächste Unterrichtsstunde und kann ihn nur wärmstens weiterempfehlen!",
                },
                {
                    "author_name": "Zakariae",
                    "rating": 5,
                    "text": "Moritz ist einfach großartig! Mit viel Geduld, Fachwissen und einer freundlichen Art hat er das Schwimmenlernen zu einer tollen Erfahrung gemacht. Er erklärt die Techniken verständlich, gibt hilfreiche Tipps und schafft eine angenehme Atmosphäre im Wasser. Dank ihm fühle ich mich jetzt viel sicherer im Wasser. Absolut empfehlenswert!",
                },
            ]
            for rd in reviews_data:
                if rd["text"] not in existing_review_texts:
                    review = CoachReview(
                        coach_id=coach_moritz.id,
                        user_id=None,
                        rating=rd["rating"],
                        text=rd["text"],
                        source="superprof",
                        author_name=rd["author_name"],
                        is_approved=True,
                    )
                    db.session.add(review)
            db.session.commit()
            print(f"[OK] Bewertungen gesynct für {coach_moritz.name}")
        
        db.session.commit()

    @app.route("/")
    def index():
        locations = Location.query.order_by(Location.name.asc()).all()
        now = datetime.now(ZoneInfo('Europe/Berlin'))
        print(f"[DEBUG] Index: {len(locations)} locations (Berlin time: {now.strftime('%H:%M')})")
        
        # Compute adaptive status for each location
        locations_with_status = []
        for loc in locations:
            status = compute_location_status(loc, now)
            # Attach computed fields as dynamic attributes (not persisted)
            loc._opening_status = status['opening_status']
            loc._opening_status_short = status['opening_status_short']
            loc._opening_class = status['opening_class']
            loc._water_temperature_label = status['water_temperature_label']
            loc._crowd_level_label = status['crowd_level_label']
            loc._crowd_class = status['crowd_class']
            loc._verified_label = status['verified_label']
            locations_with_status.append(loc)
        
        # Für Leaflet: nur Locations mit Koordinaten als JSON + computed status
        locations_for_map = []
        for loc in locations_with_status:
            if loc.latitude is not None and loc.longitude is not None:
                locations_for_map.append({
                    "id": loc.id,
                    "name": loc.name,
                    "location_type": loc.location_type,
                    "district": loc.district,
                    "city": loc.city or "Berlin",
                    "address": loc.address,
                    "latitude": float(loc.latitude),
                    "longitude": float(loc.longitude),
                    "maps_url": loc.maps_url,
                    "booking_url": url_for("booking") + "?location_id=" + str(loc.id),
                    # Computed status
                    "_opening_status": loc._opening_status,
                    "_opening_status_short": loc._opening_status_short,
                    "_opening_class": loc._opening_class,
                    "_water_temperature_label": loc._water_temperature_label,
                    "_crowd_level_label": loc._crowd_level_label,
                    "_crowd_class": loc._crowd_class,
                    "_verified_label": loc._verified_label,
                })
        print(f"[DEBUG] Index: {len(locations_for_map)} locations an Leaflet übergeben")
        
        # ── Community Feed Posts ──
        feed_posts = FeedPost.query.order_by(FeedPost.created_at.desc()).limit(20).all()
        
        return render_template("index.html", locations=locations_with_status,
                               locations_for_map=locations_for_map,
                               feed_posts=feed_posts)

    @app.route("/feed/post", methods=["POST"])
    @login_required
    def feed_post():
        text = request.form.get("text", "").strip()
        if not text:
            flash("Bitte gib einen Text ein.", "danger")
            return redirect(url_for("index"))
        
        post = FeedPost(user_id=current_user.id, text=text)
        db.session.add(post)
        db.session.commit()
        
        flash("Dein Update wurde veröffentlicht!", "success")
        return redirect(url_for("index"))

    @app.route("/coaches")
    def coaches():
        coach_list = Coach.query.filter_by(is_active=True).order_by(Coach.name.asc()).all()
        return render_template("coaches.html", coaches=coach_list)

    @app.route("/coaches/review/<int:coach_id>", methods=["POST"])
    @login_required
    def coaches_review(coach_id):
        coach = Coach.query.get_or_404(coach_id)
        rating = request.form.get("rating", type=int)
        text = request.form.get("text", "").strip()
        if not rating or rating < 1 or rating > 5:
            flash("Bitte wähle eine Bewertung von 1–5 Sternen.", "danger")
            return redirect(url_for("coaches"))
        review = CoachReview(
            coach_id=coach.id,
            user_id=current_user.id,
            rating=rating,
            text=text,
            source="squalo",
            author_name=current_user.name,
            is_approved=True,
        )
        db.session.add(review)
        db.session.commit()
        flash("Danke für deine Bewertung!", "success")
        return redirect(url_for("coaches"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            if not name or not email or not password:
                flash("Please fill all fields", "danger")
                return redirect(url_for("register"))
            if User.query.filter_by(email=email).first():
                flash("Email already registered", "danger")
                return redirect(url_for("register"))
            u = User(name=name, email=email, password_hash=generate_password_hash(password))
            db.session.add(u)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash("Logged in", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out", "success")
        return redirect(url_for("index"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        all_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
        bookings_pending = [b for b in all_bookings if b.status == 'angefragt']
        bookings_confirmed = [b for b in all_bookings if is_confirmed_status(b.status)]
        bookings_rejected = [b for b in all_bookings if b.status == 'abgelehnt']
        notes = TrainingNote.query.filter_by(user_id=current_user.id).order_by(TrainingNote.created_at.desc()).all()
        return render_template("dashboard.html",
                               bookings=all_bookings,
                               bookings_pending=bookings_pending,
                               bookings_confirmed=bookings_confirmed,
                               bookings_rejected=bookings_rejected,
                               notes=notes)

    @app.route("/calendar/<int:booking_id>.ics")
    @login_required
    def calendar_event(booking_id):
        b = Booking.query.get_or_404(booking_id)
        if b.user_id != current_user.id or not is_confirmed_status(b.status):
            flash("Kalender-Export nur für bestätigte eigene Termine möglich.", "warning")
            return redirect(url_for("dashboard"))
        if not b.confirmed_date:
            flash("Kalender-Export: Kein bestätigtes Datum vorhanden.", "warning")
            return redirect(url_for("dashboard"))

        tz = ZoneInfo("Europe/Berlin")
        start_dt = datetime.combine(b.confirmed_date, b.confirmed_time or datetime.min.time()).replace(tzinfo=tz)
        end_dt = start_dt + timedelta(minutes=b.duration_minutes or 60)
        loc_name = b.confirmed_location.name if b.confirmed_location else "TBD"
        coach_name = b.preferred_coach.name if b.preferred_coach else "Moritz"
        user = User.query.get(b.user_id)
        user_name = user.name if user else ""

        uid = f"squalo-booking-{b.id}@squalo.app"
        dt_start = start_dt.strftime("%Y%m%dT%H%M%S")
        dt_end = end_dt.strftime("%Y%m%dT%H%M%S")
        dtstamp = datetime.now(tz).strftime("%Y%m%dT%H%M%S")
        summary = "Squalo Schwimmtraining"
        description = (
            f"Dein bestätigtes Squalo Schwimmtraining mit {coach_name}.\\n"
            f"Ort: {loc_name}\\n"
            f"Dauer: {b.duration_minutes} Minuten\\n"
            f"Schüler: {user_name}"
        )

        ics_content = (
            "BEGIN:VCALENDAR\r\n"
            "VERSION:2.0\r\n"
            "PRODID:-//Squalo Schwimmcoaching//DE\r\n"
            "CALSCALE:GREGORIAN\r\n"
            "METHOD:PUBLISH\r\n"
            "X-WR-TIMEZONE:Europe/Berlin\r\n"
            "BEGIN:VTIMEZONE\r\n"
            "TZID:Europe/Berlin\r\n"
            "BEGIN:DAYLIGHT\r\n"
            "TZOFFSETFROM:+0100\r\n"
            "TZOFFSETTO:+0200\r\n"
            "TZNAME:CEST\r\n"
            "DTSTART:19700329T020000\r\n"
            "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3\r\n"
            "END:DAYLIGHT\r\n"
            "BEGIN:STANDARD\r\n"
            "TZOFFSETFROM:+0200\r\n"
            "TZOFFSETTO:+0100\r\n"
            "TZNAME:CET\r\n"
            "DTSTART:19701025T030000\r\n"
            "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10\r\n"
            "END:STANDARD\r\n"
            "END:VTIMEZONE\r\n"
            "BEGIN:VEVENT\r\n"
            f"UID:{uid}\r\n"
            f"DTSTAMP:{dtstamp}\r\n"
            f"DTSTART;TZID=Europe/Berlin:{dt_start}\r\n"
            f"DTEND;TZID=Europe/Berlin:{dt_end}\r\n"
            f"SUMMARY:{summary}\r\n"
            f"LOCATION:{loc_name}\r\n"
            f"DESCRIPTION:{description}\r\n"
            "STATUS:CONFIRMED\r\n"
            "END:VEVENT\r\n"
            "END:VCALENDAR\r\n"
        )
        return Response(
            ics_content,
            mimetype="text/calendar",
            headers={"Content-Disposition": f"attachment; filename=squalo-training-{b.id}.ics"}
        )

    @app.route("/feed", methods=["GET", "POST"])
    @login_required
    def feed():
        if request.method == "POST":
            text = request.form.get("text")
            image = request.files.get("image")
            image_path = None
            if image and allowed_file(image.filename):
                filename = secure_filename(f"{int(datetime.utcnow().timestamp())}_{image.filename}")
                filepath = os.path.join(uploads_path, filename)
                image.save(filepath)
                image_path = f"uploads/{filename}"
            post = FeedPost(user_id=current_user.id, text=text, image_path=image_path)
            db.session.add(post)
            db.session.commit()
            flash("Posted to feed", "success")
            return redirect(url_for("feed"))
        posts = FeedPost.query.order_by(FeedPost.is_pinned.desc(), FeedPost.created_at.desc()).all()
        return render_template("feed.html", posts=posts)

    @app.route("/booking", methods=["GET", "POST"])
    @login_required
    def booking():
        locations = Location.query.order_by(Location.name.asc()).all()
        if request.method == "POST":
            priority_type = request.form.get("priority_type", "balanced")

            # Parse duration
            duration_raw = request.form.get("duration_minutes", "60")
            try:
                duration_minutes = int(duration_raw)
            except (ValueError, TypeError):
                duration_minutes = 60
            # Valid durations
            valid_durations = [30, 60, 90, 120, 180, 240, 300]
            if duration_minutes not in valid_durations:
                duration_minutes = 60

            duration_slots = duration_minutes // 30

            # Price calculation
            if duration_minutes == 300:
                # 5h package: 200 € instead of 250 €
                estimated_price = 200.0
            else:
                estimated_price = duration_slots * 25.0

            # Parse up to 3 time options
            def parse_date_time(idx):
                d = request.form.get(f"date_option_{idx}")
                t = request.form.get(f"time_option_{idx}")
                d_val = date.fromisoformat(d) if d else None
                t_val = None
                if t:
                    try:
                        t_val = time_mod.strptime(t, "%H:%M")
                        from datetime import time as time_type
                        t_val = time_type(t_val.tm_hour, t_val.tm_min)
                    except Exception:
                        t_val = None
                return d_val, t_val

            d1, t1 = parse_date_time(1)
            d2, t2 = parse_date_time(2)
            d3, t3 = parse_date_time(3)

            p1 = request.form.get("preferred_location_1") or None
            p2 = request.form.get("preferred_location_2") or None
            p3 = request.form.get("preferred_location_3") or None
            # Coach preference
            preferred_coach_raw = request.form.get("preferred_coach_id") or None
            preferred_coach_id = int(preferred_coach_raw) if preferred_coach_raw else None
            training_goal = request.form.get("training_goal")
            user_note = request.form.get("user_note")

            # Validate
            if not d1 or not t1:
                flash("Bitte mindestens einen Zeitwunsch (Datum + Uhrzeit) angeben.", "danger")
                return render_template("booking.html", locations=locations)

            # Build legacy requested_start from option 1
            requested_start = None
            if d1 and t1:
                from datetime import datetime as dt
                requested_start = dt.combine(d1, t1)

            b = Booking(
                user_id=current_user.id,
                priority_type=priority_type,
                duration_minutes=duration_minutes,
                duration_slots=duration_slots,
                estimated_price=estimated_price,
                date_option_1=d1, time_option_1=t1,
                date_option_2=d2, time_option_2=t2,
                date_option_3=d3, time_option_3=t3,
                requested_start=requested_start,
                preferred_location_1_id=int(p1) if p1 else None,
                preferred_location_2_id=int(p2) if p2 else None,
                preferred_location_3_id=int(p3) if p3 else None,
                preferred_coach_id=preferred_coach_id,
                training_goal=training_goal,
                user_note=user_note,
                status="angefragt",
            )
            db.session.add(b)
            db.session.commit()

            # Simulated notification
            send_booking_notification(b)

            flash("Deine Terminanfrage wurde gesendet! Ich prüfe deine Wunschzeiten und melde mich bei dir.", "success")
            return redirect(url_for("dashboard"))
        coaches = Coach.query.filter_by(is_active=True).all()
        return render_template("booking.html", locations=locations, coaches=coaches)

    @app.route("/shop", methods=["GET", "POST"])
    def shop():
        if request.method == "POST":
            # ── Process shop order ──
            selected_ids = request.form.getlist("selected_products")
            if not selected_ids:
                flash("Bitte wähle mindestens ein Produkt aus.", "warning")
                return redirect(url_for("shop"))

            # Resolve product objects
            selected = [p for p in SHOP_PRODUCTS if p["id"] in selected_ids]
            if not selected:
                flash("Ungültige Produktauswahl.", "danger")
                return redirect(url_for("shop"))

            # Customer data
            customer_name = ""
            customer_email = ""
            note = request.form.get("note", "").strip()
            if current_user.is_authenticated:
                customer_name = current_user.name
                customer_email = current_user.email
            else:
                customer_name = request.form.get("customer_name", "").strip()
                customer_email = request.form.get("customer_email", "").strip()

            if not customer_name or not customer_email:
                flash("Bitte Name und E-Mail angeben.", "danger")
                return redirect(url_for("shop"))

            # Create order
            order = ShopOrder(
                user_id=current_user.id if current_user.is_authenticated else None,
                customer_name=customer_name,
                customer_email=customer_email,
                status="requested",
                note=note if note else None,
            )
            db.session.add(order)
            db.session.flush()  # get order.id

            for p in selected:
                item = ShopOrderItem(
                    order_id=order.id,
                    product_name=p["name"],
                    product_category=p["category"],
                    product_link=p["link"] or None,
                    quantity=1,
                )
                db.session.add(item)

            db.session.commit()

            # Send emails
            _send_shop_customer_email(order, selected)
            _send_shop_admin_email(order, selected)

            flash("Deine Produktauswahl wurde gespeichert! Ich bringe die Produkte zur nächsten Schwimmstunde mit.", "success")
            return redirect(url_for("shop"))

        # GET: group products by category
        categories = {}
        for p in SHOP_PRODUCTS:
            cat = p["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(p)

        return render_template("shop.html", categories=categories)

    @app.route("/admin")
    @login_required
    def admin():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))

        from datetime import timedelta

        # ── Wochenplan: navigation with week_offset ──────────────
        week_offset = request.args.get('week_offset', 0, type=int)

        today = date.today()
        # Monday of this week + offset
        week_start = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6)

        # ISO calendar week number
        iso_year, iso_week, _ = week_start.isocalendar()

        # Robust confirmed-status filter (handles legacy values)
        from sqlalchemy import or_, and_

        # Confirmed bookings in this week — match on effective date:
        #   primary: confirmed_date in range
        #   fallback: confirmed_date IS NULL but date_option_1 or requested_start in range
        week_confirmed = Booking.query.filter(
            Booking.status.in_(CONFIRMED_STATUSES),
            or_(
                # Case 1: confirmed_date set and in range
                and_(Booking.confirmed_date >= week_start, Booking.confirmed_date <= week_end),
                # Case 2: confirmed_date NULL, fallback to date_option_1
                and_(Booking.confirmed_date.is_(None), Booking.date_option_1 >= week_start, Booking.date_option_1 <= week_end),
                # Case 3: confirmed_date NULL, date_option_1 NULL, fallback to requested_start
                and_(Booking.confirmed_date.is_(None), Booking.date_option_1.is_(None),
                     Booking.requested_start >= datetime.combine(week_start, datetime.min.time()),
                     Booking.requested_start <= datetime.combine(week_end, datetime.max.time())),
            ),
        ).order_by(Booking.confirmed_date.asc(), Booking.date_option_1.asc(), Booking.requested_start.asc()).all()

        # Pending bookings (angefragt) – shown separately for awareness
        bookings_pending = Booking.query.filter(Booking.status == 'angefragt').order_by(Booking.created_at.desc()).all()

        # All bookings for full overview
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()

        # ── Coaches ───────────────────────────────────────────────
        coaches = Coach.query.order_by(Coach.name.asc()).all()

        # ── Schüler (Users) ──────────────────────────────────────
        students = User.query.filter(User.role != 'admin').order_by(User.name.asc()).all()

        # Build week calendar: list of 7 day-dicts
        import calendar as cal_mod
        week_days = []
        day_names_de = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        for i in range(7):
            d = week_start + timedelta(days=i)
            # Use effective_date for matching (handles bookings with confirmed_date=None)
            day_bookings = [b for b in week_confirmed if get_effective_date(b) == d]
            week_days.append({
                'date': d,
                'day_name': day_names_de[i],
                'day_num': d.day,
                'month': d.strftime('%b'),
                'bookings': day_bookings,
                'is_today': d == today,
            })

        # ── Website-Aktivität (Session-Tracking) ──────────────────
        now = datetime.utcnow()
        five_min_ago = now - timedelta(minutes=5)
        today_start = datetime.combine(now.date(), datetime.min.time())

        try:
            active_sessions = SiteSession.query.filter(
                SiteSession.last_seen >= five_min_ago
            ).count()
            visitors_today = SiteSession.query.filter(
                SiteSession.first_seen >= today_start
            ).count()
            logged_in_online = SiteSession.query.filter(
                SiteSession.last_seen >= five_min_ago,
                SiteSession.is_authenticated == True
            ).count()
            # Last 5 recent visitors (anonymized)
            recent_visitors = SiteSession.query.filter(
                SiteSession.last_seen >= five_min_ago
            ).order_by(SiteSession.last_seen.desc()).limit(10).all()
        except Exception:
            active_sessions = 0
            visitors_today = 0
            logged_in_online = 0
            recent_visitors = []

        return render_template("admin.html",
                               week_days=week_days,
                               week_start=week_start,
                               week_end=week_end,
                               week_offset=week_offset,
                               iso_year=iso_year,
                               iso_week=iso_week,
                               bookings_pending=bookings_pending,
                               bookings=bookings,
                               coaches=coaches,
                               students=students,
                               active_sessions=active_sessions,
                               visitors_today=visitors_today,
                               logged_in_online=logged_in_online,
                               recent_visitors=recent_visitors,
                               now=now)

    @app.route("/admin/booking/<int:booking_id>/confirm", methods=["POST"])
    @login_required
    def admin_confirm_booking(booking_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        booking = Booking.query.get_or_404(booking_id)
        booking.status = "bestaetigt"
        cl = request.form.get("confirmed_location")
        if cl:
            booking.confirmed_location_id = int(cl)
        cd = request.form.get("confirmed_date")
        ct = request.form.get("confirmed_time")
        if cd:
            booking.confirmed_date = date.fromisoformat(cd)
        if ct:
            try:
                t = time_mod.strptime(ct, "%H:%M")
                from datetime import time as time_type
                booking.confirmed_time = time_type(t.tm_hour, t.tm_min)
            except Exception:
                pass
        note = request.form.get("admin_note")
        if note:
            booking.admin_note = note
        db.session.commit()
        # Send confirmation email to customer
        send_customer_confirmation_email(booking)
        flash(f"Booking #{booking.id} bestätigt", "success")
        return redirect(url_for("admin"))

    @app.route("/admin/booking/<int:booking_id>/reject", methods=["POST"])
    @login_required
    def admin_reject_booking(booking_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        booking = Booking.query.get_or_404(booking_id)
        booking.status = "abgelehnt"
        note = request.form.get("admin_note")
        if note:
            booking.admin_note = note
        db.session.commit()
        # Send rejection email to customer
        send_customer_rejection_email(booking, admin_note=note)
        flash(f"Booking #{booking.id} abgelehnt", "info")
        return redirect(url_for("admin"))

    @app.route("/admin/week")
    @login_required
    def admin_week():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        bookings = Booking.query.filter(
            Booking.status.in_(list(CONFIRMED_STATUSES) + ['angefragt'])
        ).order_by(Booking.created_at.desc()).all()
        return render_template("admin_week.html", bookings=bookings)

    @app.route("/admin/booking-history")
    @login_required
    def admin_booking_history():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))

        today = date.today()

        # ── Normalize all bookings into a unified list ──
        all_bookings = Booking.query.order_by(Booking.created_at.desc()).all()

        # ── Compute per-booking display fields ──
        bookings_data = []
        for b in all_bookings:
            eff_date = get_effective_date(b)
            eff_time = get_effective_time(b)

            # Is it past or future?
            is_past = False
            is_future = False
            if eff_date:
                is_past = eff_date < today
                is_future = eff_date > today

            bookings_data.append({
                'booking': b,
                'eff_date': eff_date,
                'eff_time': eff_time,
                'is_past': is_past,
                'is_future': is_future,
            })

        # ── Compute stats ──
        total = len(all_bookings)
        pending_statuses = ['angefragt', 'pending', 'open', 'requested']
        confirmed_statuses_list = list(CONFIRMED_STATUSES)
        open_count = sum(1 for b in all_bookings if (b.status or '').lower() in pending_statuses)
        confirmed_count = sum(1 for b in all_bookings if (b.status or '').lower() in confirmed_statuses_list)
        past_count = sum(1 for bd in bookings_data if bd['is_past'])
        future_count = sum(1 for bd in bookings_data if bd['is_future'])

        # Last booking
        last_booking_at = all_bookings[0].created_at if all_bookings else None

        return render_template(
            "admin_booking_history.html",
            bookings_data=bookings_data,
            total=total,
            open_count=open_count,
            confirmed_count=confirmed_count,
            past_count=past_count,
            future_count=future_count,
            last_booking_at=last_booking_at,
            today=today,
        )

    @app.route("/admin/shop-orders")
    @login_required
    def admin_shop_orders():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        orders = ShopOrder.query.order_by(ShopOrder.created_at.desc()).all()
        return render_template("admin_shop_orders.html", orders=orders)

    @app.route("/admin/settings", methods=["GET", "POST"])
    @login_required
    def admin_settings():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        if request.method == "POST":
            # Benachrichtigungs-E-Mail
            email = request.form.get("booking_notification_email")
            if email:
                AppSetting.set("booking_notification_email", email)
            # Absendername
            sender_name = request.form.get("default_sender_name")
            if sender_name is not None:
                AppSetting.set("default_sender_name", sender_name)
            # Mail-Templates speichern
            tpl_keys = [
                "tpl_new_subject", "tpl_new_body",
                "tpl_confirm_subject", "tpl_confirm_body",
                "tpl_reject_subject", "tpl_reject_body",
                "tpl_alternative_subject", "tpl_alternative_body",
            ]
            for key in tpl_keys:
                val = request.form.get(key)
                if val is not None:
                    AppSetting.set(key, val)
            flash("Einstellungen gespeichert", "success")
            return redirect(url_for("admin_settings"))
        # GET: current values
        current_email = AppSetting.get("booking_notification_email", DEFAULT_ADMIN_EMAIL)
        default_sender_name = AppSetting.get("default_sender_name", "Squalo Schwimmcoaching")
        return render_template("admin_settings.html",
                               current_email=current_email,
                               default_sender_name=default_sender_name,
                               # Mail-Templates: use DB values or defaults
                               tpl_new_subject=AppSetting.get("tpl_new_subject", "Neue Squalo-Terminanfrage"),
                               tpl_new_body=AppSetting.get("tpl_new_body", _default_tpl_new()),
                               tpl_confirm_subject=AppSetting.get("tpl_confirm_subject", "Dein Squalo Schwimmtraining wurde bestätigt"),
                               tpl_confirm_body=AppSetting.get("tpl_confirm_body", _default_tpl_confirm()),
                               tpl_reject_subject=AppSetting.get("tpl_reject_subject", "Deine Squalo Terminanfrage"),
                               tpl_reject_body=AppSetting.get("tpl_reject_body", _default_tpl_reject()),
                               tpl_alternative_subject=AppSetting.get("tpl_alternative_subject", "Alternativvorschlag für dein Squalo Schwimmtraining"),
                               tpl_alternative_body=AppSetting.get("tpl_alternative_body", _default_tpl_alternative()),
                               )

    @app.route("/admin/coaches", methods=["GET", "POST"])
    @login_required
    def admin_coaches():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            title = request.form.get("title", "").strip()
            bio = request.form.get("bio", "").strip()
            strengths = request.form.get("strengths", "").strip()
            swim_style = request.form.get("swim_style", "").strip()
            experience = request.form.get("experience", "").strip()
            specialization = request.form.get("specialization", "").strip()
            cities_served = request.form.get("cities_served", "").strip()
            image_url = request.form.get("image_url", "").strip()
            external_profile_url = request.form.get("external_profile_url", "").strip()
            is_active = request.form.get("is_active") == "1"
            coach_id = request.form.get("coach_id")
            if not name:
                flash("Bitte einen Namen angeben.", "danger")
                return redirect(url_for("admin_coaches"))
            slug = name.lower().replace(" ", "-").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")
            if coach_id:
                coach = Coach.query.get(int(coach_id))
                if coach:
                    coach.name = name
                    coach.slug = slug
                    coach.first_name = first_name
                    coach.last_name = last_name
                    coach.email = email
                    coach.title = title
                    coach.bio = bio
                    coach.strengths = strengths
                    coach.swim_style = swim_style
                    coach.experience = experience
                    coach.specialization = specialization
                    coach.cities_served = cities_served
                    coach.image_url = image_url
                    coach.external_profile_url = external_profile_url
                    coach.is_active = is_active
                    flash(f"Coach {name} aktualisiert.", "success")
            else:
                if Coach.query.filter_by(slug=slug).first():
                    flash("Ein Coach mit diesem Namen existiert bereits.", "danger")
                    return redirect(url_for("admin_coaches"))
                coach = Coach(name=name, slug=slug, first_name=first_name, last_name=last_name,
                              email=email, title=title, bio=bio, strengths=strengths,
                              swim_style=swim_style, experience=experience,
                              specialization=specialization, cities_served=cities_served,
                              image_url=image_url, external_profile_url=external_profile_url,
                              is_active=is_active)
                db.session.add(coach)
                flash(f"Coach {name} angelegt.", "success")
            db.session.commit()
            return redirect(url_for("admin_coaches"))
        coaches = Coach.query.order_by(Coach.name.asc()).all()
        return render_template("admin_coaches.html", coaches=coaches)

    @app.route("/admin/coaches/<int:coach_id>/toggle", methods=["POST"])
    @login_required
    def admin_coach_toggle(coach_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        coach = Coach.query.get_or_404(coach_id)
        coach.is_active = not coach.is_active
        db.session.commit()
        flash(f"Coach {'aktiviert' if coach.is_active else 'deaktiviert'}.", "info")
        return redirect(url_for("admin_coaches"))

    @app.route("/admin/coaches/<int:coach_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_coach_edit(coach_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        coach = Coach.query.get_or_404(coach_id)
        if request.method == "POST":
            coach.first_name = request.form.get("first_name", "").strip()
            coach.last_name = request.form.get("last_name", "").strip()
            coach.email = request.form.get("email", "").strip()
            coach.title = request.form.get("title", "").strip()
            coach.bio = request.form.get("bio", "").strip()
            coach.strengths = request.form.get("strengths", "").strip()
            coach.swim_style = request.form.get("swim_style", "").strip()
            coach.experience = request.form.get("experience", "").strip()
            coach.specialization = request.form.get("specialization", "").strip()
            coach.cities_served = request.form.get("cities_served", "").strip()
            coach.image_url = request.form.get("image_url", "").strip()
            coach.external_profile_url = request.form.get("external_profile_url", "").strip()
            coach.is_active = request.form.get("is_active") == "1"
            # Update name from first/last if provided
            fn = coach.first_name
            ln = coach.last_name
            if fn and ln:
                coach.name = f"{fn} {ln}"
                coach.slug = coach.name.lower().replace(" ", "-").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")
            db.session.commit()
            flash(f"Coach {coach.name} aktualisiert.", "success")
            return redirect(url_for("admin_coaches"))
        return render_template("admin_coach_edit.html", coach=coach)

    @app.route("/admin/coaches/<int:coach_id>/delete", methods=["POST"])
    @login_required
    def admin_coach_delete(coach_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        coach = Coach.query.get_or_404(coach_id)
        name = coach.name
        db.session.delete(coach)
        db.session.commit()
        flash(f"Coach {name} gelöscht.", "info")
        return redirect(url_for("admin_coaches"))

    @app.route("/admin/students")
    @login_required
    def admin_students():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        students = User.query.filter(User.role != 'admin').order_by(User.name.asc()).all()
        # Attach booking count per student
        student_data = []
        for s in students:
            booking_count = Booking.query.filter_by(user_id=s.id).count()
            confirmed_count = Booking.query.filter(Booking.user_id == s.id, Booking.status.in_(CONFIRMED_STATUSES)).count()
            pending_count = Booking.query.filter_by(user_id=s.id, status='angefragt').count()
            student_data.append({
                'user': s,
                'booking_count': booking_count,
                'confirmed_count': confirmed_count,
                'pending_count': pending_count,
            })
        return render_template("admin_students.html", student_data=student_data)

    # ── Student profile / Schülermappe ──────────────────────────
    @app.route("/admin/students/<int:user_id>")
    @login_required
    def admin_student_profile(user_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))

        student = User.query.get_or_404(user_id)
        if student.role == 'admin' and student.id != current_user.id:
            flash("Zugriff verweigert", "danger")
            return redirect(url_for("admin_students"))

        bookings = Booking.query.filter_by(user_id=student.id).order_by(
            Booking.confirmed_date.desc().nullslast(),
            Booking.date_option_1.desc().nullslast(),
            Booking.created_at.desc()
        ).all()

        # Pre-resolve locations and coaches for template
        all_locations = Location.query.all()
        all_coaches = Coach.query.all()
        loc_map = {l.id: l.name for l in all_locations}
        coach_map = {c.id: c.display_name for c in all_coaches}

        # Attach invoice info and resolved data to each booking
        bookings_with_invoices = []
        for b in bookings:
            inv = Invoice.query.filter_by(booking_id=b.id).first()
            eff_date = b.confirmed_date or b.date_option_1 or (
                b.requested_start.date() if b.requested_start else None
            )
            eff_time = b.confirmed_time or b.time_option_1 or (
                b.requested_start.time() if b.requested_start else None
            )
            end_time = None
            if eff_time:
                from datetime import timedelta as _td
                total_min = eff_time.hour * 60 + eff_time.minute + (b.duration_minutes or 60)
                end_time = (datetime.min + _td(minutes=total_min)).time()
            loc_name = loc_map.get(b.confirmed_location_id) or loc_map.get(b.preferred_location_1_id) or '–'
            coach_name = coach_map.get(b.preferred_coach_id, 'Moritz Zentner')
            bookings_with_invoices.append({
                'booking': b,
                'invoice': inv,
                'eff_date': eff_date,
                'eff_time': eff_time,
                'end_time': end_time,
                'loc_name': loc_name,
                'coach_name': coach_name,
            })

        return render_template("student_profile.html",
                               student=student,
                               bookings_with_invoices=bookings_with_invoices)

    # ── Invoice PDF generation ───────────────────────────────────
    @app.route("/admin/students/<int:user_id>/bookings/<int:booking_id>/invoice.pdf")
    @login_required
    def admin_invoice_pdf(user_id, booking_id):
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))

        student = User.query.get_or_404(user_id)
        booking = Booking.query.get_or_404(booking_id)

        # Security: booking must belong to this student
        if booking.user_id != student.id:
            flash("Buchung gehört nicht zu diesem Schüler.", "danger")
            return redirect(url_for("admin_student_profile", user_id=user_id))

        # Check if invoice already exists for this booking
        existing = Invoice.query.filter_by(booking_id=booking.id).first()
        if existing:
            invoice = existing
        else:
            # Create new invoice
            invoice = Invoice(
                invoice_number=Invoice.next_number(),
                user_id=student.id,
                booking_id=booking.id,
                amount=booking.estimated_price or 50.0,
                currency='EUR',
                status='issued',
            )
            db.session.add(invoice)
            db.session.commit()

        # Resolve coach name
        coach_name = 'Moritz Zentner'
        if booking.preferred_coach_id:
            coach = Coach.query.get(booking.preferred_coach_id)
            if coach:
                coach_name = coach.display_name

        # Generate PDF
        from invoice_generator import generate_invoice_pdf
        try:
            pdf_bytes = generate_invoice_pdf(
                invoice=invoice,
                booking=booking,
                user=student,
                coach_name=coach_name,
            )
        except Exception as e:
            flash(f'Fehler bei der PDF-Erstellung: {e}', 'danger')
            return redirect(url_for('admin_student_profile', user_id=user_id))

        # Update pdf_generated_at
        from datetime import datetime as _dt
        invoice.pdf_generated_at = _dt.utcnow()
        db.session.commit()

        filename = f'Rechnung_{invoice.invoice_number}.pdf'
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename,
        )

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(uploads_path, filename)

    @app.cli.command("initdb")
    def initdb_command():
        db.create_all()
        print("Initialized DB")

    @app.cli.command("seed")
    def seed_command():
        db.create_all()
        
        # ── Admin-User (gleiche Logik wie create_app) ──────────────
        admin_email = os.environ.get("ADMIN_EMAIL", "zentner.moritz@gmail.com")
        admin_password = os.environ.get("ADMIN_INITIAL_PASSWORD", "admin123")
        
        admin_user = User.query.filter_by(email=admin_email).first()
        if admin_user:
            admin_user.role = "admin"
            admin_user.password_hash = generate_password_hash(admin_password)
            print(f"[OK] Admin aktualisiert: {admin_email}")
        else:
            admin_user = User(
                name="Admin",
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                role="admin"
            )
            db.session.add(admin_user)
            print(f"[OK] Admin neu angelegt: {admin_email}")
            
        if not User.query.filter_by(email="user@squalo.local").first():
            user = User(
                name="Max Mustermann", 
                email="user@squalo.local", 
                password_hash=generate_password_hash("password"), 
                role="user"
            )
            db.session.add(user)
            
        # Seed all Squalo swim locations (idempotent - prevents duplicates)
        # Import seed data from seed_data.py
        try:
            from seed_data import SWIM_LOCATIONS
        except ImportError:
            # Fallback to hardcoded locations if seed_data.py is not available
            SWIM_LOCATIONS = [
                ("Stadtbad Tiergarten", "Schwimmbad", "Mitte", "open", "verified", "25°C", "low", "https://maps.google.com"),
                ("Kombibad Seestraße", "Kombibad", "Charlottenburg", "open", "verified", "28°C", "medium", "https://maps.google.com"),
                ("Schwimm- und Sprunghalle im Europasportpark", "Kombibad", "Neukölln", "open", "verified", "26°C", "medium", "https://maps.google.com"),
                ("Sommerbad Neukölln", "Sommerbad", "Neukölln", "open", "not_verified", "22°C", "medium", "https://maps.google.com"),
                ("Prinzenbad", "Sommerbad", "Mitte", "open", "verified", "24°C", "low", "https://maps.google.com"),
                ("Stadtbad Charlottenburg – Alte Halle", "Schwimmbad", "Charlottenburg", "open", "verified", "27°C", "low", "https://maps.google.com"),
                ("Strandbad Plötzensee", "Strandbad", "Reinickendorf", "closed", "verified", "18°C", "high", "https://maps.google.com"),
                ("Flughafensee", "See", "Reinickendorf", "open", "verified", "20°C", "low", "https://maps.google.com"),
                ("Strandbad Wannsee", "Strandbad", "Steglitz-Zehlendorf", "open", "verified", "22°C", "medium", "https://maps.google.com"),
                ("Stadtbad Schöneberg", "Schwimmbad", "Schöneberg", "open", "verified", "26°C", "medium", "https://maps.google.com"),
                ("Stadtbad Wilmersdorf I", "Schwimmbad", "Wilmersdorf", "open", "verified", "25°C", "low", "https://maps.google.com"),
                ("Stadtbad Wilmersdorf II", "Schwimmbad", "Wilmersdorf", "open", "verified", "25°C", "low", "https://maps.google.com"),
                ("Kombibad Gropiusstadt – Halle", "Kombibad", "Neukölln", "open", "verified", "28°C", "medium", "https://maps.google.com"),
                ("Kombibad Gropiusstadt – Sommerbad", "Sommerbad", "Neukölln", "open", "verified", "24°C", "medium", "https://maps.google.com"),
                ("Sommerbad Kreuzberg", "Sommerbad", "Kreuzberg", "open", "verified", "23°C", "low", "https://maps.google.com"),
                ("Sommerbad Olympiastadion", "Sommerbad", "Charlottenburg", "open", "verified", "26°C", "medium", "https://maps.google.com"),
                ("Kombibad Spandau Süd", "Kombibad", "Spandau", "open", "verified", "27°C", "medium", "https://maps.google.com"),
                ("Stadtbad Lankwitz", "Schwimmbad", "Steglitz-Zehlendorf", "open", "verified", "25°C", "low", "https://maps.google.com"),
                ("Tegeler See", "See", "Reinickendorf", "open", "verified", "19°C", "low", "https://maps.google.com"),
                ("Stadtbad Fischerinsel", "Schwimmbad", "Mitte", "open", "verified", "24°C", "low", "https://maps.google.com"),
                ("Müggelsee", "See", "Treptow-Köpenick", "open", "verified", "21°C", "low", "https://maps.google.com"),
                ("Strandbad Friedrichshagen", "Strandbad", "Treptow-Köpenick", "open", "verified", "22°C", "medium", "https://maps.google.com"),
            ]
        
        # Seed locations that don't already exist (idempotent)
        for location_data in SWIM_LOCATIONS:
            name = location_data["name"]
            existing_location = Location.query.filter_by(name=name).first()
            if existing_location:
                # Update existing location if data is missing
                if not existing_location.location_type:
                    existing_location.location_type = location_data["location_type"]
                if not existing_location.district:
                    existing_location.district = location_data["district"]
                if not existing_location.official_status:
                    existing_location.official_status = location_data["official_status"]
                if not existing_location.verified_status:
                    existing_location.verified_status = location_data["verified_status"]
                if not existing_location.water_temperature:
                    existing_location.water_temperature = location_data["water_temperature"]
                if not existing_location.crowd_level:
                    existing_location.crowd_level = location_data["crowd_level"]
                if not existing_location.maps_url:
                    existing_location.maps_url = location_data["maps_url"]
                if not existing_location.latitude:
                    existing_location.latitude = location_data["latitude"]
                if not existing_location.longitude:
                    existing_location.longitude = location_data["longitude"]
                if not existing_location.address:
                    existing_location.address = location_data["address"]
            else:
                # Create new location
                loc = Location(
                    name=location_data["name"], 
                    location_type=location_data["location_type"], 
                    district=location_data["district"], 
                    address=location_data["address"], 
                    latitude=location_data["latitude"], 
                    longitude=location_data["longitude"], 
                    official_status=location_data["official_status"], 
                    verified_status=location_data["verified_status"], 
                    water_temperature=location_data["water_temperature"], 
                    crowd_level=location_data["crowd_level"], 
                    maps_url=location_data["maps_url"]
                )
                db.session.add(loc)
                
        db.session.commit()
        print(f"Seeded {len(SWIM_LOCATIONS)} Squalo swim locations")

    @app.route("/impressum")
    def impressum():
        return render_template("impressum.html")

    # ── robots.txt ──────────────────────────────────────────────
    @app.route("/robots.txt")
    def robots_txt():
        base = get_public_base_url()
        content = (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /admin\n"
            "Disallow: /dashboard\n"
            "Disallow: /feed\n"
            "Disallow: /login\n"
            "Disallow: /register\n"
            f"\nSitemap: {base}/sitemap.xml\n"
        )
        return Response(content, mimetype='text/plain')

    # ── sitemap.xml ─────────────────────────────────────────────
    @app.route("/sitemap.xml")
    def sitemap_xml():
        base = get_public_base_url()
        pages = [
            ('/', '1.0', 'daily'),
            ('/coaches', '0.8', 'weekly'),
            ('/shop', '0.6', 'weekly'),
            ('/booking', '0.5', 'monthly'),
            ('/impressum', '0.3', 'monthly'),
        ]
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for path, priority, changefreq in pages:
            xml_parts.append('  <url>')
            xml_parts.append(f'    <loc>{base}{path}</loc>')
            xml_parts.append(f'    <changefreq>{changefreq}</changefreq>')
            xml_parts.append(f'    <priority>{priority}</priority>')
            xml_parts.append('  </url>')
        xml_parts.append('</urlset>')
        return Response('\n'.join(xml_parts), mimetype='application/xml')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

