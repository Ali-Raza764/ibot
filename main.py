import pyttsx3
from groq import Groq
import speech_recognition as sr
# from gtts import gTTS
# import pygame
# import random
# import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 190)
client = Groq(api_key="put your key here")
# pygame.mixer.init()


# Function to convert speech to text
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise and listen for input
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        recognizer.energy_threshold = 400
        try:
            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak("Sorry I did not understand what you said")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

# def text_to_speech(text, language="en", output_file='output.mp3'):
#     random_number  = str(random.randint(1, 1000000000))
#     tts = gTTS(text=text, lang=language, slow=False)
#     tts.save(output_file+random_number)  
#     play_audio(output_file+random_number)
#     os.remove(output_file+random_number)

# def play_audio(audio_file):
#     pygame.mixer.music.load(audio_file)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

def get_response(text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=.7,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    return response

if __name__ == "__main__":
    speak("Hello, How can I help you?")
    while True:
        try:
            user_command = speech_to_text()
            
            # Check if user_command is None
            if user_command is None:
                continue  # Skip this iteration if no valid speech is detected

            print("Creating response for:", user_command)
            response = get_response( "Extra info for you before answering: the given text before this is a user_input to a robot called robot the robot is created by Ali Raza Khalid from Abbottabad and donot respond with anything like robot responds or robot thinks say I think ok "
            "and the robot will talk using pyttsx3 so keep the responses in less than one line and simple. "
            "The user command is: "
            + user_command)
            response_string = ""
            for chunk in response:
                response_string += chunk.choices[0].delta.content or ""
            text_without_quotes = response_string.replace('"', '').replace("`", "").replace("_", "")
            print(text_without_quotes)
            print("Generating audio")
            speak(text_without_quotes)
        except Exception as e:
            print("An error occurred", e)
