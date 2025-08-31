from card import Card, SUITS, RANK
import random



class Deck():
    
            
    def __init__(self,):
        self.cards=[]
       
        for i in SUITS:
            for j in RANK:
                
                self.cards.append(Card(i,j))

    def shuffle(self):
        random.shuffle(self.cards)
    
    

    def __len__(self):
        return len(self.cards)
    

