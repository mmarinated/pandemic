# city - num_bad_cards - num_cubes_placed
LIST_CITIES_CARDS_CUBES = [
    ('tripoli',       3, 3),
    ('istanbul',      3, 3),
    ('cairo',         3, 3),
    ('london',        3, 3),

    ('lagos',         3, 2),
    ('sao_paolo',     3, 2),

    ('new_york',      3, 2),
    ('washington',    3, 2),
    ('jacksonville',  3, 2),

    ('chicago',       2, 2),
    ('atlanta',       1, 1),
    ('denver',        2, 2),
    ('los_angeles',   1, 1),
    ('san_francisco', 2, 2),
    ('paris',         2, 0),
#     ('mexico',     1, 0),
#     ('frankfurt',     2, 0),
#     ('st_peterburg',  1, 0),
#     ('moscow',     1, 0),

]

###
## Helpers
###

def CHECK_SETUP_CORRECTNESS(num_cubes, LIST_CITIES_CARDS_CUBES):
    _sum_cubes = sum(cube for _, _, cube in LIST_CITIES_CARDS_CUBES)
    assert _sum_cubes == num_cubes, _sum_cubes


def SET_CITIES_AS_VARIABLES(LIST_CITIES_CARDS_CUBES, globals_dict):
    """
    Adds cities in LIST_CITIES_CARDS_CUBES to globals().
    Useful so you can type chicago with autocomlete instead of 'chicago'
    """
    for city, _, _ in LIST_CITIES_CARDS_CUBES:
        globals_dict[city] = city
