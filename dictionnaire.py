from collections import Counter
VALID_WORDS = set()
with open("French ODS dictionary.txt", 'r') as f:
    for i in f:
        VALID_WORDS.add(tuple(i[:-1]))

class Dictionary():
    @staticmethod
    def find_valid_words(self, player_hand, valid_word_list = VALID_WORDS):
        hand_symbols = [tile.symbol for tile in player_hand]
        hand_counts = Counter(s for s in hand_symbols if s != '?')
        num_blanks = hand_symbols.count('?')

        found_words = set()

        for word in valid_word_list:
            if 2 <= len(word) <= len(player_hand):
                word_counts = Counter(word.upper())
                blanks_used = 0
                can_form = True
                for letter, requirement in word_counts.items():
                    available = hand_counts.get(letter, 0)
                    missing = requirement - available

                    if missing > 0:
                        if missing <= (num_blanks - blanks_used):
                            blanks_used += missing
                        else:
                            can_form = False
                            break 
                if can_form:
                    found_words.add(word)
        return found_words
<<<<<<< Updated upstream
    def is_word_valid(self, word):
        return word in VALID_WORDS
    def find_valid_words(self, letters):
        words = set()
        for word in VALID_WORDS:
            if letters in word:
                words.add(word)
=======
    @staticmethod
    def is_word_valid(word):
        return word in VALID_WORDS
>>>>>>> Stashed changes
