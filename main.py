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
        sys.stdout.flush() # Ensure the frame is displayed
        time.sleep(0.25) # Wait briefly before the next frame

    clear() # Reset the screen for the next flashcard

    show_cursor()

def hide_cursor():
    sys.stdout.write('\033[?25l') # Escape code
    sys.stdout.flush() # Forcibly outputs the terminal's buffer

def show_cursor():
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

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
        error("Unknown deck!")


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
        print("Ok. Your stats are still saved.")

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

    print("Your user statistics have been reset!")
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
        exit("That is not a valid option")


### Main function that runs the flashcards ###
def run_flashcards():
    # Welcome screen
    clear()
    print("Welcome to Beck's flashcard app!\n")
    print("Please choose a set to study by typing its number and pressing enter:")
    print("--> 1 - MacOS Terms")
    print("--> 2 - Spanish words")
    print("\n--> Or type '0' to see statistics")

    deck_index = input("\nType a number: ")
    clear()

    # Concert number to file path
    if deck_index == '1':
        flashcard_filepath = 'flashcards_macos.json'
    elif deck_index == '2':
        flashcard_filepath = 'flashcards_spanish.json'
    elif deck_index == '0':
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

    ## Cycle through flashcards
    for card in flashcard_keys:
        usr_input = input(f"{card}\n\n--> ") # Show prompt and get input
        if usr_input == flashcards[card]: # Lookup correct answer and compare to the user's input
            print("\nThat is correct!\n")
            log_correct_or_incorrect(card, 'correct')
        else:
            print(f"\nSorry, the correct answer was '{flashcards[card]}'\n")
            log_correct_or_incorrect(card, 'incorrect')


        # Show a brief rest screen (auto timed)
        # print("Moving on shortly")
        print()
        next_card()

    print("Good job! You've reviewed all the flashcards for this set.")

if __name__ == '__main__':
    run_flashcards()