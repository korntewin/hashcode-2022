use rust::parse_input;

fn main() {

    let data = "./data/a_an_example.in.txt";
    let (like, dislike, cust_prefs ) = parse_input(data.to_string());

    like.iter().for_each(|ele| println!("{}", ele));
    dislike.iter().for_each(|ele| println!("{}", ele));
}
