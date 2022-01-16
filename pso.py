import typing as t
import numpy as np
import time

class Swarm:
    """Swarm of particle for finding global optima
    """
    def __init__(self,
        n_vars: int, int_pos: np.array, lbs_x: np.array, ubs_x: np.array,
        lbs_v: np.array, ubs_v: np.array, wv: float = 0.9, wl: float = 1.5, wg: float = 1.5,
        n_pars = 100, max_persist_iter = 20, max_iter = 1000
        ):
        
        self.int_pos = int_pos
        self.lbs_v = lbs_v
        self.ubs_v = ubs_v
        self.lbs_x = lbs_x
        self.ubs_x = ubs_x
        self.wv = wv
        self.wl = wl
        self.wg = wg
        self.max_persist_iter = max_persist_iter
        self.g_best_score = -1 << 31
        self.g_best_x = None
        self.max_iter = max_iter

        # init particle
        self.pars = [Particle(n_vars, wv, wl, wg, seed=time.time_ns() % 1000000) for _ in range(n_pars)]
        [par.initial() for par in self.pars]

    def get_x(self, x):

        # round int position
        x = x.copy()

        # convert float
        interval_float = self.ubs_x - self.lbs_x
        x[~self.int_pos] = x[~self.int_pos] * interval_float[~self.int_pos] + self.lbs_x[~self.int_pos]

        # convert int
        interval_int = 1 / (self.ubs_x - self.lbs_x + 1)
        x[self.int_pos] = x[self.int_pos] // interval_int[self.int_pos] + self.lbs_x[self.int_pos]

        return x

    def evaluate(self, score_func: t.Callable, input_parser: t.Callable):

        xs = [self.get_x(par.x) for par in self.pars]
        scores = [score_func(input_parser(x)) for x in xs]
        return scores

    def update_global(self, newscore: float, newx: np.array):
        if newscore > self.g_best_score:
            self.g_best_score = newscore
            self.g_best_x = newx

    def optimize(self, score_func, input_parser) -> np.array:

        persist_count = 0
        iter = 0
        while persist_count < self.max_persist_iter and iter < self.max_iter:
            scores = self.evaluate(score_func, input_parser)
            
            max_pairs = max(zip(scores, self.pars), key=lambda pairs: pairs[0])

            if max_pairs[0] <= self.g_best_score:
                persist_count += 1
            else:
                self.update_global(max_pairs[0], max_pairs[1].x)
                persist_count = 0

            # update particle
            [par.update_par(score, self.ubs_v, self.lbs_v, self.g_best_x) 
            for score, par in zip(scores, self.pars)]
            
            iter += 1
            print(f'iter: {iter}, persit iter: {persist_count}, '
            f'best score: {self.g_best_score}')
            # f'best score: {self.g_best_score}, best x: {self.get_x(self.g_best_x)}')

        return self.g_best_x


class Particle:
    """One particle responsible for finding local optima
    """

    def __init__(self, 
            n_vars: int, wv: float = 0.7, wl: float = 2, wg: float = 2, seed = 191
        ):
        np.random.seed(seed)
        self.n_vars = n_vars
        self.wv = wv
        self.wl = wl
        self.wg = wg
        self.x = None
        self.v = None
        self.l_best_x = None
        self.l_best_score = -1 << 31

    def initial(self):

        # normalize x in 0 ~ 1
        x = np.random.rand(self.n_vars)
        self.x = x

        # init v
        v = np.random.rand(self.n_vars) * 2 - 1
        self.v = v

    def update_v(self, ubs_v: np.array, lbs_v: np.array, g_best_x: np.array):
        v = self.v*self.wv \
            + (self.l_best_x - self.x) * np.random.rand() * self.wl \
            + (g_best_x - self.x) * np.random.rand() * self.wg

        # cap v
        u_idx = v > ubs_v
        l_idx = v < lbs_v
        v[u_idx] = ubs_v[u_idx]
        v[l_idx] = lbs_v[l_idx]
        self.v = v

    def update_x(self):
        x = self.x + self.v

        # cap x
        x[x > 1] = 1
        x[x < -1] = -1
        self.x = x

    def update_l_best(self, newscore: float):
        if newscore > self.l_best_score:
            self.l_best_score = newscore
            self.l_best_x = self.x

    def update_par(self, newscore, ubs_v, lbs_v, g_best_x):
        self.update_l_best(newscore)
        self.update_v(ubs_v, lbs_v, g_best_x)
        self.update_x()



if __name__ == '__main__':
    
    scorefunc = lambda xy: -(xy[0]**2 + xy[1]**2)
    
    def input_parser(xs: np.array):
        return xs[0], xs[1]

    s = Swarm(2, np.array([True, True]), np.array([-10, -10]), np.array([10, 10]), np.array([-10, -10]), np.array([10, 10]))
    s.optimize(scorefunc, input_parser)


