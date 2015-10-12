
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
