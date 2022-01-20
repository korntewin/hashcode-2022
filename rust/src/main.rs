use rust::parse_input;

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
}
