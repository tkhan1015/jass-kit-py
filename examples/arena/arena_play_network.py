# HSLU
#
# Created by Thomas Koller on 7/28/2020
#

import logging

from jass.agents.agent_by_network import AgentByNetwork
from jass.agents.agent_ex1 import AgentEx1
from jass.arena.arena import Arena
from jass.agents.agent_random_schieber import AgentRandomSchieber


def main():
    # Set the global logging level (Set to debug or info to see more messages)
    logging.basicConfig(level=logging.INFO)

    # setup the arena
    arena = Arena(nr_games_to_play=1)
    player = AgentEx1()
    # my_player = AgentByNetwork('http://localhost:5000/random')
    my_player = AgentByNetwork('https://lg3bsb3a96.execute-api.eu-central-1.amazonaws.com/dev/random')

    arena.set_players(my_player, player, my_player, player)
    print('Playing {} games'.format(arena.nr_games_to_play))
    arena.play_all_games()
    print('Average Points Team 0: {:.2f})'.format(arena.points_team_0.mean()))
    print('Average Points Team 1: {:.2f})'.format(arena.points_team_1.mean()))


if __name__ == '__main__':
    main()
