from copy import deepcopy
from resources import Resources


class Named:
    def name(self, name):
        self.name = name
        return self


class Quest(Named):

    def __init__(self, required, reward):
        self.required = required
        self.reward = reward

    def action(self, actor, state):
        state = deepcopy(state)
        yield from state.players[actor].sub(self.required)
        yield from state.players[actor].add(self.reward)
        yield state


class NoopIntrigue(Named):
    def action(owner, state):
        return state


class CoreBuilding(Named):

    def __init__(self, reward):
        self.reward = reward

    def action(self, actor, state):
        state = deepcopy(state)
        yield from state.players[actor].add(self.reward)
        return state


class Building(Named):

    def __init__(self, cost, action_required, action_reward, owner_reward):
        self.cost = cost
        self.action_required = action_required or Resources()
        self.action_reward = action_reward
        self.owner_reward = owner_reward
        self.owner = None

    def action(self, actor, state):
        state = deepcopy(state)
        yield from state.players[actor].sub(self.action_required)
        yield from state.players[actor].add(self.action_reward)
        if self.owner is not None:
            yield from state.players[self.owner].add(self.owner_reward)
        yield state


class Library:

    quests = [
        Quest(Resources(fighters=3), Resources(vp=6)).name('sample quest')
    ]

    intrigues = [
        NoopIntrigue().name('sample intrigue')
    ]

    core_buildings = [
        CoreBuilding(Resources(fighters=2)).name('fighters')
    ]

    @classmethod
    def quest(cls, name):
        for item in cls.quests:
            if item.name == name:
                return item
