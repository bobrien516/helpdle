from colorama import Fore, Style
import sys

def read_dictionary():
    # Path to the system dictionary on macOS
    dictionary_path = '/usr/share/dict/words'
    #dictionary_path = '/tmp/dict/words'

    # Read words from the dictionary file
    with open(dictionary_path, 'r') as file:
        words = [ word for word in file.read().splitlines() if len(word) == 5]

    return words

def colorize_word(word, required_letters, known_positions):
    colored_word = ""
    print(f"colorizing word {word}")
    print(known_positions)
    print(required_letters)
    for i, letter in enumerate(word):
    #    print(f"i: {i}, letter: {letter}")
    #    print(f"get: {known_positions.get(str(i+1))}")
        if letter in required_letters:
            if known_positions.get(str(i + 1)) and word[i] == known_positions[str(i+1)]:
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
        required_letters = set()
        known_positions = {}
        exclude_letters = set()
        
        while True:
            print("\nMenu:")
            print("1. Add required letter")
            print("2. Specify known position")
            print("3. Add exclude letter")
            print("4. Perform search")
            print("5. Exit")

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
                            required_letters.add(letter.lower())
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
                    
                #TODO support negative positions - e.g. it is known that a is not in position 1
            
            if choice == '3':
                exclude_letter_input = input("Enter one or more exclude letters separated by space (or press Enter to skip): ")
                if not exclude_letter_input:
                    break
                for el in exclude_letter_input.split():
                    exclude_letters.add(el.lower())
            
            if choice == '4':
                filtered_words = search_words_by_criteria(words if not filtered_words else filtered_words, required_letters, exclude_letters,known_positions)

                if filtered_words:
                    print(f"Found {len(filtered_words)} words matching search criteria:")
                    if len(filtered_words) < 20:
                        for word in filtered_words:
                            print(word)
                            colored_word = colorize_word(word, required_letters,known_positions)
                            print(colored_word)
                    
                else:
                    print(f"No words found matching the criteria.")
                    sys.exit(0)

            if choice == '5':
                sys.exit(0)

if __name__ == "__main__":
    # Initialize colorama for Windows compatibility
    if sys.platform.startswith('win'):
        import colorama
        colorama.init()
    
    main()