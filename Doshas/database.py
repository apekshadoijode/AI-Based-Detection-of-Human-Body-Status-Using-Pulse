from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    profile_pic = db.Column(db.String(200))
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with DoshaData
    dosha_data = db.relationship('DoshaData', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DoshaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Body characteristics
    body_frame = db.Column(db.String(50), nullable=False)
    hair_type = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_complexion = db.Column(db.String(50), nullable=False)
    body_weight = db.Column(db.String(50), nullable=False)
    nails = db.Column(db.String(50), nullable=False)
    teeth_size_color = db.Column(db.String(50), nullable=False)
    work_pace = db.Column(db.String(50), nullable=False)
    mental_activity = db.Column(db.String(50), nullable=False)
    memory = db.Column(db.String(50), nullable=False)
    sleep_pattern = db.Column(db.String(50), nullable=False)
    weather_conditions = db.Column(db.String(50), nullable=False)
    reaction_adverse = db.Column(db.String(50), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    eating_habit = db.Column(db.String(50), nullable=False)
    hunger = db.Column(db.String(50), nullable=False)
    body_temperature = db.Column(db.String(50), nullable=False)
    joints = db.Column(db.String(50), nullable=False)
    nature = db.Column(db.String(50), nullable=False)
    body_energy = db.Column(db.String(50), nullable=False)
    voice_quality = db.Column(db.String(50), nullable=False)
    body_odor = db.Column(db.String(50), nullable=False)
    
    # Results
    vata_score = db.Column(db.Integer)
    pitta_score = db.Column(db.Integer)
    kapha_score = db.Column(db.Integer)
    primary_dosha = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
