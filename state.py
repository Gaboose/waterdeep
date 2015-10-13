from collections import Sequence

from library import Library
from resources import QualityResources
from actions import QuestQuery, IntrigueQuery


class State:

    def __init__(self, players, board):
        self.players = players
        self.board = board


class Player():

    def __init__(self, agentsN, quests, resources):
        self.agentsN = agentsN
        self.quests = quests
        self.resources = resources

    def add(self, resources):
        if isinstance(resources, Sequence):
            for el in resources:
                yield from self.add(el)
            return

        if isinstance(resources, QualityResources):
            for i in range(resources.quests):
                yield QuestQuery(lambda quest: self.quests.append(quest))
            yield from self._add_intrigues(resources.intrigues)
        else:
            self.resources += resources

    def sub(self, resources):
        if isinstance(resources, Sequence):
            for el in resources:
                yield from self.sub(el)
            return

        if isinstance(resources, QualityResources):
            for i in range(resources.quests):
                yield QuestQuery(lambda quest: self.quests.remove(quest))
        else:
            self.resources -= resources


class OpenPlayer(Player):

    def __init__(self, *args, **kwargs):
        self.lord = None
        self.intrigues = []
        super().__init__(*args, **kwargs)

    def _add_intrigues(self, num):
        for i in range(num):
            yield IntrigueQuery(
                lambda intrigue: self.intrigues.append(intrigue))

    def __repr__(self):
        names = ['agentsN', 'quests', 'resources', 'intrigues', 'lord']
        items = ['{}={}'.format(name, getattr(self, name)) for name in names]
        return 'OpenPlayer({})'.format(', '.join(items))


class Opponent(Player):

    def __init__(self, *args, **kwargs):
        self.intriguesN = 0
        super().__init__(*args, **kwargs)

    def _add_intrigues(self, num):
        self.intriguesN += num
        return
        yield

    def __repr__(self):
        names = ['agentsN', 'quests', 'resources', 'intriguesN']
        items = ['{}={}'.format(name, getattr(self, name)) for name in names]
        return 'Opponent({})'.format(', '.join(items))


class Board:

    def __init__(self, buildings_for_sale, quests):
        self.buildings_for_sale = buildings_for_sale
        self.buildings_open = Library.core_buildings
        self.buildings_used = []
        self.quests = quests
