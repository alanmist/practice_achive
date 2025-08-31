
class Chips:
    def __init__(self, starting=100):
        self.wallet = starting
        self.bet = 0

    def can_wager(self, amount: int) -> bool:
        return amount > 0 and amount <= self.wallet

    def place_bet(self, amount: int) -> None:
        """Lock stake at start of round."""
        if not self.can_wager(amount):
            raise ValueError("Invalid bet amount.")
        self.bet = amount
        self.wallet -= amount   # stake locked

    def payout_win(self) -> None:
        """Standard 1:1 win (return stake + winnings)."""
        self.wallet += self.bet * 2
        self.bet = 0

    def payout_blackjack(self, num=3, den=2) -> None:
        """Blackjack 3:2 (configurable)."""
        self.wallet += self.bet + (self.bet * num) // den
        self.bet = 0

    def payout_push(self) -> None:
        """Tie → refund stake."""
        self.wallet += self.bet
        self.bet = 0

    def settle_loss(self) -> None:
        """Already deducted stake on place_bet; nothing to add back."""
        self.bet = 0
