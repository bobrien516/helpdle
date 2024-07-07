from colorama import Fore, Style
import sys

def read_dictionary():
    # Path to the system dictionary on macOS
    dictionary_path = '/usr/share/dict/words'

    # Read words from the dictionary file
    with open(dictionary_path, 'r') as file:
        words = [ word for word in file.read().splitlines() if len(word) == 5]

    return words

def colorize_word(word, required_letters):
    colored_word = ""
    for i, letter in enumerate(word):
        if int(i + 1) in required_letters.keys(): # check if we had flagged the position
            if word[i] == required_letters[str(i + 1)]:
                colored_word += Fore.GREEN + letter + Style.RESET_ALL
            else:
                colored_word += Fore.YELLOW + letter + Style.RESET_ALL
        else:
            colored_word += letter
    return colored_word

'''
loop through lettters in word
if letter is in required letters highlight yellow
if letter is in required letters and at specified position highlight green
'''

def search_words_by_criteria(words, required_letters, exclude_letters, known_positions):
    # Filter words based on the criteria
    filtered_words = []

    for word in words:
        word_lower = word.lower()
        match = True
        for position, letter in known_positions.items():
            # Check exact position
            if word_lower[int(position) - 1] != letter:
                match = False
                break
        
        if match:
            for letter in required_letters:
                if letter not in word:
                    match = False
                    break

        if match:
            for exclude_letter in exclude_letters:
                if exclude_letter in word_lower:
                    match = False
                    break
        
        if match:
            filtered_words.append(word_lower)

    return filtered_words

def main():
    words = read_dictionary()
    filtered_words = []

    while True:
        required_letters = []
        known_positions = {}
        exclude_letters = []
        
        while True:
            #TODO - do not accept more than 5 required letter args
            letter = input("Enter a required letter (or press Enter to finish): ")
            if not letter:
                break
            required_letters.append(letter.lower())

            position = input("Enter its position (1 to 5, or leave blank if unknown): ")
            if position:
                known_positions[position] = letter.lower()
                
        if not required_letters:
            break

        while True:
            exclude_letter_input = input("Enter one or more exclude letters separated by space (or press Enter to skip): ")
            if not exclude_letter_input:
                break
            for el in exclude_letter_input.split():
                exclude_letters.append(el.lower())

        filtered_words = search_words_by_criteria(words if not filtered_words else filtered_words, required_letters, exclude_letters,known_positions)

        if filtered_words:
            print(f"Found {len(filtered_words)} words matching search criteria:")
            for word in filtered_words:
                #colored_word = colorize_word(word, required_letters)
                #print(colored_word)
                print(word)
        else:
            print(f"No words found matching the criteria.")

if __name__ == "__main__":
    # Initialize colorama for Windows compatibility
    if sys.platform.startswith('win'):
        import colorama
        colorama.init()
    
    main()