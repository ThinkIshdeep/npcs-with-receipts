import base64, io, json, math, unittest
import numpy as np
from lab.core import astar, clean
from lab import npcs

class CoreTests(unittest.TestCase):

    def test_astar_routes_around_wall(self):
        path = astar([0, 0], [4, 4], [[2, y] for y in range(4)], 5)
        self.assertEqual(path[-1], [4, 4])
        self.assertTrue(all((p[0] != 2 or p[1] == 4 for p in path)))

    def test_astar_impossible(self):
        self.assertEqual(astar([0, 0], [2, 2], [[1, y] for y in range(3)], 3), [])

    def test_json_serialization(self):
        self.assertEqual(clean({'a': np.int64(2), 'b': float('nan')}), {'a': 2, 'b': None})

class SocialTests(unittest.TestCase):

    def test_private_observation(self):
        e = npcs.Engine()
        e.interact({'npc': 0, 'kind': 'borrow'})
        self.assertFalse(e.state['npcs'][2]['memories'])

    def test_money_conservation_and_repay(self):
        e = npcs.Engine()
        total = lambda: e.state['player_money'] + sum((x['money'] for x in e.state['npcs']))
        before = total()
        e.interact({'npc': 0, 'kind': 'borrow'})
        e.interact({'npc': 0, 'kind': 'repay'})
        self.assertEqual(total(), before)
        self.assertEqual(e.state['debts']['0'], 0)

    def test_rumour_provenance(self):
        e = npcs.Engine()
        e.interact({'npc': 0, 'kind': 'borrow'})
        e.advance({})
        m = e.state['npcs'][1]['memories'][0]
        self.assertFalse(m['direct'])
        self.assertEqual(m['source'], 'Mira')
        self.assertLess(m['confidence'], 1)
