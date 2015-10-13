
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
                raise Exception('Not enough {} answers'.format(query.__class__.__name__))
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