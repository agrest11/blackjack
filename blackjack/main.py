from random import shuffle

# heart chr(9829) ♥
# diamond chr(9830) ♦
# spade chr(9824) ♠
# club = chr(9827) ♣

suits = [chr(9829), chr(9830), chr(9824), chr(9827)]
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f'{self.rank} {self.suit}'


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def __repr__(self):
        return f'Cards remaining in deck: {len(self.cards)}'

    def shuffle(self):
        if len(self.cards) < 52:
            raise ValueError("Only full decks can be shuffled!")
        shuffle(self.cards)
        return self

    def deal(self):
        if len(self.cards) == 0:
            raise ValueError("All cards have been dealt")
        return self.cards.pop()

    def reset(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, one_card):
        self.cards.append(one_card)
        self.value += values[one_card.rank]

    def reset(self):
        self.cards = []
        self.value = 0


def display_hand(which_hand):
    for i, some_card in enumerate(which_hand.cards):
        if i != 0:
            print(', ', end=' ')
        print(some_card, end=' ')


def play_again(money_for_bet):
    if money_for_bet == 0:
        print("Sorry, but you're broke. You can't play again.")
        exit()
    answer = input('Do you wanna play again? (yes/no)\n')
    if not answer.lower().startswith('y'):
        exit()
    my_deck.reset()
    my_deck.shuffle()
    my_hand.reset()
    dealer_hand.reset()
    money_for_bet, to_bet = get_bet(money_for_bet)
    return money_for_bet, to_bet


def get_bet(money_for_bet):
    print(f'You have {money_for_bet} money left.')
    to_bet = input('How much do you want to bet?\n')
    while not to_bet.isdecimal():
        to_bet = input('Enter the number: ')
    money_for_bet -= int(to_bet)
    print(f'Money left: {money_for_bet}')
    return money_for_bet, int(to_bet)


my_deck = Deck()
my_deck.shuffle()
my_hand = Hand()
dealer_hand = Hand()
money = 500
money, bet = get_bet(money)

while True:
    print("\nWhat do you want to do?\n(1) Hit\n(2) Stand\n(4) Exit\n")
    choice = input()
    while not choice.isdecimal() or int(choice) > 4 or int(choice) < 1:
        choice = input('Enter the number (1-4): ')
    choice = int(choice)

    if choice == 1:
        my_hand.add_card(my_deck.deal())
        display_hand(my_hand)
        print(f'\n{my_hand.value}')
        if my_hand.value == 21:
            print('\nYou won!')
            money += 2*bet
            money, bet = play_again(money)
        elif my_hand.value > 21:
            print(f'\nYou lost! You have {money} money.')
            money, bet = play_again(money)

    elif choice == 2:
        while dealer_hand.value < 17:
            dealer_hand.add_card(my_deck.deal())
        display_hand(dealer_hand)
        print(f'\n{dealer_hand.value}')
        if dealer_hand.value == 21 or dealer_hand.value > my_hand.value:
            print(f'\nDealer won! You have {money} money.')
            money, bet = play_again(money)
        elif dealer_hand.value == my_hand.value:
            print("\nIt's a tie!")
            money += bet
            money, bet = play_again(money)
        else:
            print('\nYou won!')
            money += 2*bet
            money, bet = play_again(money)

    else:
        exit()
