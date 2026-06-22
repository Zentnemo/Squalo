"""
Squalo Schwimmcoaching — PDF Invoice Generator
Uses ReportLab to create professional PDF invoices.
"""
import io
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

# ── Squalo Brand Colors ──────────────────────────────────────────
DARK_BLUE = colors.HexColor('#003d4d')
TURQUOISE = colors.HexColor('#00a8cc')
ORANGE = colors.HexColor('#ff8c1a')
LIGHT_GRAY = colors.HexColor('#f5f5f5')
MID_GRAY = colors.HexColor('#999999')
TEXT_DARK = colors.HexColor('#1a1a1a')
TEXT_LIGHT = colors.HexColor('#666666')
WHITE = colors.white

# ── Provider / Invoice defaults ──────────────────────────────────
PROVIDER = {
    'name': 'Moritz Zentner UG (haftungsbeschränkt)',
    'street': 'Limburger Straße 5',
    'zip_city': '13353 Berlin',
    'country': 'Deutschland',
    'representative': 'Moritz Alexander Zentner',
    'email': 'hello@cloudbrainer.com',
    'register': 'Amtsgericht Berlin-Charlottenburg',
    'hrb': '282726',
    'ust_id': 'wird nachgereicht',
}

PAYMENT = {
    'iban': 'wird ergänzt',
    'bic': 'wird ergänzt',
    'hinweis': 'Steuerliche Angaben werden ergänzt.',
}

DEFAULT_PRICE = 50.00


def _format_de_date(dt):
    """Format datetime as DD.MM.YYYY."""
    if dt is None:
        return '–'
    if isinstance(dt, datetime):
        return dt.strftime('%d.%m.%Y')
    # Handle date objects
    return dt.strftime('%d.%m.%Y')


def _format_de_time(t):
    """Format time as HH:MM."""
    if t is None:
        return '–'
    return t.strftime('%H:%M')


def _format_eur(amount):
    """Format float as German EUR string."""
    if amount is None:
        amount = DEFAULT_PRICE
    return f'{amount:,.2f} €'.replace(',', 'X').replace('.', ',').replace('X', '.')


def _get_logo_path():
    """Return path to Squalo logo, or None if not found."""
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base, 'static', 'images', 'squalo-logo.png'),
        os.path.join(base, 'static', 'images', 'squalo_logo.png'),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def generate_invoice_pdf(invoice, booking, user, coach_name='Moritz Zentner'):
    """
    Generate a professional PDF invoice and return it as bytes.

    Args:
        invoice: Invoice model instance
        booking: Booking model instance
        user: User model instance (the student/customer)
        coach_name: Name of the coach

    Returns:
        bytes: PDF file content
    """
    buf = io.BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=15 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    # ── Custom styles ────────────────────────────────────────────
    s_title = ParagraphStyle(
        'InvoiceTitle', parent=styles['Title'],
        fontSize=22, textColor=DARK_BLUE, spaceAfter=2 * mm,
        fontName='Helvetica-Bold',
    )
    s_subtitle = ParagraphStyle(
        'InvoiceSubtitle', parent=styles['Normal'],
        fontSize=10, textColor=TEXT_LIGHT, spaceAfter=6 * mm,
    )
    s_heading = ParagraphStyle(
        'SectionHeading', parent=styles['Heading2'],
        fontSize=11, textColor=DARK_BLUE, spaceBefore=4 * mm, spaceAfter=2 * mm,
        fontName='Helvetica-Bold',
    )
    s_normal = ParagraphStyle(
        'NormalText', parent=styles['Normal'],
        fontSize=9, textColor=TEXT_DARK, leading=13,
    )
    s_small = ParagraphStyle(
        'SmallText', parent=styles['Normal'],
        fontSize=8, textColor=TEXT_LIGHT, leading=11,
    )
    s_right = ParagraphStyle(
        'RightAligned', parent=s_normal,
        alignment=TA_RIGHT,
    )
    s_right_bold = ParagraphStyle(
        'RightBold', parent=s_right,
        fontName='Helvetica-Bold', fontSize=10,
    )
    s_amount_large = ParagraphStyle(
        'AmountLarge', parent=s_right,
        fontName='Helvetica-Bold', fontSize=14, textColor=DARK_BLUE,
    )

    elements = []

    # ── Logo / Branding ──────────────────────────────────────────
    logo_path = _get_logo_path()
    if logo_path:
        from reportlab.platypus import Image as RLImage
        try:
            img = RLImage(logo_path, width=45 * mm, height=15 * mm)
            img.hAlign = 'LEFT'
            elements.append(img)
            elements.append(Spacer(1, 3 * mm))
        except Exception:
            # Fallback: text branding
            elements.append(Paragraph(
                '<font color="#003d4d" size="16"><b>SQUALO</b></font> '
                '<font color="#00a8cc" size="10">Schwimmcoaching</font>',
                styles['Normal']
            ))
            elements.append(Spacer(1, 3 * mm))
    else:
        # No logo — text branding fallback
        elements.append(Paragraph(
            '<font color="#003d4d" size="16"><b>SQUALO</b></font> '
            '<font color="#00a8cc" size="10">Schwimmcoaching</font>',
            styles['Normal']
        ))
        elements.append(Spacer(1, 3 * mm))

    # ── Invoice header ───────────────────────────────────────────
    header_data = [
        [
            Paragraph('<b>RECHNUNG</b>', ParagraphStyle(
                'h', parent=s_title, fontSize=18, spaceAfter=0)),
            Paragraph(
                f'<b>Rechnungsnr.:</b> {invoice.invoice_number}<br/>'
                f'<b>Datum:</b> {_format_de_date(invoice.issued_at)}<br/>'
                f'<b>Seite:</b> 1 von 1',
                ParagraphStyle('hdr', parent=s_right, fontSize=9, leading=13)),
        ]
    ]
    header_table = Table(header_data, colWidths=[100 * mm, 70 * mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6 * mm))

    # ── Horizontal rule ──────────────────────────────────────────
    elements.append(HRFlowable(
        width='100%', thickness=1, color=TURQUOISE,
        spaceAfter=4 * mm, spaceBefore=2 * mm
    ))

    # ── Provider block (left) + Customer block (right) ──────────
    provider_text = (
        f'<b>{PROVIDER["name"]}</b><br/>'
        f'{PROVIDER["street"]}<br/>'
        f'{PROVIDER["zip_city"]}<br/>'
        f'{PROVIDER["country"]}<br/><br/>'
        f'Vertreten durch: {PROVIDER["representative"]}<br/>'
        f'E-Mail: {PROVIDER["email"]}<br/>'
        f'HRB: {PROVIDER["hrb"]}<br/>'
        f'USt-IdNr.: {PROVIDER["ust_id"]}'
    )

    # Customer data — use whatever is available
    customer_lines = []
    full_name = user.name or ''
    if full_name:
        customer_lines.append(f'<b>{full_name}</b>')
    if user.email:
        customer_lines.append(f'E-Mail: {user.email}')
    customer_text = '<br/>'.join(customer_lines) if customer_lines else '<i>Kunde</i>'

    addr_data = [
        [
            Paragraph(provider_text, s_normal),
            Paragraph(
                f'<b>Rechnungsempfänger:</b><br/>{customer_text}',
                s_normal
            ),
        ]
    ]
    addr_table = Table(addr_data, colWidths=[90 * mm, 80 * mm])
    addr_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(addr_table)
    elements.append(Spacer(1, 6 * mm))

    # ── Leistungsbeschreibung ────────────────────────────────────
    elements.append(Paragraph('<b>Leistungsbeschreibung</b>', s_heading))

    # Resolve effective date/time/location
    eff_date = booking.confirmed_date or booking.date_option_1 or (
        booking.requested_start.date() if booking.requested_start else None
    )
    eff_time = booking.confirmed_time or booking.time_option_1 or (
        booking.requested_start.time() if booking.requested_start else None
    )
    eff_location = None
    if booking.confirmed_location_id:
        from models import Location
        loc = Location.query.get(booking.confirmed_location_id)
        if loc:
            eff_location = loc.name

    duration = booking.duration_minutes or 60
    amount = booking.estimated_price or DEFAULT_PRICE

    # Build service description
    goal_text = ''
    if booking.training_goal:
        goal_text = f'<br/>Schwerpunkt: {booking.training_goal}'

    service_lines = [
        f'1x Personal Schwimmcoaching mit Schwerpunkt Schwimmen und Triathlon{goal_text}',
        f'Termin: {_format_de_date(eff_date)}, {_format_de_time(eff_time)} Uhr',
    ]
    if eff_location:
        service_lines.append(f'Ort: {eff_location}')
    service_lines.append(f'Coach: {coach_name}')
    service_lines.append(f'Dauer: {duration} Minuten')

    service_text = '<br/>'.join(service_lines)
    elements.append(Paragraph(service_text, s_normal))
    elements.append(Spacer(1, 4 * mm))

    # ── Price table ──────────────────────────────────────────────
    price_data = [
        [
            Paragraph('<b>Position</b>', s_normal),
            Paragraph('<b>Betrag</b>', ParagraphStyle('pr', parent=s_normal, alignment=TA_RIGHT)),
        ],
        [
            Paragraph(
                f'Personal Coaching / Schwimmcoaching<br/>'
                f'<font size="8" color="#666666">'
                f'{_format_de_date(eff_date)} · {_format_de_time(eff_time)}'
                f'{(" · " + eff_location) if eff_location else ""}'
                f'</font>',
                s_normal
            ),
            Paragraph(f'<b>{_format_eur(amount)}</b>', s_right_bold),
        ],
    ]
    price_table = Table(price_data, colWidths=[120 * mm, 50 * mm])
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4 * mm),
        ('TOPPADDING', (0, 0), (-1, 0), 3 * mm),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3 * mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3 * mm),
        ('TOPPADDING', (0, 1), (-1, -1), 3 * mm),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3 * mm),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, TURQUOISE),
        ('LINEABOVE', (0, 1), (-1, 1), 0.5, TURQUOISE),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, TURQUOISE),
    ]))
    elements.append(price_table)
    elements.append(Spacer(1, 3 * mm))

    # ── Total ────────────────────────────────────────────────────
    total_data = [
        [
            Paragraph('<b>Gesamtbetrag (brutto):</b>', s_normal),
            Paragraph(f'<b>{_format_eur(amount)}</b>', s_amount_large),
        ]
    ]
    total_table = Table(total_data, colWidths=[120 * mm, 50 * mm])
    total_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3 * mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3 * mm),
        ('TOPPADDING', (0, 0), (-1, -1), 3 * mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3 * mm),
        ('LINEABOVE', (0, 0), (-1, 0), 1, DARK_BLUE),
        ('LINEBELOW', (0, 0), (-1, 0), 1, DARK_BLUE),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f7fa')),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 8 * mm))

    # ── Payment information ──────────────────────────────────────
    elements.append(Paragraph('<b>Zahlungsinformationen</b>', s_heading))
    payment_text = (
        f'Bitte überweisen Sie den Gesamtbetrag auf folgendes Konto:<br/><br/>'
        f'<b>IBAN:</b> {PAYMENT["iban"]}<br/>'
        f'<b>BIC:</b> {PAYMENT["bic"]}<br/>'
        f'<b>Verwendungszweck:</b> {invoice.invoice_number}<br/><br/>'
        f'<b>Zahlungsziel:</b> 14 Tage'
    )
    elements.append(Paragraph(payment_text, s_normal))
    elements.append(Spacer(1, 5 * mm))

    # ── Tax notice ───────────────────────────────────────────────
    elements.append(HRFlowable(
        width='100%', thickness=0.5, color=MID_GRAY,
        spaceAfter=3 * mm, spaceBefore=3 * mm
    ))
    tax_text = (
        f'<font size="8" color="#666666">'
        f'{PAYMENT["hinweis"]}<br/>'
        f'USt-IdNr.: {PROVIDER["ust_id"]}<br/>'
        f'Registergericht: {PROVIDER["register"]} · HRB {PROVIDER["hrb"]}'
        f'</font>'
    )
    elements.append(Paragraph(tax_text, s_small))
    elements.append(Spacer(1, 6 * mm))

    # ── Footer ───────────────────────────────────────────────────
    elements.append(HRFlowable(
        width='100%', thickness=0.5, color=TURQUOISE,
        spaceAfter=3 * mm, spaceBefore=2 * mm
    ))
    footer_text = (
        f'<font size="7" color="#999999">'
        f'{PROVIDER["name"]} · {PROVIDER["street"]} · {PROVIDER["zip_city"]}<br/>'
        f'E-Mail: {PROVIDER["email"]} · '
        f'Vielen Dank für dein Vertrauen! 🦈'
        f'</font>'
    )
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer', parent=s_small, alignment=TA_CENTER, fontSize=7
    )))

    # ── Build PDF ────────────────────────────────────────────────
    doc.build(elements)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes
