import speech_recognition as sr
import pyttsx3
import pyjokes
import pywhatkit
import wikipedia
import webbrowser
import datetime
import time
import pyautogui as pyg
from tqdm import tqdm
import mysql.connector as mlt
from pwinput import pwinput
from ecapture import ecapture as ec

# MYSQL DATABASE CONNECTION
mydb = mlt.connect(
    host="localhost",
    user="root",
    passwd="vinay988",
    database="vinaydb1"
)

cur = mydb.cursor()
cur.execute("SELECT * from vinaydb1.details;")
enroll_no, name, user_id, passwrd = [], [], [], []


# INSERTING DATA INTO LISTS
def data():
    for cursor_elements in cur:
        enroll_no.append(cursor_elements[0])
        name.append(cursor_elements[1])
        user_id.append(cursor_elements[2])
        passwrd.append(cursor_elements[3])


# Voice / Language Options
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# hear the microphone and return the audio as text
def transform_audio_into_text():
    # store recognizer in a variable
    r = sr.Recognizer()

    # set microphone
    with sr.Microphone() as source:
        # adjusting noise cancellation
        r.adjust_for_ambient_noise(source)
        # waiting time
        r.pause_threshold = 0.8
        # report that recording has begun
        print("You can now speak")

        # save what you hear as audio
        audio = r.listen(source)

        try:
            # search on google
            request = r.recognize_google(audio, language="en-in")
            # test in text
            print("You said " + request)

            # return request
            return request

        # In case it doesn't understand audio
        except sr.UnknownValueError:

            # show proof that it didn't understand audio
            print("Oops! I didn't understand audio")

            # return error
            return "I am still waiting"

        # In case the request cannot be resolved
        except sr.RequestError:

            # show proof that it didn't understand audio
            print("Oops! There is no service")

            # return error
            return "I am still waiting"
        # In case of Unexpected Error
        except:

            # show proof that it didn't understand audio
            print("Oops! Something went wrong")

            # return error
            return "I am still waiting"


# Function so that the assistant can be heard
def speak(message):
    # start engine of pyttsx3
    engine = pyttsx3.init()
    # setProperty used to select a particular voice
    engine.setProperty('voice', id2)

    # deliver message
    engine.say(message)
    # runAndWait() will make the speech audible in the system
    engine.runAndWait()


# Inform day of the week
def ask_day():
    # Create a variable with today information
    day = datetime.date.today()
    print(day)

    # Create variable for day of the week
    week_day = day.weekday()
    print(week_day)

    # Names of days
    seven_days = {0: 'Monday',
                  1: 'Tuesday',
                  2: 'Wednesday',
                  3: 'Thursday',
                  4: 'Friday',
                  5: 'Saturday',
                  6: 'Sunday'}

    # Say the day of the week
    speak(f"Today is {seven_days[week_day]}")


# Inform what time it is
def ask_time():
    # Variable with time information
    time = datetime.datetime.now()
    time = f'At this moment it is {time.hour} hours and  {time.minute} minutes'
    print(time)

    # Say the time
    speak(time)


# Create initial greeting
def initial_greeting():
    # Say Greeting
    speak('Hello I am Stella. How can I help you?')


# Main Function of the Assistant
def my_assistant():
    # Activate Initial Greeting
    initial_greeting()

    # Cut-off variable
    go_on = True

    # Main Loop
    while go_on:

        # Activate microphone and save request
        my_request = transform_audio_into_text().lower()

        if 'open youtube' in my_request:
            speak('Sure')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'open browser' in my_request:
            speak('Of course, I am on it')
            webbrowser.open('https://www.google.com')
            continue
        elif 'what day is today' in my_request:
            ask_day()
            continue
        elif 'what is the time' in my_request:
            ask_time()
            continue
        elif 'do a wikipedia search for' in my_request:
            speak('I am looking for it')
            my_request = my_request.replace('do a wikipedia search for', '')
            answer = wikipedia.summary(my_request, sentences=1)
            speak('according to wikipedia: ')
            speak(answer)
            continue
        elif 'search the internet for' in my_request:
            speak('of course, right now')
            my_request = my_request.replace('search the internet for', '')
            pywhatkit.search(my_request)
            speak('this is what i found')
            continue
        elif 'play' in my_request:
            speak('oh, what a great idea! I will play it right now')
            pywhatkit.playonyt(my_request)
            continue
        elif 'joke' in my_request:
            speak(pyjokes.get_joke())
            continue
        elif "camera" in my_request or "take a picture" in my_request:
            ec.capture(0, "frame", "frame.png")
        elif 'goodbye' in my_request:
            speak('I am going to rest. Let me know if you need anything')
            break
my_assistant()
