use rust::parse_input;
use rust::Particle;

fn main() {

    let data = "./data/d_difficult.in.txt";
    let (like, dislike, cust_prefs ) = parse_input(data.to_string());

    println!("len like: {}", like.len());
    println!("len dislike: {}", dislike.len());
    let max_val = cust_prefs.iter().map(|(idx, _)| idx).max().unwrap_or(&0);
    let min_val = cust_prefs.iter().map(|(idx, _)| idx).min().unwrap_or(&0);
    println!("max cust: {}", max_val);
    println!("min cust: {}", min_val);
    // test print cust prefs
    cust_prefs.get(&1).unwrap().get(&1).unwrap().iter().for_each(|s| println!("{}", s));

    let mut p1 = Particle {
        n_vars: 10, wv: 0.7, wg: 2.0, wl: 2.0, x: Vec::new(), v: Vec::new(), l_best_x: Vec::new(), l_best_score: 0.0
    };

    p1.initial();

    println!("{:?}", p1.v);
    let v1 = (1..10).map(|x| x as f32).collect::<Vec<f32>>();
    p1.update_v(v1.clone(), v1.clone(), v1);
    println!("{:?}", p1.v);
}
