from card import Card, RANKS, SUITS

import random

class Deck():
    
    def __init__(self):
        self.cards=[]
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal_one(self):
        return self.cards.pop()


    def __str__(self):
        return "\n".join(str(card)for card in self.cards)
    
    def __len__(self):
        return len(self.cards)