import unittest

from state import Board, State, Player, OpenPlayer, Opponent
from resources import Resources, QualityResources
import library
from library import Quest, Building, NoopIntrigue
import actions
from actions import Supply, Release, DrawFaceDown, TakeFaceUp


class Basic(unittest.TestCase):

    def test_resources(self):
        r = Resources(fighters=5) + Resources(wizards=3)
        r += Resources(clerics=3) + Resources() - Resources(fighters=1)
        self.assertEqual([r.fighters, r.wizards, r.clerics], [4, 3, 3])

    def test_quest(self):
        s = State({'red': Player()})
        q = Quest(Release(Resources(fighters=3)), Supply(Resources(vp=6)))

        s = actions.run(q.action('red', s))

        r = s.players['red'].resources
        self.assertEqual([r.fighters, r.vp], [-3, 6])

    def test_building(self):
        players = {'red': OpenPlayer(4),
                   'blue': Opponent(4)}
        s = State(players)
        b = Building(5, [Supply(Resources(wizards=3))],
                     [Supply(Resources(clerics=2)),
                      DrawFaceDown(QualityResources(intrigues=1))])
        b.owner = 'blue'

        s = actions.run(b.action('red', s))

        self.assertEqual([s.players['red'].resources.wizards,
                          s.players['blue'].resources.clerics,
                          s.players['blue'].intriguesN], [3, 2, 1])

    def test_quest_query(self):
        s = State({'red': OpenPlayer()}, Board(quests=[Quest().name("Reward")]))
        q = Quest(Release(Resources(fighters=3)),
                  TakeFaceUp(QualityResources(quests=1)))

        s = actions.feed(q.action('red', s),
                         QuestQuery=[Quest().name("Reward"),
                                     Quest().name("New")])

        p = s.players['red']
        self.assertEqual(p.resources.fighters, -3)
        self.assertEqual({quest.name for quest in p.quests}, {"Reward"})
        self.assertIn("New", {quest.name for quest in s.board.quests})

    def test_query_feed(self):
        quests_on_board = [Quest().name("Reward"), Quest().name("Reward2")]

        s = State({'red': OpenPlayer(4)},
                  Board(quests=[Quest().name("Reward"),
                                Quest().name("Reward2")]))
        q = Quest(TakeFaceUp(QualityResources(quests=2)),
                  DrawFaceDown(QualityResources(intrigues=1)))

        s = actions.feed(q.action('red', s), QuestQuery=[Quest().name("Reward"),
                                                         Quest().name("New"),
                                                         Quest().name("Reward2"),
                                                         Quest().name("New2")],
                                             IntrigueQuery=[NoopIntrigue().name("Reward3")])

        p = s.players['red']
        self.assertEqual({quest.name for quest in p.quests}, {"Reward", "Reward2"})
        self.assertEqual({intrigue.name for intrigue in p.intrigues}, {"Reward3"})
        self.assertIn("New", {quest.name for quest in s.board.quests})
        self.assertIn("New2", {quest.name for quest in s.board.quests})
        pass


class Buildings(unittest.TestCase):

    def test_cliffwatch_inn_reset(self):
        quests = [Quest().name('B{}'.format(i)) for i in range(9)]
        s = State({'red': Player()}, Board(quests=quests[:4]))

        s = actions.feed(library.CliffwatchInnReset().action('red', s),
                         QuestQuery=quests[4:8] + quests[7:])

        p = s.players['red']
        self.assertEqual({quests[7]}, set(p.quests))
        self.assertEqual(set(quests[4:7] + [quests[8]]), set(s.board.quests))


if __name__ == '__main__':
    unittest.main()
