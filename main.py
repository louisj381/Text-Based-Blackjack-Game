import math
from deck import Deck, Hand

def main():
    while True:
        str_money_limit = input("Welcome to blackjack! Set your limit, play within it:\n")
        try:
            money_limit = int(str_money_limit)
            if money_limit > 0:
                break
            else:
                print("enter a bet amount greater than zero")
        except ValueError:
            print("Please enter an integer.")
    playerHand = Hand(money=int(money_limit))
    deck = Deck()
    dealerHand = Hand(money=0)
    while True:
        early_outcome = setupCards(playerHand, dealerHand, deck)
        if early_outcome == "continue":
            continue
        elif early_outcome == -1:
            break
        gameplay(playerHand, dealerHand, deck)

# start helper functions
#this function expects two cards, so just using at the start of the game
def checkBlackJack(cards):
    if (cards[0][0] != 'A' and cards[1][0] != 'A'):
        return False
    if (cards[0][0] == 'A'):
        if cards[1][0] in Deck.ten_valued_cards:
            return True
        return False
    elif (cards[1][0] == 'A'):
        if cards[0][0] in Deck.ten_valued_cards:
            return True
        return False
    return False

def getBetInput(money_left):
    while True:
        str_bet_amount = input("place your bet! You have " + str(money_left) + " left\nBet: ")
        try:
            bet_amount = int(str_bet_amount)
            if bet_amount > 0 and bet_amount <= money_left:
                break
            else:
                print("enter a bet amount between zero and your total money left: " + str(money_left))
        except ValueError:
            print("Please enter an integer.")
    return bet_amount

# end helper functions

def setupCards(playerHand, dealerHand, deck):
    dealerHand.emptyHand()
    playerHand.emptyHand()
    money_left = playerHand.money
    if playerHand.getBet() == 0 and money_left == 0:
        print("you lost all your money, game over :(")
        return -1
    if playerHand.getBet() > 0:
        decision = input("you've bet "+ str(playerHand.getBet()) + ", do you want to add to bet?(Y/N)\n")
        if decision[0].upper() == 'Y':
            bet_amount = getBetInput(money_left)
            playerHand.setBet(bet_amount)
    else:
        bet_amount = getBetInput(money_left)
        playerHand.setBet(bet_amount)
    first_player_card = deck.getRandomCard()
    second_player_card = deck.getRandomCard()
    playerHand.addCard(first_player_card)
    playerHand.addCard(second_player_card)
    playerHand.print_cards()
    first_dealer_card = deck.getRandomCard()
    dealerHand.addCard(first_dealer_card)
    print("dealers first card: " + str(first_dealer_card))
    #this card is face down, but dealer peaks to ensure it isnt'a blackjack
    second_dealer_card = deck.getRandomCard()
    dealerHand.addCard(second_dealer_card)

    if checkBlackJack([first_dealer_card, second_dealer_card]):
        if checkBlackJack([first_player_card, second_player_card]):
            dealerHand.print_cards("dealer's")
            print("Double Blackjack! What are the odds! Pushing..")
            return "continue"
        else:
            dealerHand.print_cards("dealer's")
            print("Lost! Dealer had blackjack")
            dealerHand.win(playerHand.getBet())
            playerHand.clearBet()
            return "continue"
    elif checkBlackJack([first_player_card, second_player_card]):
        print("Winner! You got blackjack!")
        playerHand.win(playerHand.getBet())
        playerHand.clearBet()
        return "continue"
    return

def gameplay(playerHand, dealerHand, deck):
    while True:
        play_call = input("Hit or stand?\n").strip().lower()
        if play_call == "HIT" or play_call[0] == "h":
            new_card = deck.getRandomCard()
            print("new card is " + str(new_card))
            playerHand.addCard(new_card)
            playerHand.print_cards()
            player_value = playerHand.getBestValue()
            if player_value > 21:
                print("you busted!")
                dealerHand.win(playerHand.getBet())
                playerHand.clearBet()
                break
        elif play_call == "STAND" or play_call[0] == "s":
            #reveal second card
            dealerHand.print_cards("dealer's")
            dealer_value = dealerHand.getBestValue()
            if dealer_value < 17:
                while True:
                    new_card = deck.getRandomCard()
                    print("new card is " + str(new_card))
                    dealerHand.addCard(new_card)
                    dealerHand.print_cards("dealer's")
                    dealer_value = dealerHand.getBestValue()
                    if dealer_value >= 17:
                        break
            if dealer_value > 21:
                print("dealer busted! You win!")
                playerHand.win(playerHand.getBet())
                playerHand.clearBet()
                break
            else: #means dealer has value between 17 and 21
                player_value = playerHand.getBestValue()
                if player_value > dealer_value:
                    print("Winner! Your value of " + str(player_value) + " beats the dealers " + str(dealer_value))
                    playerHand.win(playerHand.getBet())
                    playerHand.clearBet()
                    break
                elif dealer_value > player_value:
                    print("Lost! Dealer's value of " + str(dealer_value) + " is greater than your " + str(player_value))
                    dealerHand.print_cards("dealer's")
                    playerHand.print_cards()
                    dealerHand.win(playerHand.getBet())
                    playerHand.clearBet()
                    break
                else:
                    #push, need to break out of gameplay without adjusting money
                    dealerHand.print_cards("dealer's")
                    playerHand.print_cards()
                    print("Tie! Pushing..")
                    break
        else:
            print("sorry I'm not familar with that option, choose either 'hit' or 'stand'")

main()