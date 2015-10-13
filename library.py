from copy import deepcopy

from resources import Resources, QualityResources
from actions import BuildingQuery, QuestQuery, IntrigueQuery
from actions import Supply, Release, TakeFaceUp, DrawFaceDown


class Named:
    def name(self, name):
        self.name = name
        return self

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '({}="{}")'.format(self.__class__.__name__, self.name)


class Quest(Named):

    def __init__(self, *actions):
        self.actions = actions

    def action(self, actor, state):
        for action in self.actions:
            state = yield from action.action(actor, state)
        return state


class NoopIntrigue(Named):
    def action(actor, state):
        return state
        yield


class CoreBuilding(Named):

    def __init__(self, *actions):
        self.actions = actions

    def action(self, actor, state):
        for action in self.actions:
            state = yield from action.action(actor, state)
        return state


class CliffwatchInnReset(Named):

    def __init__(self):
        self.name("Cliffwatch Inn (Reset)")

    def action(self, actor, state):
        state = deepcopy(state)
        state.board.quests = []
        for i in range(4):
            quest = yield QuestQuery()
            state.board.quests.append(quest)

        state = yield from TakeFaceUp(QualityResources(quests=1)).action(actor, state)
        return state


class BuildersHall(Named):

    def __init__(self):
        self.name("Builder's Hall")

    def action(self, actor, state):
        state = deepcopy(state)
        building = yield BuildingQuery()
        state.players[actor].resources -= Resources(gold=building.cost)
        building = deepcopy(building)
        building.owner = actor
        state.board.buildings_open.append(building)
        return state


class CastleWaterdeep(Named):

    def __init__(self):
        self.name("Castle Waterdeep")

    def action(self, actor, state):
        state = deepcopy(state)
        state.board.tower_owner = actor
        state = yield from DrawFaceDown(QualityResources(intrigues=1)).action(actor, state)
        return state


class WaterdeepHarbor(Named):

    def __init__(self, i):
        self.name("Waterdeep Harbor {}".format(i))

    def action(self, actor, state):
        intrigue = IntrigueQuery()
        state = yield from intrigue.action(actor, state)
        state.players[actor].remove_intrigue(intrigue)
        return state


class Building(Named):

    def __init__(self, cost, actions, owner_actions):
        self.cost = cost
        self.actions = actions
        self.owner_actions = owner_actions

        self.owner = None

    def action(self, actor, state):
        for action in self.actions:
            state = yield from action.action(actor, state)
        for action in self.owner_actions:
            state = yield from action.action(self.owner, state)

        return state


class Library:

    quests = [
        Quest(Supply(Resources(fighters=3)), Supply(Resources(vp=6))).name('sample quest')
    ]

    intrigues = [
        NoopIntrigue().name('sample intrigue')
    ]

    core_buildings = [
        CoreBuilding(Supply(Resources(gold=4))).name("Aurora's Realms Shop"),
        CoreBuilding(Supply(Resources(wizards=1))).name("Blackstaff Tower"),
        CoreBuilding(TakeFaceUp(QualityResources(quests=1)),
                     Supply(Resources(gold=2))).name("Cliffwatch Inn (Gold)"),
        CoreBuilding(TakeFaceUp(QualityResources(quests=1)),
                     DrawFaceDown(QualityResources(intrigues=1))).name("Cliffwatch Inn (Intrigue)"),
        CliffwatchInnReset(),
        BuildersHall(),
        CastleWaterdeep(),
        WaterdeepHarbor(1),
        WaterdeepHarbor(2),
        WaterdeepHarbor(3),
        CoreBuilding(Supply(Resources(fighters=2))).name("Field of Triumph"),
        CoreBuilding(Supply(Resources(rogues=2))).name("The Grinning Lion Tavern"),
        CoreBuilding(Supply(Resources(clerics=1))).name("The Plinth")
    ]

    @classmethod
    def quest(cls, name):
        for item in cls.quests:
            if item.name == name:
                return item
