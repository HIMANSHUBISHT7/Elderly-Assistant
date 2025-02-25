from flask import Flask, request, jsonify, render_template
import pyttsx3
import threading
import time
from datetime import datetime, timedelta
import webbrowser
import re
from plyer import notification

app = Flask(__name__)
engine = pyttsx3.init()

# Medication Schedule (Dynamic)
medication_schedule = {
    "08:00": "morning medicine",
    "17:20": "afternoon medicine",
    "20:00": "night medicine"
}

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def update_medication_schedule(time, name):
    """Dynamically update the medication schedule."""
    medication_schedule[time] = name
    return f" Medication reminder set for {time}: {name}"

def remove_medication_schedule(time):
    """Remove a medication reminder."""
    if time in medication_schedule:
        del medication_schedule[time]
        return f" Removed medication reminder for {time}"
    return " No reminder found for this time."

def medication_reminder():
    """Check and remind for medication at a fixed schedule with pop-ups and chatbot response."""
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M')

            for med_time, med_name in list(medication_schedule.items()):
                # Exact time reminder
                if current_time == med_time:
                    reminder = f"🚨 It's time to take your {med_name}!"
                    print(reminder)
                    speak(reminder)
                    notification.notify(
                        title="Medication Reminder",
                        message=reminder,
                        timeout=10
                    )
                    time.sleep(60)  # Prevent multiple notifications within the same minute

                # One-hour prior reminder
                hour_before = (datetime.strptime(med_time, "%H:%M") - timedelta(hours=1)).strftime("%H:%M")
                if current_time == hour_before:
                    early_reminder = f"🔔 Reminder: Your {med_name} is due in one hour."
                    print(early_reminder)
                    notification.notify(
                        title="Upcoming Medication Reminder",
                        message=early_reminder,
                        timeout=10
                    )
                    time.sleep(60)  # Prevent multiple notifications within the same minute

            time.sleep(10)  # Prevent excessive CPU usage
        except Exception as e:
            print(f" Error in reminder thread: {e}")
            time.sleep(10)


# Website shortcuts
website_database = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "github": "https://www.github.com",
    "hk vitals": "https://www.hkvitals.com/",
    "disease diagnosis": "http://localhost:8501/"
}

# Open websites
def open_website(command):
    """Opens a website based on the command."""
    for site in website_database:
        if site in command:
            webbrowser.open(website_database[site])
            return f"Opening {site}..."
    return "I couldn't find the website. Please try again."

# Extract disease from user input
def extract_disease(command):
    """Extracts the disease from various sentence structures."""
    patterns = [
        r"i have (a |an )?(?P<disease>\w+)", 
        r"i am suffering from (?P<disease>\w+)",
        r"i got (a |an )?(?P<disease>\w+)",
        r"i feel like i have (a |an )?(?P<disease>\w+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            return match.group("disease")
    
    return None

# Medicine recommendation function
def recommend_medicine(disease):
    medicine_database = {
        "cold": ["Paracetamol", "Cough Syrup", "Antihistamines"],
        "fever": ["Ibuprofen", "Paracetamol", "Acetaminophen"],
        "diabetes": ["Metformin", "Insulin", "Glipizide"],
        "hypertension": ["Amlodipine", "Lisinopril", "Losartan"],
        "headache": ["Aspirin", "Ibuprofen", "Paracetamol"],
        "stomach pain": ["Omeprazole", "Ranitidine", "Antacids"]
    }
    
    disease = disease.lower().strip()
    if disease in medicine_database:
        medicines = ", ".join(medicine_database[disease])
        return f"For {disease}, you can take: {medicines}. However, consult a doctor before taking any medication."
    else:
        return "I'm not sure about that disease. Please consult a doctor."

# Response function
def respond_to_command(command):
    """Processes user commands and returns a response."""
    command = command.lower()
    
    if "hello" in command or "hi" in command:
        return "Hello! How can I assist you today?"
    elif "time" in command:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    elif "date" in command:
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."
    elif "weather" in command:
        return "I'm sorry, I can't fetch the weather yet."
    elif "emergency" in command or "help" in command:
        send_emergency_alert()
        return "Emergency alert activated! Contacting your caregiver."
    elif "how are you" in command or "talk to me" in command:
        return "I'm here to assist you! How can I help today?"
    elif "exit" in command or "stop" in command:
        return "Goodbye! Stay safe."
    elif "open" in command or "go to" in command or "launch" in command:
        return open_website(command)
    elif "joke" in command:
        return "Why don't scientists trust atoms? Because they make up everything!"
    elif "motivate me" in command or "give me motivation" in command:
        return "Believe in yourself! Every great achievement started with the decision to try."
    elif "who made you" in command or "who created you" in command:
        return "I was created by a skilled developer with a vision for smart AI assistance!"
    elif "your name" in command or "who are you" in command:
        return "I'm your AI assistant, here to help with anything you need."
    elif "tell me a fact" in command:
        return "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still perfectly edible!"
    elif "shutdown" in command or "power off" in command:
        return "Shutting down... Just kidding! I can't do that yet."
    elif "sing a song" in command:
        return "I'm not the best singer, but here's a classic: 🎵 Twinkle, twinkle, little star... 🎵"
    elif "define" in command:
        return "Please specify the word you want me to define."
    elif "tell me a story" in command:
        return "Once upon a time, a coder built a smart AI assistant. And that assistant is me!"
    elif "calculate" in command:
        return "I can help with basic calculations. Please specify the numbers."
    elif "where am i" in command:
        return "I'm not sure, but you can check your location using Google Maps."
    elif "translate" in command:
        return "I can help with translations. Please specify the language and phrase."
    elif "good morning" in command:
        return "Good morning! Hope you have a fantastic day ahead."
    elif "good night" in command:
        return "Good night! Sleep well and recharge for a great tomorrow."
    elif "i am bored" in command:
        return "Let’s play a quick game! How about a riddle? What has to be broken before you can use it? (Hint: It's something in your kitchen.)"
    
    # Handle medical queries
    disease = extract_disease(command)
    if disease:
        return recommend_medicine(disease)

    return "I'm not sure how to respond to that, but I'm here to help."
# Emergency alert function
def send_emergency_alert():
    print("Sending emergency alert to caregivers...")
    speak("Emergency alert sent! Help is on the way.")

# Web routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
        data = request.get_json()
        user_input = data.get("text", "").strip()

        if not user_input:
            return jsonify({"response": "I couldn't understand. Please try again."})

        print(f"User said: {user_input}")
        response = respond_to_command(user_input)

        return jsonify({"response": response})

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"response": "An unexpected error occurred. Please try again."})

if __name__ == '__main__':
    reminder_thread = threading.Thread(target=medication_reminder, daemon=True)
    reminder_thread.start()
    app.run(debug=True)