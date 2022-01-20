from methods import method_pso

from my_io import parse_input

def main():
    fp = './data/d_difficult.in.txt'
    op = './output/e_elaborate.out.txt'

    num_c, cust_prefs, likes, dislikes, all_ings = parse_input(fp)

    optim_used_ings = method_pso(num_c, cust_prefs, likes, dislikes, all_ings)
    output = ' '.join([str(len(optim_used_ings)), *list(optim_used_ings)])
    with open(op, 'w') as f:
        f.write(output)
    

if __name__ == '__main__':
    main()
