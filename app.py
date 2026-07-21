from flask import Flask, render_template, request, redirect
import sqlite3
import os
import requests
import json
import traceback
import requests
PLANTNET_API_KEY = "YOUR_PLANTNET_API_KEY"

HF_API_KEY = "YOUR_HUGGINGFACE_API_KEY"

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)

# ==========================
# Upload Folder
# ==========================

UPLOAD_FOLDER="static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Login

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/leafy.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect("/home")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# ==========================
# Register
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/leafy.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            email TEXT,
            username TEXT,
            password TEXT
        )
        """)

        cursor.execute("""
        INSERT INTO users(fullname,email,username,password)
        VALUES(?,?,?,?)
        """, (fullname, email, username, password))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


# ==========================
# Home Page
# ==========================

@app.route("/home")
def home():
    return render_template("home.html")


# ==========================
# Disease Detection Page
# ==========================

@app.route("/detect")
def detect():
    return render_template("detect.html")


# ==========================
# AI Prediction
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    image = request.files["leaf"]

    if image.filename == "":
        return "Please upload a plant image."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(filepath)

    plant_name = "Unknown Plant"
    scientific_name = "Unknown"
    confidence = 0

    water = "Generating..."
    sunlight = "Generating..."
    soil = "Generating..."
    temperature = "Generating..."
    uses = "Generating..."
    health = "Generating..."
    disease = "Generating..."
    treatment = "Generating..."
    care_tips = "Generating..."

    url = (
        f"https://my-api.plantnet.org/v2/identify/all"
        f"?api-key={PLANTNET_API_KEY}"
    )

    try:

        with open(filepath, "rb") as img:

            files = {
                "images": img
            }

            data = {
                "organs": "leaf"
            }

            response = requests.post(
                url,
                files=files,
                data=data,
                timeout=30
            )

        if response.status_code != 200:
            return f"PlantNet Error : {response.text}"

        result = response.json()

        if not result.get("results"):
            return "Unable to identify plant."

        best = result["results"][0]

        confidence = round(best.get("score", 0) * 100, 2)

        species = best.get("species", {})

        scientific_name = species.get(
            "scientificNameWithoutAuthor",
            "Unknown"
        )

        common_names = species.get("commonNames", [])

        if common_names:
            plant_name = common_names[0]
        else:
            plant_name = scientific_name

    except Exception:

        traceback.print_exc()

        water = "Unable to generate"
        sunlight = "Unable to generate"
        soil = "Unable to generate"
        temperature = "Unable to generate"
        uses = "Unable to generate"
        health = "Unknown"
        disease = "Unknown"
        treatment = "Unknown"
        care_tips = "Try another image."
    # ==================================================
    # Generate AI Report using Hugging Face
    # ==================================================

    prompt = f"""
You are an expert botanist.

Plant Name: {plant_name}
Scientific Name: {scientific_name}

Return ONLY valid JSON.

{{
    "water":"",
    "sunlight":"",
    "soil":"",
    "temperature":"",
    "uses":"",
    "health":"",
    "disease":"",
    "treatment":"",
    "care_tips":""
}}
"""

    try:

        payload = {
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500,
            "temperature": 0.3
        }

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        text = result["choices"][0]["message"]["content"].strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        ai = json.loads(text)

        water = ai.get("water", "Not Available")
        sunlight = ai.get("sunlight", "Not Available")
        soil = ai.get("soil", "Not Available")
        temperature = ai.get("temperature", "Not Available")
        uses = ai.get("uses", "Not Available")
        health = ai.get("health", "Healthy")
        disease = ai.get("disease", "None")
        treatment = ai.get("treatment", "Not Available")
        care_tips = ai.get("care_tips", "Not Available")

    except Exception as e:

        print("HF Error:", e)

        water = "Not Available"
        sunlight = "Not Available"
        soil = "Not Available"
        temperature = "Not Available"
        uses = "Not Available"
        health = "Healthy"
        disease = "None"
        treatment = "Not Available"
        care_tips = "Not Available"

    # -----------------------------
    # Result Page
    # -----------------------------

    return render_template(

        "result.html",

        plant_name=plant_name,
        scientific_name=scientific_name,
        confidence=confidence,

        water=water,
        sunlight=sunlight,
        soil=soil,
        temperature=temperature,
        uses=uses,
        health=health,
        disease=disease,
        treatment=treatment,
        care_tips=care_tips,

        image=image.filename    
    )


@app.route("/profile")
def profile():
    return "<h2>Profile Page Coming Soon...</h2>"


@app.route("/logout")
def logout():
    return redirect("/")


@app.route("/loading")
def loading():
    return render_template("loading.html")

# ==========================
# Run Flask
# ==========================

if __name__ == "__main__":
    app.run(debug=True)