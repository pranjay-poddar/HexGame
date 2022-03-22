from __future__ import division, print_function
from random import randrange
from time import time
import sys

hex_digits = '0123456789ABCDEF'

def bits(n): return bin(n+16)[3:] # i.e. 5 -> '0101'

def ref(): # print ref table bin to hex
    print('-'*39)
    for i in range(0,16,4):
        for n in range(i,i+4):
            f = '{:2d} {}:{}'
            print(f.format(n, hex_digits[n], bits(n)), end=' ')
        print()
    print('   q: quit, r: reference\n' + '-'*39)

def pick(): # pick 4 random digits from 0 to 16 inclusive
    return [randrange(16), randrange(16), 
            randrange(16), randrange(16)]

def play(digits): 
    # play one round return won boolean, 'quit', or 'reference'
    bins = ( bits(d) for d in digits )
    print(' '.join(bins), end=' ? ')
    sys.stdout.flush()
    guess = sys.stdin.readline().upper()[:4].upper()  # can't use input
    if guess[0] == 'Q' : return 'quit'
    if guess[0] == 'R' : return 'reference'
    expect = ''.join((hex_digits[d] for d in digits)) 
    return  expect == guess

def main(): # main loop with tracking of best runs
    ref()

    run_count = 0
    run_elapsed = 0.0
    last_time = time()
    best_runs = {}
    
    def add_run(count, elapsed):
        if (count not in best_runs or elapsed < best_runs[count]) and count > 0:
            best_runs[count] = elapsed
    
    while True:
        correct = play(pick())
        if correct == 'quit':
            break
        if correct == 'reference': 
            ref()
            continue
        if correct:
            run_count += 1
            current_time = time()
            run_elapsed += current_time - last_time
            last_time = current_time
            f = '  correct:  {} run(s) average {:.01f} seconds per try'
            print(f.format( run_count, run_elapsed/run_count))
        else:
            add_run(run_count, run_elapsed)
            run_count = 0
            run_elapsed = 0.0
            last_time = time()
            print('wrong')
    add_run(run_count, run_elapsed)
    
    for c in best_runs:
        print('\nRECAP:')
        f = '{} run(s) average {:.01f} seconds per try'
        print(f.format(c, best_runs[c]/c))
        
if __name__ == '__main__':
    main()
