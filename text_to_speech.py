import pyttsx3 # TTS module
from settings import speak_cards # Centralized settings panel


def narrate(text_to_speak, language_id):
            if speak_cards is True: # If setting is on, else don't speak anything
              if language_id == 'spanish' or language_id == 2:
                     language_id = 85
              else:
                     language_id = 16 # English voice
              engine = pyttsx3.init()
              voices = engine.getProperty('voices')
              engine.setProperty('voice', voices[language_id].id)
              engine.setProperty('rate', 175)
              engine.say(text_to_speak)
              engine.runAndWait()
              engine.stop()

# Code for ID voices in case more are installed and mess up the indexing
'''
def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Index: {index} | Voice name: {voice.name} | Language: {voice.languages} | ID: {voice.id}")
'''