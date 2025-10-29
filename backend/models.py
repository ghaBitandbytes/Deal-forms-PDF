from app import db

# ------------------ LOIForm (existing) ------------------
class LOIForm(db.Model):
    __tablename__ = "loi_forms"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(200))
    location = db.Column(db.String(200))
    purchase_price = db.Column(db.Float)
    revenue = db.Column(db.Float)
    avg_sde = db.Column(db.Float)
    seller_role = db.Column(db.String(100))
    reason_for_selling = db.Column(db.Text)
    owner_involvement = db.Column(db.Text)
    customer_concentration_risk = db.Column(db.Text)
    deal_competitiveness = db.Column(db.Text)
    seller_note_open = db.Column(db.Boolean, default=False)
    cim_fit_narrative = db.Column(db.String(10))
    relate_to_narrative = db.Column(db.Text)
    likes_dislikes = db.Column(db.Text)
    questions_concerns = db.Column(db.Text)
    uploaded_file = db.Column(db.String(300))
    confirm_terms = db.Column(db.Boolean, default=False)

# ------------------ CIMForm (new) ------------------
class CIMForm(db.Model):
    __tablename__ = "cim_forms"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    avg_sde = db.Column(db.Float, nullable=True)
    seller_role = db.Column(db.String(100), nullable=True)
    reason_for_selling = db.Column(db.Text, nullable=False)
    owner_involvement = db.Column(db.Text, nullable=True)
    gm_in_place = db.Column(db.String(10), nullable=True)
    tenure_gm = db.Column(db.String(50), nullable=True)
    num_employees = db.Column(db.Integer, nullable=True)
    total_adjustments = db.Column(db.Float, nullable=True)
    search_fit = db.Column(db.String(10), nullable=False)
    search_connection = db.Column(db.Text, nullable=True)
    deal_interest = db.Column(db.Text, nullable=True)
    questions_concerns = db.Column(db.Text, nullable=True)
    uploaded_file = db.Column(db.String(300), nullable=True)
    confirm_terms = db.Column(db.Boolean, default=False)
