from colorama import Fore, Style
from collections import defaultdict
import sys

def read_dictionary():
    # Path to the system dictionary on macOS
    #TODO add support to detect OS and set path to dictionary 
    dictionary_path = '/usr/share/dict/words'
   

    # Read words from the dictionary file
    with open(dictionary_path, 'r') as file:
        words = [ word for word in file.read().splitlines() if len(word) == 5]

    return words

def colorize_word(word, required_letters, known_positions):
    colorized_word = ""
    '''
    loop through lettters in word
    if letter is in required letters highlight yellow
    if letter is in required letters and at specified position highlight green
    '''
    for i, letter in enumerate(word):
        if letter in required_letters:
            if known_positions.get(str(i + 1)) and word[i] == known_positions[str(i+1)]:
                colorized_word += Fore.GREEN + letter + Style.RESET_ALL
            else:
                colorized_word += Fore.YELLOW + letter + Style.RESET_ALL
        else:
            colorized_word += letter
    return colorized_word

def search_words_by_criteria(words, required_letters, exclude_letters, known_positions,negative_positions):
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
            for position, letters in negative_positions.items():
                if word_lower[int(position) - 1] in letters:
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
        required_letters = set()
        exclude_letters = set()
        known_positions = {}
        negative_positions = defaultdict(set)
        
        while True:
            print("\nMenu:")
            print("1. Add required letter")
            print("2. Specify known position")
            print("3. Specify negative position")
            print("4. Add exclude letter")
            print("5. Perform search")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                if len(required_letters) == 5:
                    print("You have already specified the maximum of 5 required letters")
                else:
                    letters = input("Enter one or more required letters: ")
                    if not letters:
                        break
                    for letter in letters:
                        if letter.isalpha():
                            if letter not in exclude_letters:
                                required_letters.add(letter.lower())
                            else:
                                print(f"letter {letter} in exclude list, cannot be required")
                        else:
                            print(f"invalid required letter {letter}")

            if choice == '2':    
                l2p = input("Enter the letter and it's position (1 to 5) separated by a colon, e.g. 'a:1': ")
                if not l2p:
                    break
                else:
                    (letter,position) = l2p.split(':')
                    if not letter.isalpha():        
                        print(f"invalid letter: {letter}")
                    else:
                        required_letters.add(letter.lower())
                        try:
                            if 1 <= int(position) <= 5:
                                known_positions[position] = letter.lower()
                        except ValueError:
                            print(f"invalid position {position}, must be between 1 and 5")
            
            if choice == '3':
                l2p = input("Enter the letter and a position it cannot occupy (1 to 5) separated by a colon, e.g. 'a:1': ")
                if not l2p:
                    break
                else:
                    (letter,position) = l2p.split(':')
                    if not letter.isalpha():        
                        print(f"invalid letter: {letter}")
                    else:
                        required_letters.add(letter.lower())
                        try:
                            if 1 <= int(position) <= 5:
                                negative_positions[position].add(letter.lower())
                        except ValueError:
                            print(f"invalid position {position}, must be between 1 and 5")
            
            if choice == '4':
                exclude_letter_input = input("Enter one or more exclude letters separated by space (or press Enter to skip): ")
                if not exclude_letter_input:
                    break
                for letter in exclude_letter_input.split():
                        if letter.isalpha():
                            if letter not in required_letters:
                                exclude_letters.add(letter.lower())
                            else:
                                print(f"letter {letter} in required list, cannot be excluded")
                        else:
                            print(f"invalid required letter {letter}")

            
            if choice == '5':
                filtered_words = search_words_by_criteria(words if not filtered_words else filtered_words, required_letters, exclude_letters,known_positions,negative_positions)

                if filtered_words:
                    display = input(f"Found {len(filtered_words)} words matching search criteria. Display them? (y/n)")
                    if display in ('Y','y'): 
                        for word in filtered_words:
                            #print(word)
                            colorized_word = colorize_word(word, required_letters,known_positions)
                            print(colorized_word)
                    
                else:
                    print(f"No words found matching the criteria:")
                    print(f"required_letters: {required_letters}")
                    sys.exit(0)

            if choice == '6':
                sys.exit(0)

if __name__ == "__main__":
    main()