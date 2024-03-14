## Imports
import json # Reading flashcards and writing statistics data
import subprocess # Clearing the console/terminal
import time # Spacing flashcards automatically
import sys # Editing line after being printed
import random # Shuffle flashcards

### Custom function definitions ###
def clear(message_after_refresh=None):
    subprocess.run("clear", shell=False)
    if message_after_refresh is not None:
        print(message_after_refresh)

def error(error_message=None):
    if error_message is not None:
        if error_message == 0:
            error("Impossible: an exit code of 0 (evoked) is used only for success, but 'error()' was called")
        else:
            exit(error_message)
    else:
        exit(1)

def next_card():
    hide_cursor()

    # Make frames of the waiting to move-on screen
    frames = []
    for filled_in in range (11):
        blank = 10 - filled_in
        current_frame = "■ "*filled_in + "□ "*blank
        frames.append(current_frame[:-1])

    # Write and overwrite the line with the current frame of the waiting to move-on screen
    for frame in frames:
        sys.stdout.write('\r' + frame)  # '\r' brings the cursor back to the start of the line
        sys.stdout.flush()  # Ensure the frame is displayed
        time.sleep(0.2)  # Wait briefly before the next frame

    clear() # Reset the screen for the next flashcard

    show_cursor()

def hide_cursor():
    sys.stdout.write('\033[?25l') # Escape code
    sys.stdout.flush() # Forcibly outputs the terminal's buffer

def show_cursor():
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

def log_correct_or_incorrect(card_prompt, user_result):
        if user_result.lower() == 'correct':
            KEY_TO_FIND = f"CORRECT___{card_prompt}"
        else:
            KEY_TO_FIND = f"INCORRECT___{card_prompt}"

        # Load the JSON data from the file tracking file to read
        with open('progress_tracking.json', 'r') as file:
            data = json.load(file)

        # Check if the key exists and increment its value
        if KEY_TO_FIND in data:
            data[KEY_TO_FIND] += 1
        else:
            error(f"The key '{KEY_TO_FIND}' was not found in the dictionary.")

        # Save the updated dictionary back to the JSON file (open in overwrite mode)
        with open('progress_tracking.json', 'w') as file:
            json.dump(data, file, indent=4)

### Main function that runs the flashcards ###
def run_flashcards():
    # Welcome screen
    clear()
    print("Welcome to Beck's flashcard app!\n")
    print("Please choose a set to study by typing its number and pressing enter:")
    print("--> 1 - MacOS Terms")
    print("--> 2 - Spanish words")
    deck_index = input("\nType a number: ")
    clear()

    # Concert number to file path
    if deck_index == '1':
        flashcard_filepath = 'flashcards_macos.json'
    elif deck_index == '2':
        flashcard_filepath = 'flashcards_spanish.json'
    else:
        error("I don't have that set!")

    ## Load in flashcards
    with open(flashcard_filepath, 'r') as file:
        # Loads its content into a Python dictionary
        flashcards = dict(json.load(file))

    ## Put flashcards in a random order
    flashcard_keys = list(flashcards.keys())
    random.shuffle(flashcard_keys)

    ## Cycle through flashcards
    for card in flashcard_keys:
        usr_input = input(f"{card}\n--> ") # Show prompt and get input
        if usr_input == flashcards[card]: # Lookup correct answer and compare to the user's input
            print("That is correct!\n")
            log_correct_or_incorrect(card, 'correct')
        else:
            print(f"Sorry, the correct answer was {flashcards[card]}\n")
            log_correct_or_incorrect(card, 'incorrect')


        # Show a brief rest screen (auto timed)
        print("Moving on shortly")
        next_card()

    print("Good job! You've review all flashcards.")

if __name__ == '__main__':
    run_flashcards()