"""Minimal Squalo Flask application (clean single-file app factory).

Provides small runnable Flask app that re-uses project's models and templates.
Includes minimal auth (register/login), required pages and CLI helpers.
"""

import os
import time as time_mod
from datetime import datetime, date
from zoneinfo import ZoneInfo
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pathlib import Path

from config import Config
from models import db, User, Location, Booking, FeedPost, TrainingNote, AppSetting, Coach, CoachReview
from location_status import compute_location_status

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def send_booking_notification(booking):
    """Simulate sending an email notification for a new booking."""
    try:
        admin_email = AppSetting.get("booking_notification_email", "info@squalo.local")
        user = User.query.get(booking.user_id)
        subject = "Neue Squalo-Terminanfrage"

        time_options = []
        if booking.date_option_1:
            t1 = booking.time_option_1.strftime('%H:%M') if booking.time_option_1 else '?'
            time_options.append(f"{booking.date_option_1.strftime('%d.%m.%Y')} {t1} Uhr")
        if booking.date_option_2:
            t2 = booking.time_option_2.strftime('%H:%M') if booking.time_option_2 else '?'
            time_options.append(f"{booking.date_option_2.strftime('%d.%m.%Y')} {t2} Uhr")
        if booking.date_option_3:
            t3 = booking.time_option_3.strftime('%H:%M') if booking.time_option_3 else '?'
            time_options.append(f"{booking.date_option_3.strftime('%d.%m.%Y')} {t3} Uhr")
        # Fallback to legacy field
        if not time_options and booking.requested_start:
            time_options.append(booking.requested_start.strftime('%d.%m.%Y %H:%M') + " Uhr")

        locs = []
        for lid in [booking.preferred_location_1_id, booking.preferred_location_2_id, booking.preferred_location_3_id]:
            if lid:
                loc = Location.query.get(lid)
                if loc:
                    locs.append(loc.name)

        lines = [
            f"An: {admin_email}",
            f"Betreff: {subject}",
            "",
            f"Kunde: {user.name if user else 'unbekannt'}",
            f"E-Mail: {user.email if user else 'unbekannt'}",
            f"Zeitoptionen: {', '.join(time_options) if time_options else 'keine'}",
            f"Wunschorte: {', '.join(locs) if locs else 'keine'}",
            f"Coach-Präferenz: {booking.preferred_coach.name if booking.preferred_coach else 'keine'}",
            f"Trainingsziel: {booking.training_goal or 'keines'}",
            f"Notiz: {booking.user_note or 'keine'}",
            f"Admin-Link: /admin/booking/{booking.id}",
        ]
        print("=" * 60)
        print("SIMULIERTE BUCHUNGSBENACHRICHTIGUNG")
        print("=" * 60)
        for line in lines:
            print(line)
        print("=" * 60)
    except Exception as e:
        print(f"Notification error (non-critical): {e}")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Ensure instance directory exists for SQLite database
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    uploads_path = os.path.join(os.path.dirname(__file__), "static", "uploads")
    os.makedirs(uploads_path, exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Initialize database and seed data if needed
    with app.app_context():
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
                              "official_status", "verified_status", "water_temperature", "crowd_level", "maps_url"]:
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
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
        notes = TrainingNote.query.filter_by(user_id=current_user.id).order_by(TrainingNote.created_at.desc()).all()
        return render_template("dashboard.html", bookings=bookings, notes=notes)

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

    @app.route("/shop")
    def shop():
        return render_template("shop.html")

    @app.route("/admin")
    @login_required
    def admin():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        users = User.query.order_by(User.name.asc()).all()
        coaches = Coach.query.order_by(Coach.name.asc()).all()
        return render_template("admin.html", bookings=bookings, users=users, coaches=coaches)

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
        flash(f"Booking #{booking.id} abgelehnt", "info")
        return redirect(url_for("admin"))

    @app.route("/admin/week")
    @login_required
    def admin_week():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        bookings = Booking.query.filter(
            Booking.status.in_(["angefragt", "bestaetigt"])
        ).order_by(Booking.created_at.desc()).all()
        return render_template("admin_week.html", bookings=bookings)

    @app.route("/admin/settings", methods=["GET", "POST"])
    @login_required
    def admin_settings():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        if request.method == "POST":
            email = request.form.get("booking_notification_email")
            if email:
                AppSetting.set("booking_notification_email", email)
                flash("Einstellungen gespeichert", "success")
            return redirect(url_for("admin_settings"))
        current_email = AppSetting.get("booking_notification_email", "info@squalo.local")
        return render_template("admin_settings.html", current_email=current_email)

    @app.route("/admin/coaches", methods=["GET", "POST"])
    @login_required
    def admin_coaches():
        if getattr(current_user, "role", "") != "admin":
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            title = request.form.get("title", "").strip()
            bio = request.form.get("bio", "").strip()
            strengths = request.form.get("strengths", "").strip()
            image_url = request.form.get("image_url", "").strip()
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
                    coach.title = title
                    coach.bio = bio
                    coach.strengths = strengths
                    coach.image_url = image_url
                    coach.is_active = is_active
                    flash(f"Coach {name} aktualisiert.", "success")
            else:
                if Coach.query.filter_by(slug=slug).first():
                    flash("Ein Coach mit diesem Namen existiert bereits.", "danger")
                    return redirect(url_for("admin_coaches"))
                coach = Coach(name=name, slug=slug, title=title, bio=bio,
                              strengths=strengths, image_url=image_url, is_active=is_active)
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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

