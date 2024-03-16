## Imports
import json # Reading flashcards and writing statistics data
import subprocess # Clearing the console/terminal
import time # Spacing flashcards automatically, calculate time taken to view cards
import sys # Editing line after being printed
import random # Shuffle flashcards
from playsound import playsound # Sound effects
from settings import * # Import all settings from 'settings.py'

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
            exit(error_message); print()
    else:
        exit(1)

def next_card(last_card_correctness):
    # Choose how long to delay based on if card was right or wrong
    if last_card_correctness == 'wrong':
        delay = 0.55
    elif last_card_correctness == 'right':
        delay = 0.10
    elif last_card_correctness == 'skip' and testing_mode is True:
        clear()
        return None
    else:
        exit(f"Bad option passed for last_card_correctness: {last_card_correctness}")

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
        sys.stdout.flush() # Ensure the frame is displayed
        time.sleep(delay) # Wait briefly before the next frame, but show longer if was wrong

    clear() # Reset the screen for the next flashcard

    show_cursor()

def hide_cursor():
    sys.stdout.write('\033[?25l') # Escape code
    sys.stdout.flush() # Forcibly outputs the terminal's buffer

def show_cursor():
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

def sound(audio_short_title, hold=True):
    if play_sound_effects is True:
        name_to_filepath = {
            "right":"sound/correct.mp3",
            "wrong":"sound/wrong.mp3",
            "beep":"sound/beep.wav",
            "end":"sound/end.wav"
        }
        if hold is False:
            playsound(name_to_filepath[audio_short_title], False)
        else:
            playsound(name_to_filepath[audio_short_title], True)

def remove_accents(the_accented_string):
    s = the_accented_string
    s = s.replace('á', 'a')
    s = s.replace('í', 'i')
    s = s.replace('ñ', 'n')
    return s

def log_correct_or_incorrect(card_prompt, user_result):
        # Remove accents
        card_prompt = remove_accents(card_prompt)

        with open('progress_tracking.json', 'r') as f:
            data = json.load(f)

        # Specify which key to log to based on user_result and increment by 1
        if user_result.lower() == 'correct':
            data[card_prompt]['c'] += 1
        else:
            data[card_prompt]['i'] += 1

        # Save the updated dictionary back to the JSON file (open in overwrite mode)
        with open('progress_tracking.json', 'w') as file:
            json.dump(data, file, indent=4)

def show_user_stats():
    # Open the json file and load its content to 'data'
    with open('progress_tracking.json', 'r') as file:
        stats = json.load(file)

    print("Here's how often you get these cards wrong:\n")

    # Make a list to hold the data of percentage wrong and card info
    wrong_cards_info = []

    # Pick which cards to show
    clear()
    print("Pick a deck to see stats for:")
    print("1) MacOS Terms")
    print("2) Spanish\n")
    deck = input("Type a deck's number: ")
    clear("Here is how often you get these terms correct: \n")

    # Know which type of deck to look at
    if deck == '1':
        deck_filter = "WD" # All MacOS Questions Start Like This
        space_size = 75 # Tells the print functions below how much trailing whitespace to leave
    elif deck == '2':
        deck_filter = "abcdefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVXYZ " # ABC's without Mac question's start with
        space_size = 8
    else:
        error("Unknown deck!\n")


    # Calculate the frequency the term is missed
    for entry in stats:

        # If the key matches the pattern
        if str(entry)[0] in deck_filter:

            entry_dict = stats[entry]

            # Get correct/incorrect numbers from sub-dictionary
            correct_number = entry_dict["c"]
            incorrect_number = entry_dict["i"]

            # Calculate the percentages
            total_times_seen = correct_number + incorrect_number
            wrong_frequency = (correct_number / total_times_seen) * 100

            # Reformat text with accents
            missed_with_accents = put_accents_back_in(entry)

            # Add the term and percent wrong (as a tuple)
            wrong_cards_info.append((wrong_frequency, missed_with_accents))

    # Sort the list by the percentage wrong in descending order
    wrong_cards_info.sort(reverse=True, key=lambda x: x[0])

    # Format and print each card
    for percent_wrong, card in wrong_cards_info:

        # Format the card like how others are
        card = str(card).capitalize()
        percent_wrong_str = f"{round(percent_wrong)}%"  # Round for readability
        spacer_start = " " * (3 - len(percent_wrong_str))
        spacer_end = " " * (space_size - len(card))
        print(f"| {percent_wrong_str}{spacer_start} | {card}{spacer_end} |")

    # Add a new line for readability from terminal entry line
    print()

def put_accents_back_in(word):
    if word == 'rio':
        return 'río'
    elif word == 'montana':
        return 'montaña'
    elif word == 'arbol':
        return 'árbol'
    else: # The correct spelling of the word does not have accents
        return word

def reset_stats():
    is_user_sure = input("Are you really sure you want to reset your stats (Yes/No)? ")
    if is_user_sure == 'Yes':
        erase_all_stats()
    else:
        print("Ok. Your stats are still saved.\n")

def erase_all_stats():
    # Open the JSON file and set 'data' to its dict
    with open('progress_tracking.json', 'r') as file:
        data = json.load(file)
    
    # Set all keys to 0
    reset_dict = {}
    for key in data:
        reset_dict[key] = {"c":0, "i":0}
    # reset_dict = {key: 0 for key in data.keys()} # Go through each key and set it to 0
    
    # Set the whole file back to this version of the dict where all keys equal 0
    with open('progress_tracking.json', 'w') as file:
        json.dump(reset_dict, file, indent=4) # Dump data in proper formatting for json

    print("Your user statistics have been reset!\n")
    exit(0)


def run_stats_screen():
    clear("User statistics")
    print("Please select an option:")
    print("--> 1 - Show stats")
    print("--> 2 - Reset stats")

    stats_screen_user_option = input("\nType a number: ")
    clear()

    if stats_screen_user_option == '1':
        show_user_stats()
    elif stats_screen_user_option == '2':
        reset_stats()
    else:
        exit("That is not a valid option\n")


### Main function that runs the flashcards ###
def run_flashcards():
    # Welcome screen
    clear()
    if testing_mode is True:
        print("[🛠️ DEV MODE IS ON]")

    print("Welcome to Beck's flashcard app!")
    if play_sound_effects is True:
        print("[ 🔊 Sound effects are on ]")
    else:
        print("[ 🔇 Sound effects are muted ]")
    print("\nPlease choose a set to study by typing its number and pressing enter:")
    print("--> 1 - MacOS Terms")
    print("--> 2 - Spanish words")
    print("--> Or type 'stats' to see statistics")

    deck_index = input("\nType a number: ")
    clear()

    # Convert number to file path
    if deck_index == '1':
        flashcard_filepath = 'flashcards_macos.json'
        card_lead_in = ""
        card_lead_out = ""
    elif deck_index == '2':
        card_lead_in = "What is \""
        card_lead_out = "\" in English?"
        flashcard_filepath = 'flashcards_spanish.json'
    elif deck_index == 'stats':
        run_stats_screen()
        return None # Exits this function after showing the stats screen
    else:
        error("I don't have that set!")

    ## Load in flashcards
    with open(flashcard_filepath, 'r') as file:
        # Loads its content into a Python dictionary
        flashcards = dict(json.load(file))

    ## Put flashcards in a random order
    flashcard_keys = list(flashcards.keys())
    random.shuffle(flashcard_keys)

    # Initialize score dict
    score = {'c':0, 's':0} # S stands for number of cards seen

    # Record the start time
    start_time = time.time()

    ## Cycle through flashcards
    for card in flashcard_keys:

        # Format the card like how others are for printing
        old_card = card
        card = str(card).capitalize()

        usr_input = input(f"{card_lead_in}{card}{card_lead_out}\nYour answer: ") # Show prompt and get input

        # Set card back to how it was
        card = old_card

        if usr_input == "" and testing_mode is True: # Skip with dev mode on
            # Code to skip faster when testing w/o logging
            sound('beep', False)
            result = 'skip'
        elif usr_input.lower().replace(" ", "") == str(flashcards[card]).lower(): # Lookup correct answer and compare to the user's input, auto match caps and spaces
            print("- - - - - - - - - - - - - - -\n✅ That is correct!\n- - - - - - - - - - - - - - -")
            score['c'] += 1
            score['s'] += 1
            log_correct_or_incorrect(card, 'correct')
            sound('right', False)
            result = 'right'
        else:
            print(f"- - - - - - - - - - - - - - -\n❌ Sorry, that's not right.\n\nThe correct answer was '{flashcards[card]}'.\n- - - - - - - - - - - - - - -")
            score['s'] += 1
            log_correct_or_incorrect(card, 'incorrect')
            sound('wrong', False)
            result = 'wrong'


        # Show a brief rest screen (auto timed)
        # print("Moving on shortly")
        next_card(result)

    end_time = time.time()

    score_dict = score
    clear()
    time.sleep(1.5) # Allow any sounds to finish playing
    print("🏆 Good job! You've reviewed all the flashcards for this set.")
    score = score['c'] / score['s']
    score = round(score, 2)
    score = score * 100
    score = str(score)
    correct = score_dict['c']
    total = score_dict['s']
    print(f"\n🎯 Accuracy: {score}% ({correct}/{total})")
    time_taken = end_time - start_time
    time_taken_formatted = ""
    mins = time_taken // 60
    seconds = time_taken % 60
    mins = str(round(mins))
    seconds = str(round(seconds))
    if mins == '0':
        time_taken_formatted = f"{seconds} seconds"
    else:
        time_taken_formatted = f"{mins} minutes and {seconds} seconds"
    print(f"🕗 Time taken: {time_taken_formatted}\n\n")
    sound('end')


if __name__ == '__main__':
    run_flashcards()