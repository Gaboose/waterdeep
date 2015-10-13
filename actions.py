from copy import deepcopy


class Query:
    pass


class IntrigueQuery(Query):
    pass


class QuestQuery(Query):
    pass


class BuildingQuery(Query):
    pass


def feed(generator, **kwargs):

    state = None

    try:
        query = generator.send(None)
        while True:
            answers = kwargs.get(query.__class__.__name__, [])
            if len(answers) > 0:
                query = generator.send(answers.pop(0))
            else:
                raise Exception('Not enough {} answers'.format(
                    query.__class__.__name__))
    except StopIteration as exception:
        state = exception.value

    if state is None:
        raise Exception('Action did not return a state')
    return state


def run(generator):
    try:
        next(generator)
    except StopIteration as exception:
        return exception.value


class Supply:

    def __init__(self, resources):
        self.resources = resources

    def action(self, actor, state):
        state = deepcopy(state)
        state.players[actor].resources += self.resources
        return state
        yield


class Release:

    def __init__(self, resources):
        self.resources = resources

    def action(self, actor, state):
        state = deepcopy(state)
        state.players[actor].resources -= self.resources
        return state
        yield


class TakeFaceUp:

    def __init__(self, resources):
        self.resources = resources

    def action(self, actor, state):
        state = deepcopy(state)

        for i in range(self.resources.quests):
            quest = yield QuestQuery()
            state.board.quests.remove(quest)
            state.players[actor].quests.append(quest)
            newquest = yield QuestQuery()
            state.board.quests.append(newquest)

        for i in range(self.resources.buildings):
            building = yield BuildingQuery()
            state.board.buildings_for_sale.remove(building)
            building.owner = actor
            state.board.buildings_open.append(building)
            newbuilding = yield BuildingQuery()
            state.board.buildings_for_sale.append(newbuilding)

        return state


class DrawFaceDown:

    def __init__(self, resources):
        self.resources = resources

    def action(self, actor, state):
        state = deepcopy(state)

        for i in range(self.resources.intrigues):
            yield from state.players[actor].draw_intrigue()

        return state
