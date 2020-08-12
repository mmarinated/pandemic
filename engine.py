from collections import Counter
from cycler import cycle

import qgrid
import pandas as pd

class Board:
    """
    Has 4 methods:
    - add:       if one adds cubes to the city
    - remove:    if one removes cubes from the city
    - draw:      infection step, may pass several cards at once.
                 Calls "remove" automatically.
    - epidemic:  epidemic happens

    list of known cities and number of cubes places should be manually maintained
    in game_setup.py

    See Example.ipynb.
    """
    CARDS_DRAWN_BY_EPIDEMIC_LVL = [2, 2, 2, 3, 3, 4, 4, 5]

    def __init__(self, list_cities_cards_cubes, list_of_players):
        self.list_of_players = cycle(list_of_players)
        # so first draw does not count
        for i in range(len(list_of_players) - 1):
            next(self.list_of_players)

        self.cities = [city for (city, card, cube) in list_cities_cards_cubes]
        cards = [card for (city, card, cube) in list_cities_cards_cubes]
        cubes = [cube for (city, card, cube) in list_cities_cards_cubes]

        self._stack_of_counters = [Counter(dict(zip(self.cities, cards)))]
        self._discarded = Counter()
        self._cubes_by_city = Counter(dict(zip(self.cities, cubes)))
        self._plague_cubes_by_city = Counter()
        self.emergency_level = 0
        self.num_epidemic = 0


    def show_stack(self):
        for c in self._stack_of_counters:
            print([f"{x}: {y}" for x, y in c.most_common() if y > 0])

    @property
    def num_cards_to_draw(self):
        return self.CARDS_DRAWN_BY_EPIDEMIC_LVL[self.num_epidemic]

    @property
    def num_left_cards(self):
        return sum(self._stack_of_counters[-1].values())

    @property
    def left_cards(self):
        return self._stack_of_counters[-1].most_common()

    @property
    def discarded_cards(self):
        return self._discarded.most_common()

    @property
    def plague_cubes(self):
        return self._plague_cubes_by_city.most_common()

    @property
    def cubes(self):
        return self._cubes_by_city.most_common()

    def add(self, city, num=1):
        self._cubes_by_city[city] += num

    def remove(self, city, num=1):
        self._cubes_by_city[city] -= num

        left = self._cubes_by_city[city]
        if left < 0:
            print("Place a plague cube")
            self.emergency_level += 1
            self._cubes_by_city[city] = 0
            self._plague_cubes_by_city[city] += abs(left)

    def epidemic(self, city):
        self.num_epidemic += 1
        self._discard_card(city, 0) # from bottom of stack
        self.remove(city, max(self._cubes_by_city[city], 1))
        self._stack_of_counters.append(self._discarded.copy())
        self._discarded = Counter()

    def draw(self, *cities):
        print(f"{next(self.list_of_players)}'s turn ended.")
        for city in cities:
            self._draw_one(city)

    def _draw_one(self, city):
        self._discard_card(city)
        self.remove(city)

    def _discard_card(self, city, stack_pos=-1):
        self._stack_of_counters[stack_pos][city] -= 1
        self._discarded[city] += 1

        if self.num_left_cards == 0:
            print(f"WARNING: starting drawing 'new' cards")
            self._stack_of_counters.pop()

    def get_city_stats(self, city):
        """
        Returns
        -------
        city, cubes, cards_on_top, prob_of_being_drawing
        """
        cubes = self._cubes_by_city[city]
        cards_on_top = self._stack_of_counters[-1][city]
        prob_of_being_drawing = self.num_cards_to_draw * cards_on_top / self.num_left_cards
        prob_of_being_drawing = min(prob_of_being_drawing, cards_on_top)
        failure_chance = prob_of_being_drawing - cubes
        discarded = self._discarded[city]

        try:
            next_stack = self._stack_of_counters[-2][city]
        except:
            next_stack = 0

        return [city, cubes, cards_on_top, prob_of_being_drawing,
                failure_chance, discarded, next_stack]

    def __call__(self):
        list_stats = [self.get_city_stats(city) for city in self.cities]
        columns = ['city', 'cubes', 'cards_on_top', 'prob_of_being_drawing',
                   'failure_chance', 'discarded', 'next_stack']
        df = pd.DataFrame(list_stats, columns=columns)

        df.index, df.index.name = df['city'], "City"
        df.drop(columns="city", inplace=True)

        df = df[['failure_chance', 'prob_of_being_drawing', 'cards_on_top',
                 'cubes', 'discarded', 'next_stack']]
        df.sort_values(by=['failure_chance', 'cards_on_top'], ascending=False, inplace=True)

        return qgrid.show_grid(df, precision=2)
