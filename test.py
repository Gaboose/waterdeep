from state import Board, State, Player, OpenPlayer, Opponent
from resources import Resources, QualityResources
from library import Quest, Building
from queries import QuestQuery


def test_resources():
    a = Resources(fighters=5) + Resources(wizards=3)
    a += Resources(clerics=3) + Resources() - Resources(fighters=1)
    return a


def test_board():
    a = Board([], [])
    return a


def test_quest():
    s = State({'red': Player(4, [], Resources())}, Board([], []))
    q = Quest(Resources(fighters=3), Resources(vp=6))

    for query in q.action('red', s):
        if isinstance(query, State):
            s = query
            break

    return s.players['red'].resources


def test_quest_query():
    s = State({'red': OpenPlayer(4, [], Resources())}, Board([], []))
    q = Quest(Resources(fighters=3), QualityResources(quests=1))

    for query in q.action('red', s):
        if isinstance(query, QuestQuery):
            query.answer(Quest(None, None))
        elif isinstance(query, State):
            s = query
            break

    return s.players['red'].resources, s.players['red'].quests


def test_building():
    players = {'red': OpenPlayer(4, [], Resources()),
               'blue': Opponent(4, [], Resources())}
    s = State(players, Board([], []))
    b = Building(5, None,
                 Resources(wizards=1),
                 (Resources(clerics=1), QualityResources(intrigues=1))
                 ).name('Dragon Tower')
    b.owner = 'blue'

    for query in b.action('red', s):
        if isinstance(query, State):
            s = query
            break

    return s.players


def test_query_feed():
    # TODO: a wrapper for action generators to automatically feed in answers to
    # queries to use in tests.
    pass
