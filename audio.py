import random
import speech_recognition as sr         #to recognise speech
import webbrowser        #to open webbrowser
import time     #to get time
from time import ctime
import playsound   #to play sound
import os      #to remove files
from gtts import gTTS     #text to speech conversion
import bs4 as bs
import pyttsx3
import subprocess
import urllib.request


def speak (text):
    text = str(text)
    engine.say(text)
    engine.setProperty('rate',500)
    engine.runAndWait()


r = sr.Recognizer()
def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
           voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
           speak('Sorry, could not hear that')
        except sr.RequestError:
           speak("Sorry, my speech service is down")
        return voice_data

def speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text = audio_string, lang='en')
    r= random.randint(1,100000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond (voice_data):

    if 'what is your name' in voice_data:
        speak('My name is windows commander')
    if 'what time is it' in voice_data:
        speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'http://google.com/search?q=' + search
        webbrowser.get().open(url)
        speak('Here is what I found for ' + search)
    if 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'http://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speak('Here is the location of ' + location)
    if 'find weather information' in voice_data:
        weather = record_audio('which country whether')
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        speak('Here what I found for weather' + weather)
    if 'find definition of' in voice_data:
        definition = record_audio('What do you need definition of?')
        url = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + definition)
        soup = bs.BeautifulSoup(url, 'lxml')
        definitions = []
        for paragraph in soup.find_all('p'):
            definitions.append(str(paragraph.text))
        if definitions:
            if definitions[0]:
                speak('I am sorry I could not find that definition, please try a web search')
            elif definitions[1]:
                speak('here is what I found ' + definitions[1])
            else:
                speak('Here is what I found ' + definitions[2])
        else:
            speak("I am sorry I could not find the definition for " + definition)

    if 'exit' in voice_data:
        speak('bye')
        exit()


time.sleep(1)

engine = pyttsx3.init()
speak('How can I help you:')
while 1:
    voice_data = record_audio()
    respond(voice_data)



