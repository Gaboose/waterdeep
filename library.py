from copy import deepcopy
from collections import namedtuple, Sequence

from resources import Resources, QualityResources
from actions import BuildingQuery, QuestQuery, IntrigueQuery


def to_dict(sequence, name='Things'):
    """
    :return: namedtuple mapping class names to sums of given elements
    e.g. to_dict((8, 'hello ', 10, 'sun')) == Things(int=18, str='hello sun')
    """

    if not isinstance(sequence, Sequence):
        sequence= (sequence,)
    dct = dict()
    for element in sequence:
        name = element.__class__.__name__
        if name in dct:
            dct[name] += element
        else:
            dct[name] = element
    keys, vals = zip(*dct.items())
    return namedtuple(name, keys)(*vals)


class Named:
    def name(self, name):
        self.name = name
        return self


class Quest(Named):

    def __init__(self, required, reward):
        self.required = required
        self.reward = to_dict(reward)

    def action(self, actor, state):
        state = deepcopy(state)

        yield from state.players[actor].sub(self.required)
        yield from state.players[actor].add((self.reward.Resources,
                                             self.reward.QualityResources.only_facedown()))
        yield from state.board.draw_faceup(self.reward.QualityResources.only_faceup(), state.players[actor])
        return state


class NoopIntrigue(Named):
    def action(owner, state):
        return state


class CoreBuilding(Named):

    def __init__(self, reward):
        self.reward = reward

    def action(self, actor, state):
        state = deepcopy(state)
        yield from state.players[actor].add((self.reward.Resources,
                                             self.reward.QualityResources.only_facedown()))
        yield from state.board.draw_faceup(self.reward.QualityResources.only_faceup(), state.players[actor])
        return state


class CliffwatchInnReset(Named):

    def __init__(self):
        self.name("Cliffwatch Inn (Reset)")

    def action(self, actor, state):
        state = deepcopy(state)
        state.board.quests = []
        for i in range(4):
            quest = yield QuestQuery()
            state.boards.quest.append(quest)

        yield from state.players[actor].add(QualityResources(quests=1))
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
        yield from state.players[actor].add(QualityResources(intrigues=1))
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

    def __init__(self, cost, action_required, action_reward, owner_reward):
        self.cost = cost
        self.action_required = action_required or Resources()
        self.action_reward = to_dict(action_reward)
        self.owner_reward = owner_reward
        self.owner = None

    def action(self, actor, state):
        state = deepcopy(state)

        state.players[actor].resources += self.action_reward['Resources'] - self.action_required
        yield from state.board.draw_faceup(self.action_reward['QualityResources'].only_faceup(), state.players[actor])
        yield from state.players[actor].add_intrigues(self.action_reward['QualityResources'].intrigues)
        yield from state.players[self.owner].add(self.owner_reward)
        return state


class Library:

    quests = [
        Quest(Resources(fighters=3), Resources(vp=6)).name('sample quest')
    ]

    intrigues = [
        NoopIntrigue().name('sample intrigue')
    ]

    core_buildings = [
        CoreBuilding(Resources(gold=4)).name("Aurora's Realms Shop"),
        CoreBuilding(Resources(wizards=1)).name("Blackstaff Tower"),
        CoreBuilding((QualityResources(quests=1), Resources(gold=2))).name("Cliffwatch Inn (Gold)"),
        CoreBuilding(QualityResources(quests=1, intrigues=1)).name("Cliffwatch Inn (Intrigue)"),
        CliffwatchInnReset(),
        BuildersHall(),
        CastleWaterdeep(),
        WaterdeepHarbor(1),
        WaterdeepHarbor(2),
        WaterdeepHarbor(3),
        CoreBuilding(Resources(fighters=2)).name("Field of Triumph"),
        CoreBuilding(Resources(rogues=2)).name("The Grinning Lion Tavern"),
        CoreBuilding(Resources(clerics=1)).name("The Plinth")
    ]

    @classmethod
    def quest(cls, name):
        for item in cls.quests:
            if item.name == name:
                return item