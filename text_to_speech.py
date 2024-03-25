import subprocess
from settings import speak_cards # Centralized settings panel


def narrate(text_to_speak):
            if speak_cards is True: # If setting is on, else don't speak anything
              subprocess.run("say hi")

narrate('hello')