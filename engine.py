from collections import Counter
from cycler      import cycle

import qgrid
import pandas as pd

class Board:
    """
    Has 4 methods:
    - add:          if one adds cubes to the city
    - remove:       if one removes cubes from the city
    - draw:         infection step, may pass several cards at once.
                    Calls "remove" automatically.
    - epidemic:     epidemic happens
    - move:         move from one city to an adjacent (free acvtion)
    - draw_hollow:  cities that are drawn after "hollow man" card is draws
    - inoculate:    performs incoluate action for *infection* cards.

    list of known cities and number of cubes places should be manually maintained
    in game_setup.py

    See Example.ipynb.
    """
    CARDS_DRAWN_BY_EPIDEMIC_LVL = [2, 2, 2, 3, 3, 4, 4, 5]

    def __init__(self, list_cities_cards_cubes,
                 list_of_players, num_events_cards,
                 num_produce_supplies=7, num_portable_lab=3,
                 has_found_jade=True):
        self.list_of_players = cycle(list_of_players)
        self.has_found_jade = has_found_jade

        cities = [city for (city, good, card, cube) in list_cities_cards_cubes]
        good   = [good for (city, good, card, cube) in list_cities_cards_cubes]
        cards  = [card for (city, good, card, cube) in list_cities_cards_cubes]
        cubes  = [cube for (city, good, card, cube) in list_cities_cards_cubes]

        self.num_good_cards = sum(good)
        self.num_epidemic_cards = _detect_number_of_epidemics(self.num_good_cards)
        print(f"Num good cards: {self.num_good_cards}, "
              f"num_epidemic: {self.num_epidemic_cards}")
        self.num_good_cards += (num_events_cards + num_produce_supplies + num_portable_lab)
        self._till_epidemic = self.num_good_cards // self.num_epidemic_cards
        self.counter_till_epidemic = self._till_epidemic

        self.cities = cities
        self._num_cards_by_city = Counter(dict(zip(self.cities, cards)))
        self._stack_of_counters = [Counter(dict(zip(self.cities, cards)))]
        self._discarded = Counter()
        self._cubes_by_city = Counter(dict(zip(self.cities, cubes)))
        self._plague_cubes_by_city = Counter()
        self.emergency_level = 0
        self.num_epidemic = 0
        self._is_first_move = True

        self.inoculated_cards = Counter()
        self.hollowed_cities = Counter()


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

    def move(self, from_city, to_city, num=1):
        self.remove(from_city, num=num)
        self.add(to_city, num=num)

    def epidemic(self, city):
        self.num_epidemic += 1
        self.counter_till_epidemic += self._till_epidemic
        self._discard_card(city, 0) # from bottom of stack
        num_draw = 1 if self.has_found_jade else max(self._cubes_by_city[city], 1)
        self.remove(city, num_draw)
        self._stack_of_counters.append(self._discarded.copy())
        self._discarded = Counter()

    def draw(self, *cities):
        if not self._is_first_move:
            print(f"{next(self.list_of_players)}'s turn ended.")
            self.num_good_cards -= len(cities)
            self.counter_till_epidemic -= len(cities)

        self._is_first_move = False

        for city in cities:
            self._draw_one(city)

    def draw_hollow(self, *cities):
        for city in cities:
            self._draw_one_hollow(city)

    def _draw_one_hollow(self, city):
        self._discard_card(city)
        self.hollowed_cities[city] += 1

    def inoculate(self, city, num=1, from_discarded=True):
        if from_discarded:
            assert self._discarded[city] >= num
            self._discarded[city] -= num
        else:
            assert self._stack_of_counters[-1][city] >= num
            self._stack_of_counters[-1][city] -= num

        self.inoculated_cards[city] += num

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
        next_stack = self._stack_of_counters[-2][city] if len(self._stack_of_counters) >= 2 else 0
        num_total = self._num_cards_by_city[city] - self.inoculated_cards[city]

        return [city, cubes, cards_on_top, prob_of_being_drawing,
                failure_chance, discarded, next_stack, num_total]

    def __call__(self):
        print(f"Cards till epidemic: {self.counter_till_epidemic}.")
        list_stats = [self.get_city_stats(city) for city in self.cities]
        columns = ['city', 'cubes', 'cards_on_top', 'prob_of_being_drawing',
                   'failure_chance', 'discarded', 'next_stack', 'num_total']
        df = pd.DataFrame(list_stats, columns=columns)
        df = df[df['num_total'] > 0]

        df.index, df.index.name = df['city'], "City"
        df.drop(columns="city", inplace=True)

        df = df[['failure_chance', 'prob_of_being_drawing', 'cards_on_top',
                 'cubes', 'discarded', 'next_stack', 'num_total']]
        df.sort_values(by=['failure_chance', 'cards_on_top'], ascending=False, inplace=True)

        return qgrid.show_grid(df, precision=2)



def _detect_number_of_epidemics(num_cards):
    if num_cards <= 36:
        return 5
    elif num_cards <= 44:
        return 6
    elif num_cards <= 51:
        return 7
    elif num_cards <= 57:
        return 8
    elif num_cards <= 62:
        return 9
    else:
        return 10
