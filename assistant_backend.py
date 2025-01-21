import pyttsx3
import speech_recognition as sr
import datetime
import pyautogui
import webbrowser
import os
import psutil
import requests
import wikipedia
import wolframalpha
import pyjokes
from pyowm import OWM

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Function to speak to the user
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input from the user
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        
        # Listen for audio input from the user
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()  # Convert to lowercase for consistency
        print(f"User said: {command}")
    
    except sr.UnknownValueError:
        # In case the assistant doesn't understand the speech
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that. Please repeat your command.")
        return None  # Return None to indicate no command was recognized
    
    except sr.RequestError:
        # In case there's a problem with the speech recognition service
        print("Sorry, the service is down.")
        speak("Sorry, the service is down. Please check your internet connection.")
        return None
    
    return command

# Get current weather using OpenWeatherMap
def get_weather(city):
    api_key = "3a0c4a1f2b2832d3d9184308a912bc8b"
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    temp = weather.temperature('celsius')["temp"]
    status = weather.detailed_status
    return temp, status

# Get the CPU and RAM usage
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

# Perform advanced actions based on commands
def perform_action(command):
    if 'hello' in command:
        speak("Hello, how can I assist you?")
    
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    
    elif 'play music' in command:
        music_path = "C:/Users/YourUsername/Music/"
        os.startfile(music_path)
        speak("Playing music.")
    
    elif 'screenshot' in command:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        speak("Screenshot taken.")
    
    elif 'tell me a joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
    
    elif 'weather' in command:
        speak("Which city's weather would you like to know?")
        city = take_command()
        if city:
            temp, status = get_weather(city)
            speak(f"The temperature in {city} is {temp}°C with {status}.")
    
    elif 'news' in command:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=580dc75860ed47459e8161e87ecf6428"
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
        for article in articles[:5]:
            speak(f"Headline: {article['title']}.")
    
    elif 'system info' in command:
        cpu_usage, ram_usage = get_system_info()
        speak(f"Your CPU usage is {cpu_usage}% and RAM usage is {ram_usage}%.")
    
    elif 'calculate' in command:
        client = wolframalpha.Client("QV2EH4-HEY4RU53R5")
        query = command.replace('calculate', '')
        res = client.query(query)
        answer = next(res.results).text
        speak(f"The answer is {answer}.")
    
    elif 'wikipedia' in command:
        speak("What do you want to know?")
        query = take_command()
        if query:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {result}")
    
    elif 'quit' in command:
        speak("Goodbye!")
        exit()

# Main function to run the assistant
def run_assistant():
    speak("Hello, I am your advanced desktop assistant. How can I help you today?")
    
    while True:
        command = take_command()
        
        if command:
            perform_action(command)

# Run the assistant
run_assistant()
