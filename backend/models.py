from app import db

class LOIForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    industry = db.Column(db.String(120))
    location = db.Column(db.String(120))
    purchase_price = db.Column(db.String(50))
    revenue = db.Column(db.String(50))
    avg_sde = db.Column(db.String(50))
    seller_role = db.Column(db.String(120))
    reason_for_selling = db.Column(db.Text)
    owner_involvement = db.Column(db.Text)
    customer_concentration_risk = db.Column(db.Text)
    deal_competitiveness = db.Column(db.Text)
    seller_note_open = db.Column(db.Boolean)

    # ✅ New fields
    cim_fit_narrative = db.Column(db.String(10))  # Yes/No
    relate_to_narrative = db.Column(db.Text)
    likes_dislikes = db.Column(db.Text)
    questions_concerns = db.Column(db.Text)

    uploaded_file = db.Column(db.String(255))  # store filename/path
    confirm_terms = db.Column(db.Boolean)
