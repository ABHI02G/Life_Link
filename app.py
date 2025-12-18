from flask import Flask, render_template, request, redirect, jsonify, url_for, session
import pyrebase
import os 
import requests
from dotenv import load_dotenv
import datetime
import uuid
import logging
import math
from datetime import datetime,timezone
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key_987654"

# -------------------------------
# USER (app) Firebase config
# -------------------------------
userconfig = {
    'apiKey': "AIzaSyDQhYxw8xDgFZ-lW2r-62pTXV62RsnJlsI",
    'authDomain': "user-30233.firebaseapp.com",
    'projectId': "user-30233",
    'storageBucket': "user-30233.appspot.com",
    'messagingSenderId': "247559550638",
    'appId': "1:247559550638:web:581f6fa3f8bc12bc76df3f",
    'measurementId': "G-WD61D4DDV6",
    'databaseURL': "https://user-30233-default-rtdb.firebaseio.com"
}
firebase = pyrebase.initialize_app(userconfig)
auth = firebase.auth()
db = firebase.database()
db_user_appointments = firebase.database()


# -------------------------------
# HOSPITAL Firebase config (fixed bucket)
# -------------------------------
hospitalconfig = {
    "apiKey": "AIzaSyDX6Cp0wEDKWvB6isatbpoxgaMJAtTcoKw",
    "authDomain": "hospital2-facf0.firebaseapp.com",
    "projectId": "hospital2-facf0",
    "storageBucket": "hospital2-facf0.appspot.com",   # <-- corrected
    "messagingSenderId": "146056979244",
    "appId": "1:146056979244:web:f74910effa1bff809a4289",
    "measurementId": "G-0TXWEDHD8N",
    "databaseURL": "https://hospital2-facf0-default-rtdb.firebaseio.com/"
}
firebase_hospital = pyrebase.initialize_app(hospitalconfig)
auth_hospital = firebase_hospital.auth()
db_hospital = firebase_hospital.database()
bloodconfig = {
  "apiKey": "AIzaSyAKoXg6iq7pafOevDg4yFS2rwy7PCNE630",
  "authDomain": "blooddatabase-8e98e.firebaseapp.com",
  "databaseURL": "https://blooddatabase-8e98e-default-rtdb.firebaseio.com/",
  "projectId": "blooddatabase-8e98e",
  "storageBucket": "blooddatabase-8e98e.firebasestorage.app",
  "messagingSenderId": "274153479776",
  "appId": "1:274153479776:web:2d952e106cabb1169d2d05",
  "measurementId": "G-ZDCW4J1SJQ",
  "databaseURL": "https://blooddatabase-8e98e-default-rtdb.firebaseio.com/"
}
firebase_blood = pyrebase.initialize_app(bloodconfig)
db_blood = firebase_blood.database()
organconfig = {
    "apiKey": "AIzaSyDSA49V396sFFFtKymJBc78hz7kc9zBCVg",
    "authDomain": "organdatabase-9023e.firebaseapp.com",
    "projectId": "organdatabase-9023e",
    "storageBucket": "organdatabase-9023e.firebasestorage.app",
    "messagingSenderId": "591330653454",
    "appId": "1:591330653454:web:51dd1b79476d4f5f39935f",
    "measurementId": "G-N4MQB3675S",
    "databaseURL": "https://organdatabase-9023e-default-rtdb.firebaseio.com/"
}
firebase_organ = pyrebase.initialize_app(organconfig)
db_organ = firebase_organ.database()

appointmentconfig = {
    "apiKey": "AIzaSyC9XeDTJIEpw5DrVU5kdYSCscxO8B1eHqA",
    "authDomain": "appointment-8587a.firebaseapp.com",
    "databaseURL": "https://appointment-8587a-default-rtdb.firebaseio.com",
    "projectId": "appointment-8587a",
    "storageBucket": "appointment-8587a.firebasestorage.app",
    "messagingSenderId": "1003941320556",
    "appId": "1:1003941320556:web:95c02fa81d8f49a8c18549",
    "measurementId": "G-YFZYEVE01T",
    "databaseURL": "https://appointment-8587a-default-rtdb.firebaseio.com"
}

firebase_appointment = pyrebase.initialize_app(appointmentconfig)
db_appointment = firebase_appointment.database()

# -------------------------------
# ROUTES - simple renderers
# -------------------------------
@app.route('/')
def about():
    return render_template('about.html')

@app.route('/registration')
def register():
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/h_dashboard')
def h_dashboard():
    return render_template('h_dashboard.html')

@app.route('/ai-center')
def ai():
    return render_template('ai-center.html')

# -------------------------------
# USER: register (POST)
# -------------------------------
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    otp = data.get("otp")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user.get("localId")
        if not uid:
            return jsonify({"status": "error", "message": "Auth failed"}), 400

        db.child("users").child(uid).set({
            "name": name,
            "age": age,
            "email": email,
            "phone": phone,
            "otp": otp,
            "role": "user"
        })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("🔥 NON-FATAL ERROR (register_user):", e)
        return jsonify({"status": "error", "message": str(e)}), 400

# -------------------------------
# USER: login (POST)
# -------------------------------
@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    try:
        user = auth.sign_in_with_email_and_password(email, password)   # <-- fixed auth variable
        # Optionally fetch user info or token here
        session['logged_in'] = True
        session['role'] = "user"
        # you can store uid if needed:
        session['uid'] = user.get('localId')
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("LOGIN ERROR (login_user):", e)
        return jsonify({"status": "error"}), 400

# -------------------------------
# HOSPITAL: register (POST)
# -------------------------------
@app.route('/register_hospital', methods=['POST'])
def register_hospital():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    contact = data.get("contact")
    otp = data.get("otp")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    try:
        hospital = auth_hospital.create_user_with_email_and_password(email, password)
        uid = hospital.get("localId")
        if not uid:
            return jsonify({"status": "error", "message": "Hospital auth failed"}), 400

        db_hospital.child("hospitals").child(uid).set({
            "name": name,
            "email": email,
            "contact": contact,
            "otp": otp,
            "role": "hospital",
        })

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("🔥 HOSPITAL ERROR (register_hospital):", e)
        return jsonify({"status": "error", "message": str(e)}), 400


# -------------------------------
# HOSPITAL: login (POST) - properly registered
# -------------------------------
@app.route('/login_hospital', methods=['POST'])
def login_hospital():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    try:
        hospital_user = auth_hospital.sign_in_with_email_and_password(email, password)

        session['logged_in'] = True
        session['role'] = "hospital"
        session['uid'] = hospital_user.get('localId')
        session['idToken'] = hospital_user['idToken']   # 🔥 REQUIRED
        session['refreshToken'] = hospital_user['refreshToken']


        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("HOSPITAL LOGIN ERROR (login_hospital):", e)
        return jsonify({"status": "error"}), 400

@app.route('/blood')
def blood():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "user":
        return redirect(url_for("h_dashboard"))

    return render_template('blood.html')
# -------------------------------
# Run
# -------------------------------
@app.route('/api/analyze_symptoms', methods=['POST'])
def analyze_symptoms_ai():
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    if not GROQ_API_KEY:
        return jsonify({"error": "Missing GROQ_API_KEY"}), 500

    url = "https://api.groq.com/openai/v1/chat/completions"

    data = request.get_json()
    symptoms = data.get("symptoms", "")

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": f"""
Analyze these symptoms and return ONLY JSON:

Symptoms: {symptoms}

JSON format:
{{
  "severity": "low | medium | high",
  "categories": [],
  "red_flags": [],
  "recommendation": ""
}}
"""
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    response_json = r.json()

    # GROQ ERROR?
    if "error" in response_json:
        print("GROQ ERROR:", response_json)
        return jsonify({"error": "Groq API error", "details": response_json}), 500

    # CORRECT WAY TO GET TEXT
   # NEW SAFE WAY TO GET AI TEXT FROM GROQ
    ai_text = (
    response_json.get("choices", [{}])[0].get("message", {}).get("content") 
    or response_json.get("choices", [{}])[0].get("text")
)

    

    if not ai_text:
        print("GROQ MISSING TEXT:", response_json)
        return jsonify({"error": "No text returned", "raw": response_json}), 500

    return jsonify({"ai_result": ai_text})



@app.route('/api/healthscore_ai', methods=['POST'])
def healthscore_ai():
    if 'uid' not in session:
        return jsonify({"error": "Not logged in"}), 401

    uid = session['uid']
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    if not GROQ_API_KEY:
        return jsonify({"error": "Missing GROQ_API_KEY"}), 500

    # User input from AI page
    user_input = request.get_json() or {}

    # Pull user profile
    try:
        profile = db.child("user_profiles").child(uid).get().val()
    except Exception as e:
        print("PROFILE FETCH ERROR:", e)
        return jsonify({"error": "Profile fetch failed"}), 500

    if not profile:
        profile = {}

    # Merge profile + manual inputs
    combined = {
        "profile": profile,
        "inputs": user_input
    }

    prompt = f"""
You are a medical risk assessment AI. Analyze the combined data below
and generate *one unified* health score.

Combined data:
{combined}

Return ONLY JSON:
{{
  "score": 0,
  "risk_level": "low | medium | high",
  "bmi": 0,
  "bmi_label": "",
  "primary_factors": [],
  "warnings": [],
  "recommendations": []
}}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{ "role": "user", "content": prompt }]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers).json()

    ai_text = (
        r.get("choices", [{}])[0].get("message", {}).get("content")
        or r.get("choices", [{}])[0].get("text")
    )

    if not ai_text:
        return jsonify({"error": "No AI text"}), 500

    return jsonify({"ai_result": ai_text})


@app.route('/api/doctor_match', methods=['POST'])
def doctor_match_ai():
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        return jsonify({"error": "Missing GROQ_API_KEY"}), 500

    url = "https://api.groq.com/openai/v1/chat/completions"
    data = request.get_json()
    symptoms = data.get("symptoms", "")
    city = data.get("city", "Unknown")

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": f"""
User symptoms: {symptoms}
City: {city}

Return ONLY JSON:
{{
  "specialty": "",
  "urgency": "",
  "suggested_doctors": ["", "", ""],
  "reason": ""
}}
"""
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    response_json = r.json()

    if "error" in response_json:
        print("GROQ ERROR:", response_json)
        return jsonify({"error": "Groq API error", "details": response_json}), 500

    # SAFE TEXT EXTRACTION
    ai_text = (
        response_json.get("choices", [{}])[0].get("message", {}).get("content")
        or response_json.get("choices", [{}])[0].get("text")
    )

    if not ai_text:
        print("GROQ MISSING TEXT:", response_json)
        return jsonify({"error": "No AI text", "raw": response_json}), 500

    return jsonify({"ai_result": ai_text})
@app.route('/api/prescription_ai', methods=['POST'])
def prescription_ai():
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        return jsonify({"error": "Missing GROQ_API_KEY"}), 500

    url = "https://api.groq.com/openai/v1/chat/completions"

    data = request.get_json()
    meds = data.get("meds", "")
    issue = data.get("issue", "")

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": f"""
User medicines currently taking:
{meds}

User health issue:
{issue}

Return ONLY JSON in the exact format below:

{{
  "summary": "",
  "possible_causes": [],
  "recommended_medicines": [],  
  "questions_to_ask_doctor": [],
  "notes": ""
}}

Rules:
- Medicines MUST be real and safe.
- Do NOT invent dangerous drugs.

"""
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    response_json = r.json()

    if "error" in response_json:
        print("GROQ ERROR:", response_json)
        return jsonify({"error": "Groq API error", "details": response_json}), 500

    ai_text = (
        response_json.get("choices", [{}])[0].get("message", {}).get("content")
        or response_json.get("choices", [{}])[0].get("text")
    )

    if not ai_text:
        return jsonify({"error": "No AI text", "raw": response_json}), 500

    return jsonify({"ai_result": ai_text})

@app.route('/rare-medicines')
def rare_medicine():
    return render_template('rare_medicine.html')
@app.route('/api/search_medicine', methods=['GET'])
def search_medicine():
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    print("Loaded Google Key:", GOOGLE_API_KEY)

    if not GOOGLE_API_KEY:
        return jsonify({"error": "Missing GOOGLE_API_KEY"}), 500

    medicine = request.args.get("q", "").strip()
    city = request.args.get("city", "").strip()

    if not medicine:
        return jsonify({"error": "No medicine provided"}), 400

    # Build Google Places text search query
    search_text = medicine + " pharmacy"
    if city:
        search_text += " " + city

    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={search_text}&key={GOOGLE_API_KEY}"
    )

    response = requests.get(url)
    print("\n\n=======GOOGLE RAW RESPONSE======")
    print(response.text)
    print("=====================================")
    data = response.json()

    if "error_message" in data:
        return jsonify({"error": data["error_message"]}), 500

    places = []
    for place in data.get("results", []):
        places.append({
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating"),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "place_id": place.get("place_id"),
        })

    # GOOGLE MAP EMBED URL
    embed_map_url = (
        "https://www.google.com/maps/embed/v1/search"
        f"?key={GOOGLE_API_KEY}&q={search_text}"
    )

    return jsonify({
        "results": places,
        "map_url": embed_map_url,
        "query": search_text
    })
@app.route('/profile')
def profile():
    return render_template('profile.html')
# Save profile to same Firebase realtime DB used by user registration
@app.route('/api/save_profile', methods=['POST'])
def save_profile():
    if 'uid' not in session:
        return jsonify({"error": "Not logged in"}), 401

    uid = session['uid']
    data = request.get_json() or {}

    # Add server-side timestamp for consistency
    data['updatedAt'] = data.get('updatedAt') or datetime.utcnow().isoformat()  # import datetime at top if needed

    try:
        db.child("user_profiles").child(uid).set(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("PROFILE SAVE ERROR:", e)
        return jsonify({"status": "error", "details": str(e)}), 500


# Load profile for current user
@app.route('/api/get_profile', methods=['GET'])
def get_profile():
    if 'uid' not in session:
        return jsonify({"error": "Not logged in"}), 401

    uid = session['uid']
    try:
        resp = db.child("user_profiles").child(uid).get()
        val = resp.val()
        if val:
            return jsonify({"status": "success", "data": val}), 200
        else:
            return jsonify({"status": "empty", "data": None}), 200
    except Exception as e:
        print("PROFILE LOAD ERROR:", e)
        return jsonify({"status": "error", "details": str(e)}), 500
@app.route('/organ')
def organ_database():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "user":
        return redirect(url_for("dashboard"))  # or error page

    return render_template('organ.html')
# -------------------------------
# SIMPLE HELPER: get hospital UID safely
# -------------------------------
def get_hospital_uid():
    uid = session.get("uid")
    role = session.get("role")

    if not uid or role != "hospital":
        raise Exception("Unauthorized")

    return uid
def get_hospital_uid():
    uid = session.get("uid")
    role = session.get("role")

    if not uid or role != "hospital":
        raise Exception("Unauthorized")

    return uid

@app.route("/api/save_organ", methods=["POST"])
def api_save_organ():
    try:
        uid = get_hospital_uid()
    except:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    payload = request.get_json() or {}
    hospital_name = payload.get("hospitalName", "")
    organs = payload.get("organs", [])
    if not hospital_name or not organs:
        return jsonify({"status": "error", "message": "hospitalName and organs required"}), 400
    record = {
        "hospitalUid": uid,
        "hospitalName": hospital_name,
        "address": payload.get("address", ""),
        "organs": organs,
        "blood": payload.get("blood", ""),
        "urgency": payload.get("urgency", ""),
        "smoking": payload.get("smoking", ""),
        "drinking": payload.get("drinking", ""),
        "chronic": payload.get("chronic", ""),
        "ageGroup": payload.get("ageGroup", ""),
        "createdAt": int(time.time())
    }
    try:
        ref = db_organ.child("organs").child(uid).push(record)
        return jsonify({"status": "success", "id": ref["name"]}), 200
    except Exception:
        app.logger.exception("SAVE ORGAN ERROR")
        return jsonify({"status": "error", "message": "Failed to save"}), 500

@app.route("/api/get_organs")
def api_get_organs():
    organ = (request.args.get("organ") or "").strip().lower()
    blood = (request.args.get("blood") or "").strip().upper()
    if not organ or not blood:
        return jsonify({"status": "error", "message": "organ and blood params required"}), 400
    try:
        hospitals = db_organ.child("organs").get().val() or {}
    except Exception:
        app.logger.exception("GET ORGANS FETCH ERROR")
        return jsonify({"status": "error", "message": "Failed to read DB"}), 500
    results = []
    for hosp_uid, hosp_block in hospitals.items():
        if not isinstance(hosp_block, dict):
            continue
        for organ_id, entry in hosp_block.items():
            if not isinstance(entry, dict):
                continue
            entry_organs = [o.lower() for o in entry.get("organs", [])]
            entry_blood = entry.get("blood", "").upper()
            if organ in entry_organs and entry_blood == blood:
                results.append({
                    "hospitalUid": hosp_uid,
                    "hospitalName": entry.get("hospitalName", ""),
                    "address": entry.get("address", ""),
                    "organs": entry.get("organs", []),
                    "blood": entry.get("blood", ""),
                    "urgency": entry.get("urgency", ""),
                    "smoking": entry.get("smoking", ""),
                    "drinking": entry.get("drinking", ""),
                    "chronic": entry.get("chronic", ""),
                    "ageGroup": entry.get("ageGroup", ""),
                    "createdAt": entry.get("createdAt", ""),
                    "recordId": organ_id
                })
    return jsonify({"organ_results": results})
# Hospital organ entry page (render h_organs.html)
@app.route("/h_organs")
def h_organs():
    # require hospital login like other hospital pages
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if session.get("role") != "hospital":
        return "Access denied: User cannot open hospital organ panel", 403
    return render_template("h_organs.html")
@app.route('/ambulance')
def ambulance():
    return render_template('amb.html')
  
@app.route('/horgan')
def horgan():
    return render_template('h_organs.html')
@app.route('/drug-inventory')
def drugi():
    return render_template('drug-inventory.html')
# -------------------------------------------
# DRUG INVENTORY (HOSPITAL FIREBASE)
# -------------------------------------------
# -------------------------------------------
# HELPERS FOR HOSPITAL AUTHENTICATION
# -------------------------------------------
def refresh_hospital_token():
    if 'idToken' not in session or 'refreshToken' not in session:
        return None

    try:
        refreshed = auth_hospital.refresh(session['refreshToken'])
        session['idToken'] = refreshed['idToken']
        return refreshed['idToken']
    except Exception as e:
        print("TOKEN REFRESH ERROR:", e)
        return None

def hospital_auth():
    uid = session.get("uid")
    token = session.get("idToken")

    if not uid or not token:
        return None, None

    # auto refresh
    new_token = refresh_hospital_token()
    if new_token:
        token = new_token

    return uid, token




# -------------------------------------------
# DRUG INVENTORY (HOSPITAL FIREBASE)
# -------------------------------------------

@app.route('/api/hospital/drugs/add', methods=['POST'])
def add_drug():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}

    try:
        ref = db_hospital.child("hospital_drugs").child(uid).push(data, token)
        return jsonify({"status": "success", "id": ref['name']}), 200
    except Exception as e:
        print("ERROR ADDING DRUG:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/hospital/drugs/get', methods=['GET'])
def get_drugs():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    try:
        result = db_hospital.child("hospital_drugs").child(uid).get(token).val()
        return jsonify({"status": "success", "data": result or {}}), 200
    except Exception as e:
        print("ERROR FETCHING DRUGS:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/hospital/drugs/update/<drug_id>', methods=['POST'])
def update_drug(drug_id):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}

    try:
        db_hospital.child("hospital_drugs").child(uid).child(drug_id).update(data, token)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("ERROR UPDATING DRUG:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/hospital/drugs/delete/<drug_id>', methods=['DELETE'])
def delete_drug(drug_id):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    try:
        db_hospital.child("hospital_drugs").child(uid).child(drug_id).remove(token)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("ERROR DELETING DRUG:", e)
        return jsonify({"error": str(e)}), 500
@app.route('/nurse')
def nurse():
    return render_template('nurse.html')
@app.route('/api/hospital/nurse/add', methods=['POST'])
def add_nurse():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    try:
        ref = db_hospital.child("hospital_nurse_system").child(uid).child("nurses").push(data, token)
        return jsonify({"status": "success", "id": ref['name']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/hospital/nurse/get', methods=['GET'])
def get_nurses():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    try:
        data = db_hospital.child("hospital_nurse_system").child(uid).child("nurses").get(token).val()
        return jsonify({"status": "success", "data": data or {} }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/hospital/nurse/update/<nid>', methods=['POST'])
def update_nurse(nid):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    try:
        data = request.get_json()
        db_hospital.child("hospital_nurse_system").child(uid).child("nurses").child(nid).update(data, token)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/hospital/nurse/delete/<nid>', methods=['DELETE'])
def delete_nurse(nid):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error": "Not logged in"}), 401

    try:
        db_hospital.child("hospital_nurse_system").child(uid).child("nurses").child(nid).remove(token)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/hospital/med/add', methods=['POST'])
def add_med():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    data = request.get_json()
    try:
        ref = db_hospital.child("hospital_nurse_system").child(uid).child("medicines").push(data, token)
        return jsonify({"status":"success","id":ref['name']}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
@app.route('/api/hospital/med/get', methods=['GET'])
def get_meds():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    try:
        data = db_hospital.child("hospital_nurse_system").child(uid).child("medicines").get(token).val()
        return jsonify({"status":"success","data":data or {} }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
@app.route('/api/hospital/med/update/<mid>', methods=['POST'])
def update_med(mid):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    data = request.get_json()
    try:
        db_hospital.child("hospital_nurse_system").child(uid).child("medicines").child(mid).update(data, token)
        return jsonify({"status":"success"}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
@app.route('/api/hospital/med/delete/<mid>', methods=['DELETE'])
def delete_med(mid):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    try:
        db_hospital.child("hospital_nurse_system").child(uid).child("medicines").child(mid).remove(token)
        return jsonify({"status":"success"}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
@app.route('/api/hospital/activity/add', methods=['POST'])
def add_activity():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    data = request.get_json()
    try:
        db_hospital.child("hospital_nurse_system").child(uid).child("activity_log").push(data, token)
        return jsonify({"status":"success"}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
@app.route('/api/hospital/activity/get', methods=['GET'])
def get_activity():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    try:
        data = db_hospital.child("hospital_nurse_system").child(uid).child("activity_log").get(token).val()
        return jsonify({"status":"success","data":data or {} }), 200
    except Exception as e:
        print("ACTIVITY GET ERROR:", e)
        return jsonify({"error":str(e)}), 500


@app.route('/api/hospital/vitals/add/<patient>', methods=['POST'])
def add_vitals(patient):
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    data = request.get_json()
    try:
        db_hospital.child("hospital_nurse_system").child(uid).child("vitals").child(patient).push(data, token)
        return jsonify({"status":"success"}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
@app.route('/api/hospital/vitals/get', methods=['GET'])
def get_vitals():
    uid, token = hospital_auth()
    if not uid:
        return jsonify({"error":"Not logged in"}), 401

    try:
        data = db_hospital.child("hospital_nurse_system").child(uid).child("vitals").get(token).val()
        return jsonify({"status":"success","data":data or {} }), 200
    except Exception as e:
        print("VITALS GET ERROR:", e)
        return jsonify({"error":str(e)}), 500
@app.route('/appointment')
def appointment():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "user":
        return redirect(url_for("dashboard"))

    return render_template("appointments.html", user_uid=session["uid"])



@app.route("/h_blood")
def hblood():
    # require hospital login same as other hospital pages
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if session.get("role") != "hospital":
        return "Access denied: Only hospitals can open this page", 403
    return render_template("h_blood.html", hospital_uid=session.get("hospital_uid", ""))
@app.route("/api/save_blood", methods=["POST"])
def api_save_blood():
    try:
        uid = get_hospital_uid()
    except Exception:
        return jsonify({"status":"error","message":"Unauthorized"}), 403

    payload = request.get_json() or {}
    hospital_name = payload.get("hospitalName","")
    address = payload.get("address","")
    blood_type = payload.get("bloodType","")
    component = payload.get("component","")
    quantity = payload.get("quantity")
    mapQuery = payload.get("mapQuery","")
    phone = payload.get("phone","")
    created_at = int(time.time())

    if not hospital_name or not blood_type or not component or not quantity:
        return jsonify({"status":"error","message":"hospitalName, bloodType, component and quantity required"}), 400

    record = {
        "hospitalUid": uid,
        "hospitalName": hospital_name,
        "address": address,
        "mapQuery": mapQuery,
        "phone": phone,
        "bloodType": blood_type,
        "component": component,
        "quantity": quantity,
        "createdAt": created_at
    }

    try:
        ref = db_blood.child("blood").child(uid).push(record)
        return jsonify({"status":"success","id": ref["name"]}), 200
    except Exception as e:
        app.logger.exception("SAVE BLOOD ERROR")
        return jsonify({"status":"error","message":"Failed to save"}), 500


# Get blood inventory across hospitals (filter by blood type)
# Example: GET /api/get_blood?blood=A%2B
@app.route("/api/get_blood")
def api_get_blood():
    blood = (request.args.get("blood") or "").strip().upper()
    if not blood:
        return jsonify({"status":"error","message":"blood param required"}), 400

    try:
        snapshot = db_blood.child("blood").get().val() or {}
    except Exception as e:
        app.logger.exception("GET BLOOD FETCH ERROR")
        return jsonify({"status":"error","message":"Failed to read DB"}), 500

    results = []
    # snapshot structure: blood -> <hospital_uid> -> <auto_id> -> record
    for hosp_uid, hosp_block in snapshot.items():
        if not isinstance(hosp_block, dict):
            continue
        for rec_id, entry in hosp_block.items():
            if not isinstance(entry, dict):
                continue
            entry_blood = (entry.get("bloodType","") or "").upper()
            if entry_blood == blood:
                results.append({
                    "hospitalUid": hosp_uid,
                    "recordId": rec_id,
                    "hospitalName": entry.get("hospitalName",""),
                    "address": entry.get("address",""),
                    "mapQuery": entry.get("mapQuery",""),
                    "phone": entry.get("phone",""),
                    "bloodType": entry.get("bloodType",""),
                    "component": entry.get("component",""),
                    "quantity": entry.get("quantity",0),
                    "createdAt": entry.get("createdAt","")
                })
    return jsonify({"blood_results": results})
@app.route("/api/get_blood_by_hospital")
def api_get_blood_by_hospital():
    """
    Returns all blood records stored under /blood/<hospital_uid>.
    If hospitalUid query param provided, use that; otherwise require logged hospital.
    """
    hospital_uid = request.args.get("hospitalUid")
    if not hospital_uid:
        # require logged-in hospital if not provided
        try:
            hospital_uid = get_hospital_uid()
        except Exception:
            return jsonify({"status":"error","message":"hospitalUid required or login required"}), 403

    try:
        snapshot = db_blood.child("blood").child(hospital_uid).get().val() or {}
    except Exception:
        app.logger.exception("GET BLOOD BY HOSPITAL ERROR")
        return jsonify({"status":"error","message":"Failed to read DB"}), 500

    results = []
    for rec_id, entry in snapshot.items():
        if not isinstance(entry, dict):
            continue
        results.append({
            "recordId": rec_id,
            "hospitalUid": hospital_uid,
            "hospitalName": entry.get("hospitalName",""),
            "address": entry.get("address",""),
            "mapQuery": entry.get("mapQuery",""),
            "phone": entry.get("phone",""),
            "bloodType": entry.get("bloodType",""),
            "component": entry.get("component",""),
            "quantity": entry.get("quantity",0),
            "createdAt": entry.get("createdAt","")
        })
    return jsonify({"blood_results": results})
@app.route("/api/get_organs_by_hospital")
def api_get_organs_by_hospital():
    """
    Return all saved organ entries for the logged-in hospital.
    """
    try:
        uid = get_hospital_uid()
    except:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        snapshot = db_organ.child("organs").child(uid).get().val() or {}
    except Exception:
        app.logger.exception("GET ORGANS BY HOSPITAL ERROR")
        return jsonify({"status": "error", "message": "Failed to read DB"}), 500

    results = []
    for rec_id, entry in snapshot.items():
        if not isinstance(entry, dict):
            continue
        results.append({
            "recordId": rec_id,
            "hospitalUid": uid,
            "hospitalName": entry.get("hospitalName",""),
            "address": entry.get("address",""),
            "organs": entry.get("organs", []),
            "blood": entry.get("blood",""),
            "urgency": entry.get("urgency",""),
            "smoking": entry.get("smoking",""),
            "drinking": entry.get("drinking",""),
            "chronic": entry.get("chronic",""),
            "ageGroup": entry.get("ageGroup",""),
            "createdAt": entry.get("createdAt","")
        })
    return jsonify({"organ_results": results})

@app.route('/happointment')
def happointment():
    if not session.get("logged_in"):
        return redirect(url_for("h_login"))

    if session.get("role") != "hospital":
        return redirect(url_for("h_dashboard"))

    return render_template("happointments.html", hospital_uid=session["uid"])


# -----------------------------------------
# USER APPOINTMENTS API
# -----------------------------------------

@app.route("/api/user/appointments/get")
def api_user_appt_get():
    if not session.get("logged_in") or session.get("role") != "user":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session.get("uid")
    data = db_user_appointments.child("user_appointments").child(uid).get().val() or {}
    return jsonify({"status": "success", "data": data})


@app.route("/api/user/appointments/add", methods=["POST"])
def api_user_appt_add():
    if not session.get("logged_in") or session.get("role") != "user":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session.get("uid")
    payload = request.get_json() or {}

    ref = db_user_appointments.child("user_appointments").child(uid).push(payload)
    return jsonify({"status": "success", "id": ref["name"]})



@app.route("/api/user/appointments/delete/<appt_id>", methods=["DELETE"])
def api_user_appt_delete(appt_id):
    if not session.get("logged_in") or session.get("role") != "user":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session.get("uid")
    db_user_appointments.child("user_appointments").child(uid).child(appt_id).remove()
    return jsonify({"status": "success"})

# -----------------------------------------
# HOSPITAL APPOINTMENTS API
# -----------------------------------------

# -----------------------------------------
# HOSPITAL APPOINTMENTS API  (FINAL + FIXED)
# -----------------------------------------

@app.route("/api/hospital/appointments/get")
def api_hosp_appt_get():
    hosp_uid = request.args.get("hospitalUid")

    if hosp_uid:
        data = db_appointment.child("hospital_appointments").child(hosp_uid).get().val() or {}
        return jsonify({"status": "success", "data": data})

    if not session.get("logged_in") or session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session["uid"]
    data = db_appointment.child("hospital_appointments").child(uid).get().val() or {}
    return jsonify({"status": "success", "data": data})



@app.route("/api/hospital/appointments/add", methods=["POST"])
def api_hosp_appt_add():
    if not session.get("logged_in") or session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session["uid"]
    payload = request.get_json() or {}

    ref = db_appointment.child("hospital_appointments").child(uid).push(payload)
    appt_id = ref["name"]

    return jsonify({"status": "success", "id": appt_id})


@app.route("/api/hospital/appointments/update/<appt_id>", methods=["POST"])
def api_hosp_appt_update(appt_id):
    if not session.get("logged_in") or session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session["uid"]
    payload = request.get_json() or {}

    db_appointment.child("hospital_appointments").child(uid).child(appt_id).update(payload)

    return jsonify({"status": "success"})


@app.route("/api/hospital/appointments/delete/<appt_id>", methods=["DELETE"])
def api_hosp_appt_delete(appt_id):
    if not session.get("logged_in") or session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized"}), 403

    uid = session["uid"]

    db_appointment.child("hospital_appointments").child(uid).child(appt_id).remove()

    return jsonify({"status": "success"})

@app.route("/api/hospitals/all")
def api_get_all_hospitals():
    try:
        data = db_hospital.child("hospitals").get().val() or {}
        results = []

        for uid, info in data.items():
            if isinstance(info, dict):
                info["hospitalUid"] = uid
                results.append(info)

        return jsonify({"status": "success", "hospitals": results})
    except Exception as e:
        print("ERROR FETCHING ALL HOSPITALS:", e)
        return jsonify({"status": "error", "message": str(e)}), 500




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
