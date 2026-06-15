"""
Adaptive location status helper for Squalo Schwimmcoaching.

Computes context-aware opening status, water temperature, crowd level,
and verified label for each location based on Berlin local time and
location type.  Uses default opening hours when no real data exists.
No external API calls, no random values.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

# ── Default opening hours (minutes since midnight) ──
INDOOR_OPEN  = 6 * 60   # 06:00
INDOOR_CLOSE = 22 * 60  # 22:00
OUTDOOR_OPEN  = 9 * 60   # 09:00
OUTDOOR_CLOSE = 20 * 60  # 20:00
NIGHT_START = 22 * 60 + 30  # 22:30
NIGHT_END   = 6 * 60        # 06:00


def is_like_lake(loc_type: str) -> bool:
    """True for free-access natural waters."""
    return any(t in loc_type for t in ['see', 'badestelle'])


def is_indoor(loc_type: str) -> bool:
    """True for managed indoor pools."""
    return any(t in loc_type for t in ['schwimmbad', 'hallenbad', 'kombibad', 'indoor'])


def is_outdoor(loc_type: str) -> bool:
    """True for managed outdoor facilities."""
    return any(t in loc_type for t in ['sommerbad', 'freibad', 'strandbad', 'outdoor'])


def compute_location_status(location, now: datetime | None = None) -> dict:
    """
    Compute adaptive status labels for a *location* (Location model instance).

    Parameters
    ----------
    location : Location
        SQLAlchemy model instance with fields: location_type, official_status,
        water_temperature, crowd_level, verified_status.
    now : datetime, optional
        Current datetime.  If omitted, uses Europe/Berlin timezone.

    Returns
    -------
    dict with keys:
        opening_status       – full human-readable string
        opening_status_short – short label for badges / popups
        opening_class        – CSS class ('open' / 'geschlossen')
        water_temperature_label
        crowd_level_label
        crowd_class          – CSS class for crowd badge
        verified_label
    """
    if now is None:
        now = datetime.now(ZoneInfo('Europe/Berlin'))

    current_minutes = now.hour * 60 + now.minute
    is_night = current_minutes >= NIGHT_START or current_minutes < NIGHT_END

    loc_type = (location.location_type or '').lower() if hasattr(location, 'location_type') else ''
    lake = is_like_lake(loc_type)
    indoor = is_indoor(loc_type)
    outdoor = is_outdoor(loc_type)

    # ── 1. Opening status ──────────────────────────────────────────
    if lake:
        if is_night:
            opening_status = 'Frei zugänglich · Baden auf eigene Verantwortung'
            opening_status_short = 'Frei zugänglich'
        else:
            opening_status = 'Frei zugänglich'
            opening_status_short = 'Frei zugänglich'
        opening_class = 'open'

    elif indoor:
        if is_night or not (INDOOR_OPEN <= current_minutes < INDOOR_CLOSE):
            opening_status = 'Geschlossen'
            opening_status_short = 'Geschlossen'
            opening_class = 'geschlossen'
        else:
            opening_status = 'Heute voraussichtlich geöffnet'
            opening_status_short = 'Geöffnet'
            opening_class = 'open'

    elif outdoor:
        if is_night or not (OUTDOOR_OPEN <= current_minutes < OUTDOOR_CLOSE):
            opening_status = 'Geschlossen'
            opening_status_short = 'Geschlossen'
            opening_class = 'geschlossen'
        else:
            opening_status = 'Heute voraussichtlich geöffnet'
            opening_status_short = 'Geöffnet'
            opening_class = 'open'
    else:
        # Fallback for unknown types
        opening_status = 'Geöffnet' if not is_night else 'Geschlossen'
        opening_status_short = opening_status
        opening_class = 'open' if not is_night else 'geschlossen'

    # ── 2. Water temperature ───────────────────────────────────────
    raw_temp = (location.water_temperature or '').strip()
    if raw_temp and raw_temp not in ('–', '-', '', 'wird aktualisiert'):
        water_temperature_label = raw_temp
    elif indoor:
        water_temperature_label = 'ca. 26–28 °C'
    else:
        water_temperature_label = 'wird aktualisiert'

    # ── 3. Crowd level ─────────────────────────────────────────────
    if is_night and not lake:
        crowd_level_label = 'geschlossen'
        crowd_class = 'geschlossen'
    elif is_night and lake:
        crowd_level_label = 'ruhig'
        crowd_class = 'niedrig'
    else:
        raw_crowd = (location.crowd_level or '').strip()
        if raw_crowd and raw_crowd not in ('–', '-', '', 'unbekannt'):
            crowd_level_label = raw_crowd
            # Normalise for CSS
            cls = raw_crowd.lower().replace(' ', '-').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
            crowd_class = cls
        else:
            crowd_level_label = 'unbekannt'
            crowd_class = ''

    # ── 4. Verified status ─────────────────────────────────────────
    raw_verified = (location.verified_status or '').strip()
    if raw_verified == 'verified':
        verified_label = 'Standort geprüft'
    else:
        verified_label = 'ausstehend'

    return {
        'opening_status': opening_status,
        'opening_status_short': opening_status_short,
        'opening_class': opening_class,
        'water_temperature_label': water_temperature_label,
        'crowd_level_label': crowd_level_label,
        'crowd_class': crowd_class,
        'verified_label': verified_label,
    }
