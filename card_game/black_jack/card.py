RANKS=['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
SUITS=["Hearts","Clubs","Diamonds","Spades"]
VALUES={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

class Card ():

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
