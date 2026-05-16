import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "civic_ultra_key"

# Auto-set paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'civic_reports.db')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)

# Updated Model with Phone Field
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    location = db.Column(db.String(100))
    phone = db.Column(db.String(15)) # Connection point
    filename = db.Column(db.String(200))
    status = db.Column(db.String(50), default="In Progress (Nagar Nigam)")
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    reports = Report.query.order_by(Report.date_posted.desc()).all()
    return render_template('index.html', reports=reports)

@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form.get('phone')
    # SIMULATION: In a real app, this sends an SMS via Twilio API
    print(f"--- SMS SENT TO {phone}: Your {request.form.get('category')} complaint is now ACTIVE. ---")
    
    new_report = Report(
        category=request.form.get('category'),
        location=request.form.get('location'),
        phone=phone
    )
    db.session.add(new_report)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)