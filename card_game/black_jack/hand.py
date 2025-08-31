
from card import Card


class Hand():

    def __init__(self):

        self.cards= []


    def add_card (self,card):
        if card is None:
            return
        if isinstance(card,list):
            self.cards.extend(card)
        else:
            self.cards.append(card)

    def best_value(self):
        total=0
        aces=0
        for c in  self.cards:
            r=c.rank
            if r in ['Jack','Queen','King']:
                total += 10
            elif r =="Ace":
                aces+=1
                total+=11
            else:
                total+= int(r)
        while total> 21 and aces:
            total-=10
            aces-=1
        return total
    

    def is_bust(self):
        return self.best_value()> 21
    def is_blackjack(self):
        if len(self.cards)!=2:
            return False
        value={self.cards[0].rank,self.cards[1].rank}
        has_ace="Ace" in value
        has_10= any(v in value for v in ("10","Jack","Queen","King"))
        return has_10 and has_ace
    

    def is_soft(self):
     
        total = 0
        aces = 0
        for c in self.cards:
            r = c.rank
            if r in ('Jack', 'Queen', 'King'):
                total += 10
            elif r == 'Ace':
                total += 11
                aces += 1
            else:
                total += int(r)
        
        while total > 21 and aces:
            total -= 10
            aces -= 1

        return aces > 0 and total <= 21
        
            


            
        
        