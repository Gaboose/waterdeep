
class Query:

    def __init__(self, callback):
        self.callback = callback

    def answer(self, element):
        self.callback(element)


class IntrigueQuery(Query):
    pass


class QuestQuery(Query):
    pass


class BuildingQuery(Query):
    pass


def feed(generator, **kwargs):
    for query in generator:
        answers = kwargs.get(query.__class__.__name__, [])
        if len(answers) > 0:
            query.answer(answers.pop(0))
        else:
            return query


def run(generator):
    for query in generator:
        return query