# city - num good cards - num_bad_cards - num_cubes_placed
LIST_CITIES_CARDS_CUBES = [
    ('tripoli',       4, 3, 3),
    ('istanbul',      4, 3, 3),
    ('cairo',         4, 3, 2),

    ('new_york',      4, 3, 3),
    ('washington',    4, 3, 3),
    ('jacksonville',  4, 3, 3),
    ('chicago',       2, 2, 2),
    ('atlanta',       1, 1, 1),
    ('denver',        2, 2, 2),
    ('los_angeles',   1, 1, 1),
    ('san_francisco', 2, 2, 2),
    ('mexico_city',   1, 1, 0),

    ('london',        4, 3, 3),
    ('paris',         2, 2, 2),
    ('frankfurt',     2, 2, 2),
    ('st_peterburg',  1, 1, 1),
    ('moscow',        1, 1, 0),

    ('sao_paolo',     4, 3, 3),
    ('buenos_aires',  2, 2, 2),
    ('lima',          1, 1, 1),
    ('bogota',        2, 2, 2),
    ('santiago',      1, 1, 1),

    ('lagos',         4, 3, 3),
]

###
## Helpers
###

def CHECK_SETUP_CORRECTNESS(num_cubes, LIST_CITIES_CARDS_CUBES):
    _sum_cubes = sum(cube for _, _, _, cube in LIST_CITIES_CARDS_CUBES)
    assert _sum_cubes == num_cubes, _sum_cubes


def SET_CITIES_AS_VARIABLES(LIST_CITIES_CARDS_CUBES, globals_dict):
    """
    Adds cities in LIST_CITIES_CARDS_CUBES to globals().
    Useful so you can type chicago with autocomlete instead of 'chicago'
    """
    for city, _, _, _ in LIST_CITIES_CARDS_CUBES:
        globals_dict[city] = city
