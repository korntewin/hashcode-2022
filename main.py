import csv
from methods import method_pso

from my_io import parse_input

def main():
    fp = './data/b_basic.in.txt'
    op = './output/b_basic.out.txt'

    num_c, cust_prefs, likes, dislikes, all_ings = parse_input(fp)

    optim_used_ings = method_pso(num_c, cust_prefs, likes, dislikes, all_ings)

    cw = csv.writer(open(op, 'w'))
    cw.writerow([len(optim_used_ings)] + list(optim_used_ings))
    

if __name__ == '__main__':
    main()
