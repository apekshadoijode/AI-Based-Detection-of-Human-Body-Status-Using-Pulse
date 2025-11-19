_**AI-Based Detection of Human Body Status Using Pulse (Inspired by Nadi Pariksha)**_

This project is a Machine Learning + Flask web application that predicts four different human body status categories using pulse-related features, inspired by the Ayurvedic diagnostic method Nadi Pariksha.
It combines traditional Ayurvedic insights with modern ML techniques to build a practical, data-driven health assessment system.

_**🌟 Overview**_

This system analyzes pulse-related input data and uses a trained Random Forest Classifier to predict the user’s body status.
The project includes:

A complete ML training pipeline (Jupyter Notebook)

A Flask web UI for real-time predictions

Multiple preprocessing, scaling, and encoding pipelines

Model deployment with .pkl files for fast inference

Datasets (dataset.csv, dataset1.csv) are used to extract statistical & physiological features related to pulse signals.

_**🎯 Project Features**_

✔️ Preprocessing of pulse-related numerical & categorical features

✔️ Feature scaling and encoding for consistent input

✔️ Random Forest classifier for multi-class classification

✔️ Flask-based prediction interface

✔️ HTML templates for user-friendly UI

✔️ Model files saved and reused for fast inference

_**🧠 Machine Learning Details**_

Model Used

Random Forest Classifier (best performing model)

Supporting Files

random_forest_model.pkl – Trained ML model

scaler.pkl – StandardScaler for numerical features

label_encoders.pkl – Encoders for categorical columns

feature_names.pkl – Ensures input order consistency

**🔍 Prediction Output**

The system predicts 4 body status categories, derived from the dataset.
(If you'd like, I can insert the exact names of the 4 categories.)

_**🏗️ Tech Stack**_


**Backend**

Python

Flask

**Machine Learning**

scikit-learn

Pandas

NumPy

Pickle

**Notebooks**
Jupyter Notebook

**Frontend**
HTML (Jinja2 templates)
CSS (from static/)

_**📂 Project Structure**_

                                                                      Doshas/
                                                                      │
                                                                      ├── app.py                         # Flask application
                                                                      ├── database.py                    # Database logic (optional)
                                                                      ├── dataset.csv                    # Main dataset
                                                                      ├── dataset1.csv                   # Additional dataset
                                                                      │
                                                                      ├── training.ipynb                 # Model training steps
                                                                      ├── prediction.ipynb               # Testing predictions
                                                                      │
                                                                      ├── random_forest_model.pkl        # Final trained model
                                                                      ├── scaler.pkl                     # Scaler for features
                                                                      ├── label_encoders.pkl             # Encoders for categories
                                                                      ├── feature_names.pkl              # Saved feature names
                                                                      │
                                                                      ├── templates/                     # UI HTML templates
                                                                      │     ├── index.html
                                                                      │     └── result.html
                                                                      │
                                                                      ├── static/                        # CSS, JS, assets
                                                                      │
                                                                      └── instance/                      # Flask instance folder

_**🚀 How to Run the Project**_
📌 Option 1: Run the Flask Web Application

This is the main app used for real-time predictions.

1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Start the Flask Server
python app.py

3️⃣ Open the Application in Your Browser
http://127.0.0.1:5000/

📓 Option 2: Run the Jupyter Notebooks

Use this option to view:

training.ipynb → Model creation, preprocessing, training

prediction.ipynb → Testing with saved .pkl model

Run Jupyter Notebook
jupyter notebook


This will open the notebook interface in your browser.

_**📊 Training & Results**_

Random Forest gave the highest accuracy among tested models

Features were scaled and encoded for robust predictions

Model components were saved separately for reproducibility

(Add your accuracy, confusion matrix, or graphs here if you want.)

**_📘 Ayurvedic Basis_**

This system is inspired by Nadi Pariksha, a diagnostic method in Ayurveda that uses pulse characteristics to assess dosha balance and body conditions.
The project attempts to translate these ancient diagnostic principles into quantifiable ML features.

_**📚 References**_

Research papers on pulse signal analysis

Ayurvedic literature on Nadi Pariksha

Scikit-learn official documentation

Flask official documentation
_
**👩‍💻 Author**_

Apeksha D M
GitHub: apekshadoijode
