import copy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .core import Base

class Engine(Base):
    actions = Base.actions | {'interact', 'advance', 'search'}

    def __init__(self):
        super().__init__()
        self.reset({})

    def reset(self, p):
        names = ['Mira', 'Kabir', 'Zoya', 'Dev', 'Anya', 'Rafi', 'Tara', 'Neel']
        roles = ['Shopkeeper', 'Mechanic', 'Librarian', 'Baker', 'Gardener', 'Courier', 'Artist', 'Teacher']
        self.state = {'day': 1, 'player_money': 100, 'debts': {}, 'events': [], 'npcs': [{'id': i, 'name': n, 'role': roles[i], 'money': 150, 'trust': 50, 'location': i % 4, 'memories': [], 'beliefs': {}, 'goal': ['Earn money', 'Help a friend', 'Keep a promise'][i % 3]} for i, n in enumerate(names)], 'last_result': None}

    def event(self, text, observers, kind, subject=None):
        e = {'id': len(self.state['events']) + 1, 'day': self.state['day'], 'text': text, 'kind': kind, 'subject': subject, 'observers': observers}
        self.state['events'].append(e)
        for i in observers:
            n = self.state['npcs'][i]
            n['memories'].append({'event_id': e['id'], 'text': text, 'source': n['name'], 'direct': True, 'day': self.state['day'], 'confidence': 1.0})
        return e

    def interact(self, p):
        i = int(p.get('npc', 0))
        if not 0 <= i < 8:
            raise ValueError('Select an NPC')
        n = self.state['npcs'][i]
        kind = p.get('kind', 'talk')
        key = str(i)
        debt = self.state['debts'].get(key, 0)
        if kind == 'borrow':
            if debt:
                raise ValueError('Repay the existing loan first')
            if n['trust'] < 35 or n['money'] < 30:
                return {'dialogue': f"{n['name']}: I need stronger reasons to lend right now."}
            n['money'] -= 30
            self.state['player_money'] += 30
            self.state['debts'][key] = 30
            text = f"Player borrowed 30 coins from {n['name']}."
        elif kind == 'repay':
            if not debt:
                raise ValueError('No outstanding debt to this character')
            if self.state['player_money'] < debt:
                raise ValueError('Not enough coins')
            n['money'] += debt
            self.state['player_money'] -= debt
            self.state['debts'][key] = 0
            n['trust'] = min(100, n['trust'] + 15)
            text = f"Player repaid the debt to {n['name']}."
        elif kind == 'help':
            n['trust'] = min(100, n['trust'] + 8)
            text = f"Player helped {n['name']} with a delivery."
        else:
            mem = n['memories'][-1]['text'] if n['memories'] else 'We have not had much history yet.'
            return {'dialogue': f"{n['name']}: {mem} My goal today is: {n['goal'].lower()}."}
        self.event(text, [i], kind, i)
        return {'dialogue': f"{n['name']}: " + ('We are square. I appreciate it.' if kind == 'repay' else 'I will remember that.')}

    def advance(self, p):
        self.state['day'] += 1
        day = self.state['day']
        old = copy.deepcopy(self.state['npcs'])
        for n in self.state['npcs']:
            n['location'] = (n['id'] + day) % 4
            debt = self.state['debts'].get(str(n['id']), 0)
            if debt:
                n['trust'] = max(0, n['trust'] - 5)
                self.event(f"Player still owes {n['name']} {debt} coins on day {day}.", [n['id']], 'overdue', n['id'])
            source = old[(n['id'] - 1) % 8]
            if source['memories']:
                m = source['memories'][-1]
                conf = m['confidence'] * 0.8
                if not any((x['event_id'] == m['event_id'] for x in n['memories'])):
                    n['memories'].append(dict(m, source=source['name'], direct=False, confidence=round(conf, 3)))
                    n['beliefs'][str(m['event_id'])] = {'confidence': round(conf, 3), 'heard_from': source['name']}
                    ev = next((x for x in self.state['events'] if x['id'] == m['event_id']))
                    if ev['kind'] == 'overdue':
                        n['trust'] = max(0, n['trust'] - round(4 * conf))
                    if ev['kind'] == 'repay':
                        n['trust'] = min(100, n['trust'] + round(4 * conf))
        return {'day': day, 'note': 'Only neighbour-to-neighbour memories propagate once per day; rumours remain sourced beliefs.'}

    def search(self, p):
        n = self.state['npcs'][int(p.get('npc', 0))]
        mem = n['memories']
        q = str(p.get('query', 'debt'))
        if not mem:
            return {'matches': []}
        vec = TfidfVectorizer().fit([x['text'] for x in mem] + [q])
        sc = cosine_similarity(vec.transform([q]), vec.transform([x['text'] for x in mem]))[0]
        return {'matches': [dict(mem[int(i)], score=float(sc[i])) for i in sc.argsort()[::-1][:5]]}

    def evaluate(self, p):
        e = Engine()
        start = e.state['player_money'] + sum((n['money'] for n in e.state['npcs']))
        e.interact({'npc': 0, 'kind': 'borrow'})
        private = all((not n['memories'] for n in e.state['npcs'][1:]))
        e.advance({})
        first = len(e.state['npcs'][1]['memories']) > 0
        far = not e.state['npcs'][4]['memories']
        e.interact({'npc': 0, 'kind': 'repay'})
        end = e.state['player_money'] + sum((n['money'] for n in e.state['npcs']))
        out = {'checks': {'private_observation': private, 'one_hop_rumour': first, 'distant_character_unaware': far, 'coin_conservation': start == end, 'debt_repaid': e.state['debts']['0'] == 0}, 'note': 'Deterministic world invariants; believability requires a human study.'}
        self.state['last_result'] = out
        return out
