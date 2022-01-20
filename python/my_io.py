import typing as t

def parse_input(fp: str) -> t.Tuple[int, dict, set, set, set]:
    
    with open(fp, 'r') as f:

        lines = [*map(lambda line: line.replace('\n', '').split(' '), f.readlines())]

        num_c = int(lines[0][0])
        cust_prefs: dict = {}
        like_ings: set = set()
        dislike_ings: set = set()
        all_ings: set = set()

        for i, pref in enumerate(lines[1:]):
            if i % 2 == 0:
                cust_prefs[i//2] = {1: set(pref[1:])}
                like_ings = like_ings.union(set(pref[1:]))
            else:
                cust_prefs[i//2][0] = set(pref[1:])
                dislike_ings = dislike_ings.union(set(pref[1:]))

        all_ings = like_ings.union(dislike_ings)

    return num_c, cust_prefs, like_ings, dislike_ings, all_ings
