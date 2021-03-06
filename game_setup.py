# city - num good cards - num_bad_cards - num_cubes_placed
LIST_CITIES_CARDS_CUBES = [
    ('tripoli',       4, 3 * 0, 0), # forsaken
    ('istanbul',      4, 3,     2),
    ('cairo',         4, 3,     2),

    ('new_york',      4, 3 * 0, 2),
    ('washington',    4, 3 - 1, 2),
    ('jacksonville',  4, 3,     2),
    ('chicago',       2, 2,     1),
    ('atlanta',       1, 1 - 1, 0),
    ('denver',        2, 2 - 1, 1),
    ('los_angeles',   1, 1 - 1, 0),
    ('san_francisco', 2, 2 * 0, 0),
    ('mexico_city',   1, 1 - 1, 0),

    ('london',        4, 3 - 2, 1),
    ('paris',         2, 2 - 1, 1),
    ('frankfurt',     2, 2,     2),
    ('st_peterburg',  1, 1,     2),
    ('moscow',        1, 1 - 1, 0),

    ('sao_paolo',     4, 3,     2),
    ('buenos_aires',  2, 2 - 2, 0),
    ('lima',          1, 1 - 1, 0),
    ('bogota',        2, 2 - 1, 2),
    ('santiago',      1, 1 - 1, 0),

    ('lagos',         4, 3 - 3, 0),
    ('kinshasa',      1, 1,     2),
    ('johannesbourg', 2, 2,     2),
    ('dar_es_salam',  2, 2,     2),
    # ('antananarivo',  2, 2,     0),
    # ('khartoum',      1, 1,     0),

    ('baghdad',       2, 2,     2),
    ('tehran',        1, 1,     0),
    ('mumbai',        2, 2,     0),
    # ('delhi',         1, 1, 0),
    # ('riyadh',        2, 2, 0),
    # ('kolkata',       1, 1, 0),
]

print(f"{'City':20s} {'bad':10} {'cubes'}")

for city, _, bad, cubes in LIST_CITIES_CARDS_CUBES:
    if cubes > bad:
        print(f"{city:20s} {bad}{'':4s} < {'':4}{cubes}")

print('-' * 30)

for city, _, bad, cubes in LIST_CITIES_CARDS_CUBES:
    if bad > cubes:
        print(f"{city:20s} {bad}{'':4} > {'':4}{cubes}")

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
