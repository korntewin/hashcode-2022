use itertools::izip;
use rand::{thread_rng, Rng};

pub struct Particle {
    pub n_vars: i32,
    pub wv: f32,
    pub wl: f32,
    pub wg: f32,
    pub x: Vec<f32>,
    pub v: Vec<f32>,
    pub l_best_x: Vec<f32>,
    pub l_best_score: f32,
}

impl Particle {

    pub fn initial(&mut self) {
        let mut rng = thread_rng();
        self.x = (1..self.n_vars).map(|_| rng.gen::<f32>()).collect();
        self.v = (1..self.n_vars).map(|_| rng.gen::<f32>() * 2.0 - 1.0).collect();
        self.l_best_x = (1..self.n_vars).map(|_| rng.gen::<f32>()).collect();
    }

    pub fn update_v(&mut self, ubs_v: Vec<f32>, lbs_v: Vec<f32>, g_best_x: Vec<f32>) {

        let mut rng = thread_rng();
        let rl = rng.gen::<f32>();
        let rg = rng.gen::<f32>();

        let v_wv = self.v.iter().map(|x| x*self.wv);
        let dl = self.l_best_x.iter().zip(self.x.iter()).map(|(lx, x)| (lx - x) * rl * self.wl);
        let dg = g_best_x.iter().zip(self.x.iter()).map(|(gx, x)| (gx - x) * rg * self.wg);
        let v = izip!(v_wv, dl, dg).map(|(v, l, g)| v + l + g);
        self.v =  izip!(lbs_v, v, ubs_v).map(|(lb, v, ub)| {
            if v < lb {lb}
            else if v > ub {ub}
            else {v}
        }).collect::<Vec<f32>>();
                                            
    }

    pub fn update_x(&mut self) {
        let x = self.x.iter().zip(self.v.iter()).map(|(x, v)| x + v);
        let x_bound = x.map(|x| if x > 1.0 {1.0} else if x < 0.0 {1.0} else {x});
        self.x = x_bound.collect();
    }

    pub fn update_l_best(&mut self, newscore: f32) {
        if newscore > self.l_best_score {
            self.l_best_score = newscore;
            self.l_best_x = self.x.clone();
        }
    }

    pub fn update_par(&mut self, newscore: f32, ubs_v: Vec<f32>, lbs_v: Vec<f32>, g_best_x: Vec<f32>) {
        self.update_l_best(newscore);
        self.update_v(ubs_v, lbs_v, g_best_x);
        self.update_x();
    }
    
}

pub struct Swarm {

}
