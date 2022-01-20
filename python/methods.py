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


def input_parser(xs: np.array, overlap_dislike_dict: dict, likes: set):
    remove_ings = {overlap_dislike_dict[idx] for idx, x in enumerate(xs) if x == 1}
    return likes - remove_ings


def cal_score_fraction(xs, ing2ind_dict, cust_prefs: dict) -> int:
    """Able to calculate fraction input
    """

    like_scores = [
        xs[ing2ind_dict[like]] 
        for _, prefs in cust_prefs.items() 
        for like in prefs[1]
        if like in ing2ind_dict
    ]

    dislike_scores = [
        xs[ing2ind_dict[dislike]] 
        for _, prefs in cust_prefs.items() 
        for dislike in prefs[0]
        if dislike in ing2ind_dict
    ]

    return sum(like_scores) - sum(dislike_scores)


def input_parser_fraction(xs: np.array):

    return xs


def method_pso(num_c, cust_prefs, likes, dislikes, all_ings):

    from pso import Swarm

    overlap_dislike_dict = {ind: ing for ind, ing in enumerate(dislikes.intersection(likes))}
    ing2ind_dict = {ing: ind for ind, ing in overlap_dislike_dict.items()}

    # pso params
    full_func = lambda used_ings: cal_score(used_ings, cust_prefs)
    full_parser = lambda xs: input_parser(xs, overlap_dislike_dict, likes)
    frac_func = lambda xs: cal_score_fraction(xs, ing2ind_dict, cust_prefs)
    frac_parser = lambda xs: input_parser_fraction(xs)

    n_vars = len(overlap_dislike_dict)
    int_pos = np.ones(n_vars) == 1
    lbs_x = np.zeros(n_vars)
    ubs_x = np.ones(n_vars)
    lbs_v = -(ubs_x + lbs_x)/2
    ubs_v = (ubs_x + lbs_x)/2

    s = Swarm(n_vars, int_pos, lbs_x, ubs_x, lbs_v*3, ubs_v*3, max_iter=1000)
    s.optimize(full_func, full_parser, fraction_mode=False)
    optim_used_ings = full_parser(s.get_x(s.g_best_x))

    # write output
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
