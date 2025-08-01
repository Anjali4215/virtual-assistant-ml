import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
import requests
import pickle

# Initialize speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"✅ You said: {command}")
        return command.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return ""

def predict_intent(command):
    model = pickle.load(open("models/trained_model.pkl", "rb"))
    vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
    X = vectorizer.transform([command])
    return model.predict(X)[0]

def perform_task(intent, command):
    if intent == "hello":
        speak("Hello! How can I assist you?")

    elif intent == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    elif intent == "date":
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    elif intent == "open_google":
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif intent == "open_youtube":
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif intent == "weather":
        speak("Please say the city name.")
        city = get_command()
        if not city: return
        api_key = "your_openweathermap_api_key"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"The weather in {city} is {weather} with temperature {temp}°C")
        else:
            speak("City not found.")

    elif intent == "send_email":
        try:
            speak("Who should I send the email to?")
            recipient = get_command()
            speak("What is the message?")
            message = get_command()
            sender = "your_email@gmail.com"
            password = "your_password"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, message)
            server.quit()
            speak("Email sent successfully.")
        except:
            speak("Sorry, I couldn't send the email.")
    elif intent == "general question":
        try:
            speak("let me search that for you")
            webbrowser.open(f"https://www.google.com/search?q={command}")
        except:
            speak("Sorry, I couldn't get it .")
    elif intent == "exit":
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("Sorry, I don't understand that yet.")

if __name__ == "__main__":
    speak("Virtual Assistant is ready.")
    while True:
        command = get_command()
        if command:
            intent = predict_intent(command)
            perform_task(intent, command)