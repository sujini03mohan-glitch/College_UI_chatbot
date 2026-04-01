from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import json
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# LOAD DATASET
with open("dataset.json") as file:
    data = json.load(file)

questions = [item["question"] for item in data["data"]]
answers = [item["answer"] for item in data["data"]]

# PREPROCESS FUNCTION
def preprocess(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    return text.strip()

# CHAT ROUTE
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    user_input = preprocess(user_input)

    #KEYWORD-BASED RESPONSES

    keywords = {
    #  COURSES INFO
    "bsc": "B.Sc Computer Science includes programming, AI, and data science.",
    "bcom": "BCom focuses on finance, accounting and business studies.",
    "bca": "BCA focuses on software development and programming.",
    "mba": "MBA focuses on management, leadership and business strategies.",
    "phd": "PhD is a research-based doctoral program.",

    #  FEES
    "btech fees": "B.Tech fee is approximately ₹1.38 Lakhs.",
    "bsc fees": "B.Sc fees range depending on specialization, starting around ₹50,000.",
    "bcom fees": "BCom fees are approximately ₹50,000 to ₹1,00,000.",
    "mba fees": "MBA fees range from ₹1.37 Lakhs to ₹2.29 Lakhs.",
    "mca fees": "MCA fee is approximately ₹1.25 Lakhs.",
    "phd fees": "PhD fee is approximately ₹1.16 Lakhs.",

    #  COURSES LIST
    "courses": "We offer BCA, BSc Computer Science, BCom, BA English, MBA and more.",
    "available courses": "Available courses include BCA, BSc, BCom, BA, MBA and PG programs.",
    "bsc courses": "BSc includes Computer Science and other science streams.",
    "bcom courses": "BCom includes general, finance and accounting streams.",

    #  FACILITIES
    "hostel": "Yes, we provide separate hostel facilities for boys and girls.",
    "hostel facility": "Hostel facilities are available with good accommodation and security.",
    "wifi": "Campus-wide WiFi is available for all students.",
    "library": "We have a fully equipped digital library.",
    "lab": "Modern labs are available for practical learning.",

    #  DEPARTMENTS
    "departments": "We have departments like Computer Science, Commerce, Arts and Management.",
    "cs department": "Computer Science department focuses on programming, AI and data science.",
    "commerce department": "Commerce department focuses on finance and business.",
    "arts department": "Arts department focuses on language and humanities.",

    #  DURATION
    "duration": "Most undergraduate courses are 3 years and postgraduate courses are 2 years.",
    "course duration": "UG courses are 3 years and PG courses are typically 2 years.",
    "bca duration": "BCA is a 3-year degree program.",
    "mba duration": "MBA is a 2-year postgraduate program.",

    # ADMISSION
    "admission": "You can apply online through our website or visit the campus.",
    "apply": "Applications can be submitted online with required documents.",
    "eligibility": "Eligibility depends on the course and previous qualifications.",

    # PLACEMENT
    "placement": "We have a placement cell with top companies visiting every year.",
    "jobs": "Students get placement opportunities in IT and business sectors.",
}    

    # CHECK KEYWORDS FIRST
    for key in keywords:
        if key in user_input:
            return jsonify({"response": keywords[key]})

    # TF-IDF FALLBACK
    all_questions = questions + [user_input]

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(all_questions)

    similarity = cosine_similarity(tfidf[-1], tfidf[:-1])
    best_match = similarity.argmax()

    if similarity[0][best_match] > 0.15:
        response = answers[best_match]
    else:
        response = "Sorry, I didn't understand your question."

    return jsonify({"response": response})


# HOME ROUTE
@app.route("/")
def home():
    return render_template("index.html")


# EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'sujini.03.mohan@gmail.com'
app.config['MAIL_PASSWORD'] = 'tkfd djpt zyan brap'
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

# EMAIL ROUTE
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json

    msg = Message(
        subject="New Course Enquiry",
        sender=app.config['MAIL_USERNAME'],
        recipients=['sujini.03.mohan@gmail.com']
    )

    msg.body = f"""
New Enquiry:

Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
Course: {data['course']}
"""

    mail.send(msg)

    return jsonify({"message": "Enquiry sent successfully!"})


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)