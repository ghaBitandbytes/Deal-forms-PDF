from flask import Blueprint, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from app import db
from models import LOIForm

loi_bp = Blueprint('loi_bp', __name__, url_prefix='/loi')

UPLOAD_FOLDER = 'backend/static/uploads'
PDF_FOLDER = 'backend/static/pdfs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)


@loi_bp.route('/', methods=['GET', 'POST'])
def loi_form():
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files.get('supporting_files')
        file_path = None
        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(file_path)

        # Save form data to DB
        new_entry = LOIForm(
            full_name=request.form.get('full_name'),
            email=request.form.get('email'),
            industry=request.form.get('industry'),
            location=request.form.get('location'),
            purchase_price=request.form.get('purchase_price'),
            revenue=request.form.get('revenue'),
            avg_sde=request.form.get('avg_sde'),
            seller_role=request.form.get('seller_role'),
            reason_for_selling=request.form.get('reason_for_selling'),
            owner_involvement=request.form.get('owner_involvement'),
            customer_concentration_risk=request.form.get('customer_concentration_risk'),
            deal_competitiveness=request.form.get('deal_competitiveness'),
            seller_note_open=True if request.form.get('seller_note_open') else False,
            cim_fit_narrative=request.form.get('cim_fit_narrative'),
            relate_to_narrative=request.form.get('relate_to_narrative'),
            likes_dislikes=request.form.get('likes_dislikes'),
            questions_concerns=request.form.get('questions_concerns'),
            uploaded_file=file_path,
            confirm_terms=True if request.form.get('confirm_terms') else False
        )

        db.session.add(new_entry)
        db.session.commit()

        # Generate PDF
        pdf_filename = f"LOI_{new_entry.full_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

        c = canvas.Canvas(pdf_path, pagesize=A4)
        y = 800
        line_height = 22
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, y, "Letter of Intent Summary")
        y -= 40
        c.setFont("Helvetica", 11)

        fields = [
            ("Name", new_entry.full_name),
            ("Email", new_entry.email),
            ("Industry", new_entry.industry),
            ("Location", new_entry.location),
            ("Purchase Price", new_entry.purchase_price),
            ("Revenue", new_entry.revenue),
            ("Avg SDE", new_entry.avg_sde),
            ("Seller Role", new_entry.seller_role),
            ("Reason for Selling", new_entry.reason_for_selling),
            ("Owner Involvement", new_entry.owner_involvement),
            ("Customer Concentration Risk", new_entry.customer_concentration_risk),
            ("Competition", new_entry.deal_competitiveness),
            ("Seller Note", "Yes" if new_entry.seller_note_open else "No"),
            ("Search Narrative Fit", new_entry.cim_fit_narrative),
            ("Search Narrative Connection", new_entry.relate_to_narrative),
            ("Deal Interest", new_entry.likes_dislikes),
            ("Questions/Concerns", new_entry.questions_concerns)
        ]

        for label, value in fields:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, f"{label}:")
            c.setFont("Helvetica", 11)
            c.drawString(200, y, str(value or ""))
            y -= line_height

            # New page if near bottom
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = 800

        c.save()

        return send_file(pdf_path, as_attachment=True)

    return render_template('loi_form.html')
