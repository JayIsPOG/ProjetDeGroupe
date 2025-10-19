import random
from collections import Counter
def charger_dictionnaire(nom_fichier="French ODS dictionary.txt"):
    try:
        with open(nom_fichier, 'r') as f:
            mots = {ligne.strip().upper() for ligne in f}
        return mots
    except FileNotFoundError:
        print(f"ERREUR : Le fichier '{nom_fichier}' est introuvable. Veuillez le creer et le remplir.")
        return set()
VALID_WORDS = charger_dictionnaire("French ODS dictionary.txt")
class Tile:
    def __init__(self, symbol, score):
        self.symbol = symbol
        self.score = score

    def __repr__(self):
        return f"'{self.symbol}'({self.score})"

class Bag:
    def __init__(self):
        self.tiles = list(
            9 * [Tile('A', 1)] + 2 * [Tile('B', 3)] + 2 * [Tile('C', 3)] +
            3 * [Tile('D', 2)] + 15 * [Tile('E', 1)] + 2 * [Tile('F', 4)] +
            2 * [Tile('G', 2)] + 2 * [Tile('H', 4)] + 8 * [Tile('I', 1)] +
            1 * [Tile('J', 8)] + 1 * [Tile('K', 10)] + 5 * [Tile('L', 1)] +
            3 * [Tile('M', 2)] + 6 * [Tile('N', 1)] + 6 * [Tile('O', 1)] +
            2 * [Tile('P', 3)] + 1 * [Tile('Q', 8)] + 6 * [Tile('R', 1)] +
            6 * [Tile('S', 1)] + 6 * [Tile('T', 1)] + 6 * [Tile('U', 1)] +
            2 * [Tile('V', 4)] + 1 * [Tile('W', 10)] + 1 * [Tile('X', 10)] +
            1 * [Tile('Y', 10)] + 1 * [Tile('Z', 10)] + 2 * [Tile('?', 0)]
        )

class Player:
    def __init__(self, bag, name):
        self.name = name
        self.bag = bag
        self.hand_max_size = 7
        self.hand = self.starting_hand()

    def starting_hand(self):
        tiles = []
        for i in range(self.hand_max_size):
            if not self.bag.tiles:
                break
            picked_tile = random.choice(self.bag.tiles)
            tiles.append(picked_tile)
            self.bag.tiles.remove(picked_tile)
        return tiles

    def draw_tiles(self):
        tiles_to_draw = self.hand_max_size - len(self.hand)
        for i in range(tiles_to_draw):
            if not self.bag.tiles:
                break
            picked_tile = random.choice(self.bag.tiles)
            self.hand.append(picked_tile)
            self.bag.tiles.remove(picked_tile)


def find_valid_words(player_hand, valid_word_list):
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

game_bag = Bag()
player = Player(game_bag, "Alice")

print(f"Hand of {player.name}: {player.hand}")
player.hand = [Tile('L', 8), Tile('E', 1), Tile('A', 1), Tile('O', 10), Tile('J', 0), Tile('R', 1), Tile('S', 1)]
print(f"(Forced hand for demo: {player.hand})")


results = find_valid_words(player.hand, VALID_WORDS)


sorted_results = sorted(list(results), key=lambda x: (x, len(x)))

print(sorted_results)
