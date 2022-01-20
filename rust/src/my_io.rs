use std::{fs, collections::{HashSet, HashMap}};

pub fn parse_input(filename: String) -> (HashSet<String>, HashSet<String>, HashMap<usize, HashMap<usize, HashSet<String>>>) {
    println!("Load filename: {}", filename);

    let contents = fs::read_to_string(&filename)
        .expect(&"Read file fail");

    let lines = contents
        .split('\n')
        .map(
            |x| 
                x
                .split(' ')
                .map(
                    |x| x.to_string()
                )
                .collect()
            )
            .collect::<Vec<Vec<String>>>();

    let mut likes: HashSet<String> = HashSet::new();
    let mut dislikes: HashSet<String> = HashSet::new();
    let mut customer_prefs: HashMap<usize, HashMap<usize, HashSet<String>>> = HashMap::new();

    let parse_line = |pairs: (usize, &Vec<String>)| -> () {
        let (idx, line) = pairs;
        match idx {
            idx if idx % 2 == 1 && idx > 0 => {
                let new_set = HashSet::<String>::from_iter(line[1..].iter().map(|ele| ele.clone()));
                likes.extend(new_set.clone());
                customer_prefs.insert((idx+1)/2, HashMap::from([(1, new_set.clone())]));
            },
            idx if idx % 2 == 0 && idx > 0 => {
                let new_set = HashSet::<String>::from_iter(line[1..].iter().map(|ele| ele.clone()));
                dislikes.extend(new_set.clone());
                customer_prefs
                    .entry((idx+1)/2)
                    .or_insert(HashMap::from([(0, new_set.clone())]))
                    .insert(0, new_set.clone());
            }
            _ => (),
        }
    };

    let _temp = lines.iter().enumerate().map(parse_line).collect::<Vec<()>>();

    (likes, dislikes, customer_prefs)

}
