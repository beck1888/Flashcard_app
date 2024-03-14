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
        time.sleep(0.03)  # Wait briefly before the next frame

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

        # Specify which key to log to based on user_result
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

def show_user_stats():
    # Open the json file and set its dict to 'data'
    with open('progress_tracking.json', 'r') as file:
        data = json.load(file)

    # Assign random dict values in test/dev mode to prevent 'not enough data' errors
    testing_mode_on = True
    if testing_mode_on is True:
        data = {key: random.randint(30, 273) for key in data.keys()}

    # Get only the wrong keys from the dict
    new_dict = {}
    for key in data:
        if key[:12] == 'INCORRECT___':
            new_dict[key] = data[key]

    # Change the loaded dict 'key' to the new one (easier for naming)
    data_new = new_dict

    # # Use the max() function on all the keys's values's to find the highest
    # highest_value = max(data_new.values())

    # # Add all keys with that highest value to a list by iterating through all the keys
    # highest_keys = [key for key, value in data_new.items() if value == highest_value]

    # Going show all keys. Replacing values with odd names for now to keep things working.
    highest_keys = data

    # Display the most missed ones in an easy to see way
    for missed in highest_keys:
        missed_with_accents = put_accents_back_in(missed)

        # # Validate there is enough data to show stats (avoid dividing by 0)
        # if data[f"INCORRECT___{missed}"] == 0:
        #     exit("Not enough data to show stats!\n")
        # elif data[f"CORRECT___{missed}"] == 0:
        #     exit("Not enough data to show stats!\n")

        
        # Calculate the frequency the term is missed
        incorrect_name = str(missed[10:]); incorrect_name = "INCORRECT___" + incorrect_name
        correct_name = missed

        sum_of_tries = data[incorrect_name.replace('_____', '___')] + data[correct_name]
        percent_wrong = data[incorrect_name] / sum_of_tries
        percent_wrong = percent_wrong * 100
        percent_wrong = round(percent_wrong, 3)

        # Print out the term and percent wrong
        missed = str(missed).removeprefix("INCORRECT___")
        show_wrong_cards = []
        show_wrong_cards.append(f"> {missed_with_accents} | {percent_wrong}% wrong")
        
        # # Calculate frequency each card is incorrect
        # wrong_cards = []
        # for key in data:
        #     key = str(key)
        #     key = key.removeprefix("CORRECT___")
        #     key = key.removeprefix("INCORRECT___")
        #     print(key)

    
    # Add space for visibility
    print("Here are the cards you get wrong the most often: ")
    for item in wrong_cards:
        print(item)
    print("\n")

def put_accents_back_in(word):
    if word == 'rio':
        return 'río'
    elif word == 'montana':
        return 'montaña'
    elif word == 'arbol':
        return 'árbol'
    else: # The correct spelling of thr word does not have accents
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
    reset_dict = {key: 0 for key in data.keys()} # Go through each key and set it to 0
    
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
    print("\n--> Or type 0 to see statistics")

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
        usr_input = input(f"{card}\n--> ") # Show prompt and get input
        if usr_input == flashcards[card]: # Lookup correct answer and compare to the user's input
            print("That is correct!\n")
            log_correct_or_incorrect(card, 'correct')
        else:
            print(f"Sorry, the correct answer was {flashcards[card]}\n")
            log_correct_or_incorrect(card, 'incorrect')


        # Show a brief rest screen (auto timed)
        # print("Moving on shortly")
        print()
        next_card()

    print("Good job! You've reviewed all the flashcards for this set.")

if __name__ == '__main__':
    run_flashcards()