
from deck import Deck
from player import Player

class Game():
    
    def __init__(self,player1, player2):
        self.player1= Player(player1)
        self.player2 =Player(player2)
        self.round_count=0
        self.max_round=100000
        self.war_count=0
    
        full_deck=Deck()
        full_deck.shuffle()
        self.player1.add_cards(full_deck.cards[:26])
        self.player2.add_cards(full_deck.cards[26:])
        
    
    def play_round(self):
        self.round_count+=1
        pot=[]
        
        playing_card1=self.player1.play_card()
        playing_card2=self.player2.play_card()
        if playing_card1 is None or playing_card2 is None:
            return 
        pot.extend([playing_card1,playing_card2])
        print(f'Round {self.round_count}: {self.player1.name} plays {playing_card1}, {self.player2.name} plays {playing_card2}')


        if playing_card1>playing_card2:
            self.player1.add_cards(pot)
            print(f"{self.player1.name} wins the round")
        
        elif playing_card1<playing_card2:
            self.player2.add_cards(pot)
            print(f'{self.player2.name} wins the round')
        
        else:
            print('WAR')
            self.handle_war(pot)

   
   
    def handle_war(self, pot, depth=0):
        self.war_count+=1
        if depth> 5:
            print('War has gone to deep')
            half=len(pot)//2
            self.player1.add_cards(pot[:half])
            self.player2.add_cards(pot[half:])
            return
        
        need_face_down=3
        if len(self.player1.hand)<need_face_down+1:
            print(f"{self.player1.name} doesn't have enought cards for war. {self.player2.name} Wins")
            self.player2.add_cards(pot)
            self.player1.hand=[]
            return
        if len(self.player2.hand)<need_face_down+1:
            print(f"{self.player2.name} doesn't have enought cards for war. {self.player1.name} Wins")
            self.player1.add_cards(pot)
            self.player2.hand=[]
            return
        print(f'Each player puts {need_face_down} cars face down')
        for i in range (need_face_down):
            pot.append(self.player1.play_card())
            pot.append(self.player2.play_card())
        
        war_card1=self.player1.play_card()
        war_card2= self.player2.play_card()

        if war_card1 is None or war_card2 is None:
            return
        
        pot.extend([war_card1,war_card2])
        print(f'War cards: {self.player1.name} plays {war_card1}, {self.player2.name} palys {war_card2} ')

        if war_card1> war_card2:
            self.player1.add_cards(pot)
            print(f'{self.player1.name} wins the war!')
        elif war_card2> war_card1:
            self.player2.add_cards(pot)
            print(f'{self.player2.name} wins the war!')
        else:
            print("war again")
            self.handle_war(pot,depth +1)

       

    def check_winner(self):
        if  len(self.player1.hand) == 0 :
            return f'{self.player2.name} won the game'
        elif len(self.player2.hand)==0:
            return f'{self.player1.name} won'
        elif self.round_count>= self.max_round:
            return 'game is draw'
        else:
            return None
    def play_game(self):
        print(f'statring game between {self.player1.name} and {self.player2.name}')

        while True:
            winner= self.check_winner()
            if winner:
                print(winner)
                print(f"Game ended after {self.round_count} rounds with {self.war_count} wars")
                break
            
            self.play_round()

            
            if self.round_count %100 ==0 and self.round_count > 0:
                print(f'Played {self.round_count} rounds so far...')


if __name__=="__main__":
    Game('ram','sam').play_game()




        
    