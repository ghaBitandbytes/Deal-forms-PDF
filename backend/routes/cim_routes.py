from flask import Blueprint, request, render_template, send_file
from werkzeug.utils import secure_filename
from app import db, mail
from flask_mail import Message
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import requests
from datetime import datetime
from models import CIMForm

cim_bp = Blueprint('cim_bp', __name__, url_prefix='/cim')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, '..', 'static', 'pdfs', 'cim')
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'static', 'uploads', 'cim')

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@cim_bp.route('/', methods=['GET', 'POST'])
def cim_form():
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files.get('supporting_files')
        file_path = None
        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(file_path)

        # Save form data to DB
        new_entry = CIMForm(
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
            gm_in_place=request.form.get('gm_in_place'),
            tenure_gm=request.form.get('tenure_gm'),
            num_employees=request.form.get('num_employees'),
            total_adjustments=request.form.get('total_adjustments'),
            search_fit=request.form.get('search_narrative_fit'),
            search_connection=request.form.get('relate_to_narrative'),
            deal_interest=request.form.get('likes_dislikes'),
            questions_concerns=request.form.get('questions_concerns'),
            uploaded_file=file_path,
            confirm_terms=True if request.form.get('confirm_terms') else False
        )

        db.session.add(new_entry)
        db.session.commit()

        # PDF generation
        pdf_filename = f"CIM_{new_entry.full_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

        c = canvas.Canvas(pdf_path, pagesize=A4)
        y = 800
        line_height = 22
        c.setFont("Helvetica-Bold", 14)
        c.drawString(180, y, "CIM Summary")
        y -= 40
        c.setFont("Helvetica", 11)

        fields = [
            ("Full Name", new_entry.full_name),
            ("Email", new_entry.email),
            ("Industry", new_entry.industry),
            ("Location", new_entry.location),
            ("Purchase Price", new_entry.purchase_price),
            ("Revenue", new_entry.revenue),
            ("Average SDE", new_entry.avg_sde),
            ("Seller Role", new_entry.seller_role),
            ("Reason for Selling", new_entry.reason_for_selling),
            ("Owner Involvement", new_entry.owner_involvement),
            ("GM in Place", new_entry.gm_in_place),
            ("Tenure of GM", new_entry.tenure_gm),
            ("Number of Employees", new_entry.num_employees),
            ("Total $ Adjustments", new_entry.total_adjustments),
            ("Search Narrative Fit", new_entry.search_fit),
            ("Relation to Search Narrative", new_entry.search_connection),
            ("Deal Interest", new_entry.deal_interest),
            ("Questions/Concerns", new_entry.questions_concerns)
        ]

        for label, value in fields:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, f"{label}:")
            c.setFont("Helvetica", 11)
            c.drawString(200, y, str(value or ""))
            y -= line_height
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = 800

        c.save()
        print(f"PDF successfully saved at: {pdf_path}")

        # --- Email Sending ---
        try:
            pdf_url = f"http://127.0.0.1:5000/static/pdfs/cim/{pdf_filename}"
            msg = Message(
                subject=f"New CIM Submission from {new_entry.full_name}",
                recipients=["syeda.ghazia@bitandbytes.net"]
            )
            msg.body = (
                f"A new CIM form has been submitted.\n\n"
                f"Full Name: {new_entry.full_name}\n"
                f"Email: {new_entry.email}\n"
                f"Industry: {new_entry.industry}\n\n"
                f"You can view or download the generated PDF here:\n{pdf_url}\n\n"
                f"— DealForms PDF System"
            )
            mail.send(msg)
            print("Email sent successfully to syeda.ghazia@bitandbytes.net")
        except Exception as e:
            print("Error sending email:", e)

        # --- Slack Notification ---
        try:
            slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
            slack_message = {
                "text": (
                    f":page_facing_up: *New CIM Form Submitted!*\n"
                    f"*Name:* {new_entry.full_name}\n"
                    f"*Email:* {new_entry.email}\n"
                    f"*Industry:* {new_entry.industry}\n"
                    f"*PDF:* {pdf_url}"
                )
            }
            response = requests.post(slack_webhook_url, json=slack_message)
            if response.status_code == 200:
                print("Slack notification sent successfully.")
            else:
                print(f"Failed to send Slack notification: {response.text}")
        except Exception as e:
            print("Error sending Slack notification:", e)

        return '', 200

    return render_template('cim_form.html')
