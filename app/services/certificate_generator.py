from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def generate_certificate(
    recipient_name: str,
    course_name: str,
    event_date: str,
    output_path: str
):
    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        output_path,
        pagesize=landscape(A4)
    )

    # Border
    pdf.setLineWidth(3)
    pdf.rect(
        15 * mm,
        15 * mm,
        page_width - 30 * mm,
        page_height - 30 * mm
    )

    # Title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 50 * mm,
        "CERTIFICATE OF COMPLETION"
    )

    # Main text
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 80 * mm,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 100 * mm,
        recipient_name
    )

    # Course
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 125 * mm,
        f"for successfully completing {course_name}"
    )

    # Date
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 150 * mm,
        f"Date: {event_date}"
    )

    pdf.save()
      