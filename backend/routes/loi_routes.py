from flask import Blueprint, request, redirect, url_for, render_template
from app import db
from models import LOIForm

loi_bp = Blueprint('loi_bp', __name__, url_prefix='/loi')

@loi_bp.route('/', methods=['GET', 'POST'])
def loi_form():
    if request.method == 'POST':
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
            seller_note_open=True if request.form.get('seller_note_open') else False
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('loi_form.html')
