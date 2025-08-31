import logging
logging.basicConfig(level=logging.INFO, format="%(message)s-%(levelname)s-%(asctime)s")

from deck import Deck
from hand import Hand


class Player():
    def __init__(self,name,hand:Hand| None=None):
        self.name= name
        self.hand= hand or Hand()

    def take(self, deck:Deck):
        self.hand.add_card(deck.deal_one())
    
    def reset_hand(self):
        self.hand= Hand()
    
    def __str__(self):
        return f"{self.name}: {self.hand.best_value()}"
    
class Dealer(Player):
    def __init__(self,hand:Hand|None=None, name:str ="Dealer",on_soft: bool=True):
        super().__init__(name,hand)
        self.on_soft=on_soft
    

    def play(self, deck):

        while True:
            total=self.hand.best_value()
            soft=self.hand.is_soft()
            
            if total<17:
                self.take(deck)
                continue
            if total==17 and soft and not self.on_soft:
                self.take(deck)
                continue

            break
