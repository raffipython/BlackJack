# -*- coding: utf-8 -*-

import random
from pprint import pprint
from Card import Card

import sys
sys.path.append(".")


class Blackjack():
    """Main Blackjack class"""

    def __init__(self, number_of_players, number_of_decks, table_min):
        """ Init method """
        self.number_of_players = number_of_players
        self.number_of_decks = number_of_decks
        self.deck = self.deck_builder()
        self.round = 0
        self.players = self.players_builder()
        self.table_min = table_min

    def deck_builder(self):
        """ Deck builder method """
        main_deck = []
        for deck in xrange(self.number_of_decks):
            for suit in ["CLUBS", "HEARTS", "DIAMONDS", "SPADES"]:
                for card in xrange(13):
                    main_deck.append("{}_{}_{}".format(card + 1, suit, deck))
        return main_deck

    def players_builder(self):
        """ Players builder method """
        players = []
        for p in range(0, self.number_of_players + 1):
            if p == 0:
                name = "Dealer"
            else:
                # Ask for player name
                name = raw_input("\nEnter name for player # {}\n".format(p))
            # Hand 1 is main, 2 is split, 3 is double split.
            # Phase is place holder for in round player phase.
            data = {"NAME": name,
                    "ONE": 0,
                    "TWO": 0,
                    "THREE": 0,
                    "POT_ONE": 0,
                    "POT_TWO": 0,
                    "POT_THREE": 0,
                    "BALANCE": 1000,
                    "PHASE": 0}
            players.append(data)
        return players

    def deck_remove_card(self, index):
        """ Removes a card at given index """
        del self.deck[index]

    def rounds(self):
        """ Increases the round count """
        self.round += 1

    def round_check(self):
        """ Check if all player turns are over to finish the round """
        phase = 0

        ## Don't bother if dealer got 21
        # if self.players[0].get("POT_ONE") == 21:
        #    return True

        for i in self.players:
            if i.get("PHASE") == 100:
                phase += 100
        if phase == len(self.players) * 100:
            return True
        else:
            return False

    def next_card(self):
        """ Returns a random card from the deck """
        index = random.randint(0, len(self.deck) - 1)
        return [index, self.deck[index]]

    def init_pot(self):
        for i in self.players:

            good_input = False
            bet = self.table_min

            while not good_input:
                x = raw_input("\nHow much you want to bet? [min. {}]\n".format(self.table_min).strip())
                try:
                    bet = int(x)
                    good_input = True
                except:
                    print "Error, please try again"

            i.update({"POT_ONE": bet})

    def reset_pots(self):
        for p in range(0, len(self.players)):
            self.players[p][4] = 0
            self.players[p][5] = 0
            self.players[p][6] = 0

    def player_details(self, player):
        """ Prints player snapshot"""

        print """
            NAME:   {}
            ONE:    {}
            TWO:    {}
            THREE:  {}
            POT_1:  {}   
            POT_2:  {}
            POT_3:  {} 
            BALANCE:    {}
            PHASE":     {}
            """.format(
            self.players[player].get("NAME"),
            self.players[player].get("ONE"),
            self.players[player].get("TWO"),
            self.players[player].get("THREE"),
            self.players[player].get("POT_ONE"),
            self.players[player].get("POT_TWO"),
            self.players[player].get("POT_THREE"),
            self.players[player].get("BALANCE"),
            self.players[player].get("PHASE"))

    def update_balance(self, player, balance):
        """ Updates the balance of a player"""
        self.players[player][7] = balance

    def update_bet(self, player, hand, bet):
        """ Updates a given bet for a hand of a player
        hand 4 for HAND_ONE, 5 for HAND_TWO, 6 for HAND_THREE"""
        self.players[player][hand] = bet

    def update_phase(self, player, phase):
        """ Updates the phase of a player"""
        self.players[player][8] = phase

    @staticmethod
    def card_value(card):
        """ Returns the value of a card or asks the player if the card is an Ace """
        c = int(card.split("_")[0])
        if c == 1:
            good_input = False
            while not good_input:
                x = raw_input("\nDrawn an Ace, count as 1 or 11? [Enter 1 or 11]\n".strip())
                try:
                    c = int(x)
                    good_input = True
                except:
                    print "Error, please try again"

        elif c > 9:
            c = 10
        return c

    @staticmethod
    def phase_details(p):
        phase = "UNKNOWN"
        if p == 0:
            phase = "Beginning of a round"
        elif p == 21:
            phase = "Player/Dealer won"
        elif p == 22:
            phase = "Player/Dealer busted"
        elif p == 100:
            phase = "Player/Dealer round is over"
        return phase

    def dealer_turn(self):
        """ Turn method for dealer """

        # test
        card = self.next_card()
        self.deck_remove_card(card[0])
        # end test

        # Print dealer snapshot
        self.player_details(0)

        # self.players[0].update({"PHASE": 100})

    def player_turn(self, player):
        """ Turn method for each player, may get called multiple times in a round"""

        """
        self.players[player].update({"ONE": self.next_card()})

        self.players[player].update({"TWO": self.next_card()})

        c1v = self.card_value(self.players[player].get("ONE"))
        c2v = self.card_value(self.players[player].get("TWO"))

        print player
        print "CARD 1 VALUE {}".format(c1v)
        print "CARD 2 VALUE {}".format(c2v)

        self.players[player].update({"POT_ONE": c1v + c2v})

        if self.players[player].get("POT_ONE") > 21 or self.players[player].get("POT_ONE") > 21 or self.players[
            player].get("POT_ONE") > 21:
            self.players[player].update({"PHASE": 100})

        if self.players[player].get("POT_ONE") == 21:
            print self.players[player].get("NAME")
            print "WINNNNNNER !!!!!!!!!!!!!!!!!!"

        #self.players[player].update({"PHASE": 100})

        """

        # test
        card = self.next_card()
        self.deck_remove_card(card[0])
        # end test

        # Print player snapshot
        self.player_details(player)
        print self.phase_details(self.players[player].get("PHASE"))

    def card_drawer(self, card):
        parts = card.split("_")[0]
        card = parts[0]
        suit = parts[1]


    def GUI(self):

        """
        for player in self.players:

        self.players[player].get("NAME"),
        self.players[player].get("ONE"),
        self.players[player].get("TWO"),
        self.players[player].get("THREE"),
        self.players[player].get("POT_ONE"),
        self.players[player].get("POT_TWO"),
        self.players[player].get("POT_THREE"),
        self.players[player].get("BALANCE"),
        self.players[player].get("PHASE"))
        """
        pass


def main():
    """ Main method """
    end_game = False

    # number_of_players MAX = 5, number_of_decks, table_min
    bj = Blackjack(4, 1, 5)

    while not end_game and bj.round < 10:
        print "\n------------------------\nROUND #{}".format(bj.round)
        bj.rounds()
        bj.init_pot()
        end_round = False

        pprint(bj.players)

        while not end_round:
            # Loop through players
            for player in range(0, bj.number_of_players + 1):
                print "+++++++++++++++"
                if player == 0:
                    bj.dealer_turn()
                else:
                    bj.player_turn(player)

                end_round = bj.round_check()

        if len(bj.deck) < (len(bj.players) + 1) * 3:
            end_game = True

        bj.reset_pots()


#main()
# TEST CASES
#test_card_1 = Card('Diamonds', '4')
#test_card_2 = Card('Clubs', 'Ace')
#test_card_3 = Card('Spades', 'Jack')
#test_card_4 = Card('Hearts', '10')

#print(Card.ascii_version_of_card(test_card_1, test_card_2, test_card_3, test_card_4))
#print(Card.ascii_version_of_hidden_card(test_card_1, test_card_2, test_card_3, test_card_4))
# print(ascii_version_of_hidden_card(test_card_1, test_card_2))

c = Card()
print(c.render_folded_card())
print(c.render_card("1_DIAMONDS_0"))




