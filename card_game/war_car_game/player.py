
class Player():
    def __init__ (self,name):
        self.name = name
        self.hand= []
        

    def play_card(self):
        return self.hand.pop(0) if self.hand else None
    

    def add_cards(self,cards):
        if cards is None:
            return
        if isinstance(cards,list):
            return self.hand.extend(cards)
        else: 
            self.hand.append(cards)
    
    
    def __str__(self):
        return f'{self.name}: {len(self.hand)} cards'
    
