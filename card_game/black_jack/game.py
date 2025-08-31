from player import Player, Dealer
from chip import Chips
from deck import Deck


class Game():
    def __init__ (self,player_name='you'):
        self.deck=Deck()
        self.deck.shuffle()
        self.player= Player(player_name)
        self.dealer= Dealer()
        self.gamble=Chips()
    def low_reshuffle(self):
        if len(self.deck)< 15:
            self.deck=Deck()
            self.deck.shuffle()

#player will have 2 card
#dealer will have 2 card
#dealer will show 1 card of his hand
#player will show his 2 card

    def deal_initial(self):
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.low_reshuffle()
        

        self.player.take(self.deck)
        self.dealer.take(self.deck)
        self.player.take(self.deck)
        self.dealer.take(self.deck)
        player_card_1=self.player.hand.cards[0]
        player_card_2=self.player.hand.cards[1]
        dealer_up_card=self.dealer.hand.cards[0]

        return {'player_total':[str(player_card_1),str(player_card_2)],
                'dealer_upcard':str(dealer_up_card)}

    def format_hand(self,cards):
        return ", ".join(str(c) for c in cards)

    def dealer_upcard_str(self):
        return str(self.dealer.hand.cards[0]) if self.dealer.hand.cards else "?"
    def take_bet(self):
        while True:
            try:
                amount = int(input("how many chips would you like to bet? "))
            except ValueError:
                print("Enter a valid integer amount. ")
                continue
            if self.gamble.bet> self.gamble.can_wager(amount):
                print(f'Sorry, your wallet does have enought {self.gamble.wallet}')
                continue
            self.gamble.place_bet(amount)
            print(f'Bet placed:{amount}. wallet now: {self.gamble.wallet} ')
            break
            
                
        
    def player_turn(self):
        while True:
            print(f"\nYour hand:, {self.format_hand(self.player.hand.cards)} (total={self.player.hand.best_value()})")
            print(f"Dealer shows:, {self.dealer_upcard_str()}")     
            choose=input('hit or stand?').lower().strip()
            if choose in ('hit','h'):
                self.player.take(self.deck)
                if self.player.hand.is_bust():
                    print(f"\nYou drew:, {str(self.player.hand.cards[-1])}")
                    print(f'Your hand:, {self.format_hand(self.player.hand.cards)},(total={self.player.hand.best_value()})')
                    print('You Busted. Dealer wins')
                    return "player_bust"
            

            elif choose in ('stand' 's'):
                return "stand"
            else:
                print('type hit of stand')
        
    
    
        


    def dealer_turn(self):
        print(f"\nDealer reveals:, {self.format_hand(self.dealer.hand.cards)} (total={self.dealer.hand.best_value()})")

        self.dealer.play(self.deck)

        print(f"Final dealer hand: {self.format_hand(self.dealer.hand.cards)} (totla={self.dealer.hand.best_value()})")

        if self.dealer.hand.is_bust():
            print("Dealer bust. You win")
            return 'dealer_bust'
        return "delaer_stand or 21"

        


    def determine_winner(self):
        pt=self.player.hand.best_value()
        dt=self.dealer.hand.best_value()

        if pt> dt:
            print(f'\n you Win {pt} vs {dt}')
            return 'player'
        elif dt>pt:
            print(f'Dealer win {dt} vs{pt}')
            return 'dealer'
        else:
            return 'draw'
    
    
    def run(self):
        print(f'staring game between {self.player.name} and {self.dealer.name}')
        
        self.take_bet()
        self.deal_initial()
        
        if self.player.hand.is_blackjack() and self.dealer.hand.is_blackjack():
            print(f"\nYour hand:{self.format_hand(self.player.hand.cards)}-BLACKJACK")
            print(f"\nDealer hand: {self.format_hand(self.dealer.hand.cards)}-BLACKJACK")
            self.gamble.payout_push()
            print(f'Push. wallet: {self.gamble.wallet}')
            return
        elif self.player.hand.is_blackjack():
            print(f"\nYour hand: {self.format_hand(self.player.hand.cards)} - BLACKJACK!")
            print(f"Dealer shows: {self.dealer_upcard_str()}")
            self.gamble.payout_blackjack()
            print(f"You have blackjack! You win! and your wallet{self.gamble.wallet}")

            return
        elif self.dealer.hand.is_blackjack():
            print(f"\nYour hand: {self.format_hand(self.player.hand.cards)}")
            print(f"Dealer's hand: {self.format_hand(self.dealer.hand.cards)} - BLACKJACK!")
            self.gamble.settle_loss()
            print(f"Dealer has blackjack! Dealer wins! and your wallet{self.gamble.wallet}")
            return
        
        state=self.player_turn()
        if state=="player_bust":
            self.gamble.settle_loss()
            print(f'wallet:{self.gamble.wallet}')
            return 
        state=self.dealer_turn()
        if state=="dealer_bust":
            self.gamble.payout_win()
            print(f'wallet: {self.gamble.wallet}')
            return
        self.determine_winner()
        result=self.determine_winner()
        if result=="player":
            self.gamble.payout_win()
        elif result=='dealer':
            self.gamble.settle_loss()
        else:
            self.gamble.payout_push()
        
        print(f"Wallet:{self.gamble.wallet}")
if __name__=="__main__":
    game=Game('ram')
    while True:
        
        game.run()
    
        play_again=input("\nPlay again? (y/n): ").lower().strip()
        if game.gamble.wallet==0:
            print('you dont have enough chip')
            break
        elif play_again not in ("y",'yes'):
            print('Thank you for playing')
        
            break