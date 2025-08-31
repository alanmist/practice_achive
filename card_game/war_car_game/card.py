
SUITS=('hearts','spades','clubs','diamonds')
RANK=['A','2','3','4','5','6','7','8','9','10','J','Q','K']

VALUE={'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13}
class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank= rank
        self.value = VALUE[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    

    def __repr__(self):
        return f"card({self.rank!r}, {self.suit!r})"
    
    def __eq__(self,other):
        
        return self.value== other.value
    
    def __lt__ (self,other):
        
        return  self.value <other.value
        
    def __gt__(self,other):
        return self.value>other.value
    