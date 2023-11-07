# HSLU
#
# Created by Thivaan Kandasamy on 11/01/2023
#
import logging
import numpy as np
from jass.agents.agent import Agent
from jass.game.const import PUSH, MAX_TRUMP, card_strings, color_of_card, offset_of_card, OBE_ABE, UNE_UFE, CLUBS, \
    SPADES, HEARTS, DIAMONDS, J_offset, A_offset, K_offset, trump_strings_german_long, card_values
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber


class AgentMinmax(Agent):
    """
    Randomly select actions for the game of jass (Schieber)
    """

    def __init__(self):
        # log actions
        self._logger = logging.getLogger(__name__)
        # self._logger.setLevel(logging.INFO)
        # Use rule object to determine valid actions
        self._rule = RuleSchieber()
        # init random number generator
        self._rng = np.random.default_rng()

    def action_trump(self, obs: GameState) -> int:
        """
        Select trump randomly. Pushing is selected with probability 0.5 if possible.
        Args:
            obs: the current game
        Returns:
            trump action
        """
        self._logger.info('Trump request')
        # Variables
        cards = []
        cards_as_string = []
        counter = 0
        diamond_hand_cards = []
        heart_hand_cards = []
        spades_hand_cards = []
        clover_hand_cards = []
        obeabe_hand_cards = []
        uneufe_hand_cards = []

        # Sort Card Hand Types
        for card_id in obs.hand:
            if card_id == 1:
                cards.append(counter)
                cards_as_string.append(card_strings[counter])
                # Count number of typ which your hand has
                if color_of_card[counter] == 0:
                    diamond_hand_cards.append(counter)
                elif color_of_card[counter] == 1:
                    heart_hand_cards.append(counter)
                elif color_of_card[counter] == 2:
                    spades_hand_cards.append(counter)
                elif color_of_card[counter] == 3:
                    clover_hand_cards.append(counter)
                # Count best number of obeabe [Ass,King,Queen,Bube]
                if offset_of_card[counter] in [0, 1, 2, 3]:
                    obeabe_hand_cards.append(counter)
                    # obe_ct = obe_ct + 1
                # Count best number of uneufe [8,7,6]
                if offset_of_card[counter] in [6, 7, 8]:
                    uneufe_hand_cards.append(counter)
                    # une_ct = une_ct + 1
            counter = counter + 1

        #### Rules to Decide which trump we are going to use

        # Determine if obeabe or ofeobe is worth it.
        if len(obeabe_hand_cards) > 6:
            self._logger.info('Result: {}'.format(OBE_ABE))
            return OBE_ABE
        if len(uneufe_hand_cards) > 6:
            self._logger.info('Result: {}'.format(UNE_UFE))
            return UNE_UFE

        # Determine best card_color
        hand_values = {'diamonds': diamond_hand_cards, 'hearts': heart_hand_cards,
                       'spades': spades_hand_cards, 'clubs': clover_hand_cards}

        best_color_card_amount = 0
        best_color_cards = []
        for key in hand_values:
            current_amount = len(hand_values[key])
            if best_color_card_amount < current_amount:
                best_color_card_amount = current_amount
                best_color_cards = [key]  # Rest best_color_cards

            elif best_color_card_amount == current_amount:
                best_color_cards.append(key)

        # in case of two or more card types, determine which is more worth it.
        if len(best_color_cards) > 1:
            color_card_amountlist = []
            for color_name in best_color_cards:
                color_cards = hand_values[color_name]
                totalamount = 0
                for color_card in color_cards:
                    totalamount = totalamount + offset_of_card[color_card]
                color_card_amountlist.append(totalamount)
            best_amount_min = min(color_card_amountlist)  # Determin Value due to amount min
            winner_color = best_color_cards[color_card_amountlist.index(best_amount_min)]
        else:
            winner_color = best_color_cards[0]

        if obs.forehand == -1:
            # Determine if we should PUSH.
            totalamount = 0
            strongcard = 0
            for card_items in hand_values[winner_color]:
                if offset_of_card[card_items] in [J_offset, A_offset, K_offset]:
                    strongcard = strongcard + 1
                totalamount = totalamount + offset_of_card[card_items]

            if strongcard < 1:
                self._logger.info('Result: {}'.format(PUSH))
                return PUSH

        if winner_color == "diamonds":
            result = DIAMONDS
        elif winner_color == "hearts":
            result = HEARTS
        elif winner_color == "spades":
            result = SPADES
        else:
            result = CLUBS

        self._logger.info('Result: {}'.format(result))
        return result

    def action_play_card(self, obs: GameState) -> int:
        """
        Select highest card from the valid cards
        Args:
            obs: The observation of the jass game for the current player
        Returns:
            card to play
        """
        self._logger.info('Card request')
        # cards are one hot encoded
        valid_cards = self._rule.get_valid_cards_from_obs(obs)
        cards = []
        cards_as_string = []
        cards_valuelist = []  # Determine value of Card
        counter = 0
        trumpf = trump_strings_german_long[obs.trump]

        # Get Informations of all valid hand cards
        for card_id in valid_cards:
            if card_id == 1:
                cards.append(counter)
                cards_as_string.append(card_strings[counter])
                cards_valuelist.append(card_values[obs.trump][counter])
            counter = counter + 1
        ### Chose a card

        # Chose highest Card first
        highest_cardvalue = max(cards_valuelist)
        card = cards[cards_valuelist.index(highest_cardvalue)]

        self._logger.info('Played card: {}'.format(card_strings[card]))
        return card
