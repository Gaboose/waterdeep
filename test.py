import unittest

from state import Board, State, Player, OpenPlayer, Opponent
from resources import Resources, QualityResources
from library import Quest, Building, NoopIntrigue
import actions


class MyTestCase(unittest.TestCase):

    def test_resources(self):
        r = Resources(fighters=5) + Resources(wizards=3)
        r += Resources(clerics=3) + Resources() - Resources(fighters=1)
        self.assertEqual([r.fighters, r.wizards, r.clerics], [4, 3, 3])


    def test_quest(self):
        s = State({'red': Player(4, [], Resources())}, Board([], []))
        q = Quest(Resources(fighters=3), Resources(vp=6))

        s = actions.run(q.action('red', s))

        r = s.players['red'].resources
        self.assertEqual([r.fighters, r.vp], [-3, 6])


    def test_building(self):
        players = {'red': OpenPlayer(4, [], Resources()),
                   'blue': Opponent(4, [], Resources())}
        s = State(players, Board([], []))
        b = Building(5, None,
                     Resources(wizards=3),
                     (Resources(clerics=2), QualityResources(intrigues=1)))
        b.owner = 'blue'

        s = actions.run(b.action('red', s))

        self.assertEqual([s.players['red'].resources.wizards,
                          s.players['blue'].resources.clerics,
                          s.players['blue'].intriguesN], [3, 2, 1])


    def test_quest_query(self):
        s = State({'red': OpenPlayer(4, [], Resources())}, Board([], []))
        q = Quest(Resources(fighters=3), QualityResources(quests=1))

        s = actions.feed(q.action('red', s), QuestQuery=[Quest(None, None).name("Reward Quest")])

        p = s.players['red']
        self.assertEqual(p.resources.fighters, -3)
        self.assertEqual({quest.name for quest in p.quests}, {"Reward Quest"})


    def test_query_feed(self):
        s = State({'red': OpenPlayer(4, [], Resources())}, Board([], []))
        q = Quest(Resources(), QualityResources(quests=2, intrigues=1))

        s = actions.feed(q.action('red', s), QuestQuery=[Quest(None, None).name("Reward Quest"),
                                                         Quest(None, None).name("Reward Quest2")],
                                             IntrigueQuery=[NoopIntrigue().name("Reward Intrigue")])

        p = s.players['red']
        self.assertEqual({quest.name for quest in p.quests}, {"Reward Quest", "Reward Quest2"})
        self.assertEqual({intrigue.name for intrigue in p.intrigues}, {"Reward Intrigue"})
        pass


if __name__ == '__main__':
    unittest.main()
