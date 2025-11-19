from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db, User, DoshaData
from werkzeug.utils import secure_filename
from PIL import Image
import os
from datetime import datetime
import pickle
import pandas as pd
from difflib import get_close_matches

# --- Load model, encoders, scaler, and feature names ---
model_filename = "random_forest_model.pkl"   # Change if needed
model = pickle.load(open(model_filename, "rb"))
label_encoders = pickle.load(open("label_encoders.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
trained_features = pickle.load(open("feature_names.pkl", "rb"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dosha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_dosha(data):
    """Calculate dosha scores based on user inputs"""
    vata_indicators = ['Thin', 'Dry', 'Dark', 'Light', 'Brittle', 'Small', 'Fast', 'Quick', 'Poor', 'Light', 'Cold', 'Anxious', 'Changeable', 'Irregular', 'Variable', 'Cold', 'Cracking', 'Anxious', 'Low', 'Hoarse', 'None']
    pitta_indicators = ['Medium', 'Oily', 'Reddish', 'Medium', 'Flexible', 'Medium', 'Moderate', 'Sharp', 'Good', 'Moderate', 'Hot', 'Angry', 'Intense', 'Regular', 'Strong', 'Hot', 'Loose', 'Ambitious', 'Moderate', 'Sharp', 'Strong']
    kapha_indicators = ['Large', 'Greasy', 'Light', 'Oily', 'Heavy', 'Thick', 'Large', 'Slow', 'Slow', 'Excellent', 'Heavy', 'Cool', 'Calm', 'Stable', 'Regular', 'Low', 'Cool', 'Stiff', 'Calm', 'High', 'Soft', 'Mild']
    
    vata_score = 0
    pitta_score = 0
    kapha_score = 0
    
    # Convert form data to list for comparison
    form_data = [
        data.get('body_frame'), data.get('hair_type'), data.get('hair_color'),
        data.get('skin_complexion'), data.get('body_weight'), data.get('nails'),
        data.get('teeth_size_color'), data.get('work_pace'), data.get('mental_activity'),
        data.get('memory'), data.get('sleep_pattern'), data.get('weather_conditions'),
        data.get('reaction_adverse'), data.get('mood'), data.get('eating_habit'),
        data.get('hunger'), data.get('body_temperature'), data.get('joints'),
        data.get('nature'), data.get('body_energy'), data.get('voice_quality'),
        data.get('body_odor')
    ]
    
    for i, value in enumerate(form_data):
        if value == vata_indicators[i]:
            vata_score += 1
        if value == pitta_indicators[i]:
            pitta_score += 1
        if value == kapha_indicators[i]:
            kapha_score += 1
    
    # Determine primary dosha
    scores = {'Vata': vata_score, 'Pitta': pitta_score, 'Kapha': kapha_score}
    primary_dosha = max(scores, key=scores.get)
    
    return vata_score, pitta_score, kapha_score, primary_dosha

def get_recommendations(primary_dosha):
    """Get food, exercise, and diet recommendations based on dosha"""
    recommendations = {
        'Vata': {
            'food': ['Warm cooked foods', 'Root vegetables', 'Nuts and seeds', 'Dairy products', 'Sweet fruits'],
            'avoid': ['Raw vegetables', 'Cold drinks', 'Dry foods', 'Beans'],
            'exercise': ['Gentle yoga', 'Walking', 'Swimming', 'Tai Chi'],
            'diet': ['Regular meals', 'Warm and moist foods', 'Sweet, sour, and salty tastes']
        },
        'Pitta': {
            'food': ['Cool foods', 'Sweet fruits', 'Green vegetables', 'Grains', 'Dairy'],
            'avoid': ['Spicy foods', 'Sour fruits', 'Fermented foods', 'Alcohol'],
            'exercise': ['Moderate exercise', 'Swimming', 'Cycling', 'Moon salutations'],
            'diet': ['Cool and refreshing foods', 'Sweet, bitter, and astringent tastes']
        },
        'Kapha': {
            'food': ['Light foods', 'Raw vegetables', 'Spices', 'Legumes', 'Fruits'],
            'avoid': ['Heavy foods', 'Dairy', 'Sweet fruits', 'Oily foods'],
            'exercise': ['Vigorous exercise', 'Running', 'Aerobics', 'Sun salutations'],
            'diet': ['Light and warm foods', 'Pungent, bitter, and astringent tastes']
        }
    }
    
    return recommendations.get(primary_dosha, {})

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        gender = request.form['gender']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        # Handle profile picture upload
        profile_pic = None
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create unique filename
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Resize image
                img = Image.open(filepath)
                img.thumbnail((200, 200))
                img.save(filepath)
                
                profile_pic = filename
        
        # Create new user
        new_user = User(
            name=name,
            phone=phone,
            email=email,
            dob=dob,
            gender=gender,
            profile_pic=profile_pic
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    dosha_history = DoshaData.query.filter_by(user_id=user.id).order_by(DoshaData.created_at.desc()).all()
    
    return render_template('profile.html', user=user, dosha_history=dosha_history)

@app.route('/data_entry', methods=['GET', 'POST'])
def data_entry():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        input_data = {
            "Body Frame": request.form['body_frame'],
            "Type of Hair": request.form['type_of_hair'],
            "Color of Hair": request.form['color_of_hair'],
            "Skin": request.form['skin'],
            "Complexion": request.form['complexion'],
            "Body Weight": request.form['body_weight'],
            "Nails": request.form['nails'],
            "Size and Color of the Teeth": request.form['size_and_color_of_the_teeth'],
            "Pace of Performing Work": request.form['pace_of_performing_work'],
            "Mental Activity": request.form['mental_activity'],
            "Memory": request.form['memory'],
            "Sleep Pattern": request.form['sleep_pattern'],
            "Weather Conditions": request.form['weather_conditions'],
            "Reaction under Adverse Situations": request.form['reaction_under_adverse_situations'],
            "Mood": request.form['mood'],
            "Eating Habit": request.form['eating_habit'],
            "Hunger": request.form['hunger'],
            "Body Temperature": request.form['body_temperature'],
            "Joints": request.form['joints'],
            "Nature": request.form['nature'],
            "Body Energy": request.form['body_energy'],
            "Quality of Voice": request.form['quality_of_voice'],
            "Body Odor": request.form['body_odor']
            }

        input_df = pd.DataFrame([input_data])

        # --- Auto-match similar columns if names differ ---
        input_cols = input_df.columns.tolist()
        missing_from_input = [f for f in trained_features if f not in input_cols]
        unseen_in_input = [f for f in input_cols if f not in trained_features]

        if missing_from_input or unseen_in_input:
            print("\n⚠️ Column name mismatch detected. Attempting automatic correction...")
            rename_map = {}
            for missing in missing_from_input:
                match = get_close_matches(missing, unseen_in_input, n=1, cutoff=0.6)
                if match:
                    rename_map[match[0]] = missing
                    print(f"🔄 Renamed '{match[0]}' → '{missing}'")

            input_df.rename(columns=rename_map, inplace=True)

        # --- Encode categorical columns ---
        for col in input_df.columns:
            if col in label_encoders:
                input_df[col] = label_encoders[col].transform(input_df[col])

        # --- Ensure column order matches training ---
        input_df = input_df.reindex(columns=trained_features)

        # --- Scale features ---
        input_scaled = scaler.transform(input_df)

        # --- Predict ---
        prediction = model.predict(input_scaled)[0]

        # --- Decode Dosha label ---
        if "Dosha" in label_encoders:
            predicted_dosha = label_encoders["Dosha"].inverse_transform([prediction])[0]
        else:
            predicted_dosha = prediction

        print(f"\n🔹 Predicted Dosha: {predicted_dosha}")

        results=predicted_dosha
        recommendations = {
                    "Vata": {
                    "food_recommended": [
                    "Warm, cooked, and oily foods",
                    "Sweet fruits like bananas and mangoes",
                    "Soups and stews"
                    ],
                    "food_avoid": [
                        "Cold and raw foods",
                        "Caffeine",
                        "Dried fruits and beans"
                    ],
                    "exercise": [
                        "Gentle yoga",
                        "Tai chi",
                        "Walking or light jogging"
                    ],
                    "lifestyle": [
                        "Maintain a regular routine",
                        "Keep warm and stay grounded",
                        "Avoid overstimulation"
                    ]
                },
                "Pitta": {
                    "food_recommended": [
                        "Cool and fresh foods",
                        "Sweet fruits like melons and grapes",
                        "Leafy greens and cucumbers"
                    ],
                    "food_avoid": [
                        "Spicy, fried, and oily foods",
                        "Alcohol and caffeine",
                        "Fermented foods"
                    ],
                    "exercise": [
                        "Swimming",
                        "Evening walks",
                        "Cooling yoga postures"
                    ],
                    "lifestyle": [
                        "Stay cool physically and emotionally",
                        "Practice meditation or pranayama",
                        "Avoid overwork"
                    ]
                },
                "Kapha": {
                    "food_recommended": [
                        "Light and warm foods",
                        "Spices like ginger and black pepper",
                        "Bitter and astringent vegetables"
                    ],
                    "food_avoid": [
                        "Heavy, oily, or cold foods",
                        "Dairy and sweets",
                        "Fried foods"
                    ],
                    "exercise": [
                        "Jogging, cycling, or dancing",
                        "Intense cardio",
                        "Dynamic yoga"
                    ],
                    "lifestyle": [
                        "Stay active and motivated",
                        "Avoid oversleeping",
                        "Engage in stimulating activities"
                    ]
                }
            }
        data = recommendations.get(results, {})

        
        return render_template('result.html', results=results,data=data)
    
    return render_template('data_entry.html')

@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    
    
    
    recommendations = ""#get_recommendations(dosha_data.primary_dosha)
    
    return render_template('result.html', 
                         dosha_data="", 
                         recommendations=recommendations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
