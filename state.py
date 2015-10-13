from collections import Sequence

from library import Library
from resources import Resources, QualityResources
from actions import QuestQuery, IntrigueQuery


class Board:

    def __init__(self, buildings_for_sale=[], quests=[], tower_owner=None):
        self.buildings_for_sale = buildings_for_sale
        self.buildings_open = Library.core_buildings
        self.buildings_used = []
        self.quests = quests
        self.tower_owner = tower_owner

    def draw_faceup(self, resources, player):
        for i in range(resources.quests):
            quest = yield QuestQuery()
            self.quests.remove(quest)
            player.quests.append(quest)
            newquest = yield QuestQuery()
            self.quests.append(newquest)


        for i in range(resources.buildings):
            building = yield BuildingQuery()
            self.buildings_for_sale.remove(building)
            self.buildings_open.append(building)
            newbuilding = yield BuildingQuery()
            self.buildings_for_sale.append(newbuilding)


class State:

    def __init__(self, players={}, board=Board()):
        self.players = players
        self.board = board


class Player():

    def __init__(self, agentsN=0, quests=[], resources=Resources()):
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
                quest = yield QuestQuery()
                self.quests.append(quest)
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
                quest = yield QuestQuery()
                self.quests.remove(quest)
        else:
            self.resources -= resources


class OpenPlayer(Player):

    def __init__(self, *args, **kwargs):
        self.lord = None
        self.intrigues = []
        super().__init__(*args, **kwargs)

    def remove_intrigue(self, intrigue):
        self.intrigues.remove(intrigue)

    def _add_intrigues(self, num):
        for i in range(num):
            intrigue = yield IntrigueQuery()
            self.intrigues.append(intrigue)

    def __repr__(self):
        names = ['agentsN', 'quests', 'resources', 'intrigues', 'lord']
        items = ['{}={}'.format(name, getattr(self, name)) for name in names]
        return 'OpenPlayer({})'.format(', '.join(items))


class Opponent(Player):

    def __init__(self, *args, **kwargs):
        self.intriguesN = 0
        super().__init__(*args, **kwargs)

    def remove_intrigue(self, intrigue):
        self.intriguesN -= 1

    def _add_intrigues(self, num):
        self.intriguesN += num
        return
        yield

    def __repr__(self):
        names = ['agentsN', 'quests', 'resources', 'intriguesN']
        items = ['{}={}'.format(name, getattr(self, name)) for name in names]
        return 'Opponent({})'.format(', '.join(items))
