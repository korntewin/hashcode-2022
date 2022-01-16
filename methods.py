import typing as t
import csv
from itertools import combinations

import numpy as np

from my_io import parse_input


def cal_score(used_ings: set, cust_prefs: dict) -> int:

    rem_custs = [
        *filter(
            lambda pairs: len(pairs[1][1] - used_ings) == 0 and len(pairs[1][0] - used_ings) == len(pairs[1][0]), 
            cust_prefs.items())
        ]

    return len(rem_custs)


def method_pso(num_c, cust_prefs, likes, dislikes, all_ings):

    from pso import Swarm

    overlap_dislike_dict = {ind: ing for ind, ing in enumerate(dislikes.intersection(likes))}

    # pso params
    score_func = lambda used_ings: cal_score(used_ings, cust_prefs)
    def input_parser(xs: np.array):
       remove_ings = {overlap_dislike_dict[idx] for idx, x in enumerate(xs) if x == 1}
       return likes - remove_ings

    n_vars = len(overlap_dislike_dict)
    int_pos = np.ones(n_vars) == 1
    lbs_x = np.zeros(n_vars)
    ubs_x = np.ones(n_vars)
    lbs_v = -(ubs_x + lbs_x)/2
    ubs_v = (ubs_x + lbs_x)/2

    s = Swarm(n_vars, int_pos, lbs_x, ubs_x, lbs_v*3, ubs_v*3)
    s.optimize(score_func, input_parser)
    optim_remove_ings = s.get_x(s.g_best_x)

    # write output
    optim_used_ings = likes - optim_remove_ings
    return optim_used_ings


def method1(fp: str):

    _, cust_prefs, likes, dislikes, all_ings = parse_input(fp)

    max_score = 0
    used_ing = {}

    for i in range(1, 2):
        combs = [likes - set(ele) for ele in combinations(dislikes, i)] \
            if len(dislikes) != 0 else [set()]
        scores = [cal_score(likes - cut_ings, cust_prefs) for cut_ings in combs]

        if len(combs) > 0:
            (cur_ings, cur_max) = max(zip(combs, scores), key=lambda pairs: pairs[1])
            if cur_max > max_score:
                max_score = cur_max
                used_ing = all_ings - cur_ings

    print(f"global max score: {max_score}")
    print(f"global max ing: {used_ing}")
