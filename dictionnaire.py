from Bag import VALID_WORDS
from collections import Counter
class Dictionnaire():
    @staticmethod
    def find_valid_words(player_hand, valid_word_list = VALID_WORDS):
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