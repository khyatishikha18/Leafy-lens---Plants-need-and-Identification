# 🌿 Leafy Lens – AI Powered Plant Identification and Plant Need Recommendation System

Leafy Lens is an AI-powered web application that identifies plants from leaf images and provides detailed plant care recommendations. The system helps users understand their plants by offering information such as water requirements, sunlight needs, soil type, temperature, health status, disease information, treatment suggestions, and care tips.

---
🚀 Features

- 🔐 User Registration and Login
- 🌿 Plant Identification using PlantNet API
- 📷 Leaf Image Upload with Preview
- 💧 Water Requirement Recommendation
- ☀️ Sunlight Recommendation
- 🌱 Soil Type Suggestion
- 🌡️ Temperature Recommendation
- ❤️ Plant Health Information
- 🦠 Disease Information
- 💊 Treatment Suggestions
- 🌿 Plant Care Tips
- 📱 Responsive User Interface

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite

### APIs
- PlantNet API (Plant Identification)
- Hugging Face API (AI-based Plant Information)

---

## 📂 Project Structure

```text
LeafyLens/
│── static/
│   ├── css/
│   ├── images/
│   └── uploads/
│
│── templates/
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── detect.html
│   └── result.html
│
│── app.py
│── database.db
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/Leafy-Lens.git
```

2. Open the project folder

```bash
cd Leafy-Lens
```

3. Install required packages

```bash
pip install -r requirements.txt
```

4. Add your PlantNet API Key and Hugging Face API Key in `app.py`.

5. Run the application

```bash
python app.py
```

6. Open your browser and visit

```
http://127.0.0.1:5000
```

---

## 🖼️ Application Workflow

1. Register/Login
2. Upload a plant leaf image
3. PlantNet API identifies the plant
4. AI generates plant care information
5. The result page displays:
   - Plant Name
   - Scientific Name
   - Confidence Score
   - Water Requirement
   - Sunlight Requirement
   - Soil Type
   - Temperature
   - Health Status
   - Disease Information
   - Treatment
   - Care Tips

---

## 🎯 Future Enhancements

- Mobile Application
- Offline Plant Identification
- Multi-language Support
- Weather-based Plant Recommendations
- Personalized Plant Care Reminder System

---

## 👩‍💻 Developer

**Khyati Shikha**

B.Tech (Computer Science & Engineering)

Bengal College of Engineering and Technology

MAKAUT University

---

## 📄 License

This project is developed for educational and academic purposes.


