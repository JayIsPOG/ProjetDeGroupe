import random
from collections import Counter
class Tile:
    def __init__(self, symbol, score):
        self.symbol = symbol
        self.score = score

    def __repr__(self):
        return f"{self.symbol}({self.score})"

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
            1 * [Tile('Y', 10)] + 1 * [Tile('Z', 10)] # + 2 * [Tile('?', 0)] jsp comment confirmer un  mot avec sa...
        )
        random.shuffle(self.tiles)
        self.tiles_left = len(self.tiles)
    def get_tiles(self, num):
        self.tiles_left = max(0, self.tiles_left - num)
        return [self.tiles[i] for i in range(self.tiles_left, self.tiles_left + num)]

class Player:
    def __init__(self, bag, name):
        self.score = 0
        self.name = name
        self.bag = bag
        self.hand_max_size = 7
        self.hand = bag.get_tiles(self.hand_max_size)

    def draw_tiles(self):
        self.hand += self.bag.get_tiles(self.hand_max_size - len(self.hand))
        self.hand_max_size = len(self.hand)

    def redraw(self):
        self.bag.tiles += self.hand
        random.shuffle(self.bag.tiles)
        self.hand = self.bag.get_tiles(self.hand_max_size)