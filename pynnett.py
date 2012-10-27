__author__ = 'mjholler'

import re
import itertools

EXIT_BAD_ARGS = 1

parent1 = parent2 = None

def generate_gams(gen):
    """ Creates possible gametes for the one parent's alleles.
        Does this by cartesian product on an array in the form:
        [[gene1_allele1, gene1_allele2], ..., [geneN_allele1, geneN_allele2]]
    """
    return [x for x in itertools.product(*gen)]

def combine_gams(gam1, gam2):
    """ Takes two gametes (one from each parent) and combines them.
        E.g., gam1 = ('A','b') and gam2 = ('a','b'), gam1 + gam2 is
        ('A','a','b','b',)
    """
    zygote = []
    for x in xrange(len(gam1)):
        # To keep the traits in readable order, we put the dominant first
        # if there is one. For codominant traits, the alleles are placed in
        # alphabetical order (case insensitive).
        if gam1[x].isupper() and gam1[x].upper() == gam2[x].upper() \
                or ord(gam1[x].upper()) < ord(gam2[x].upper()):
            zygote.append(gam1[x])
            zygote.append(gam2[x])
        else:
            zygote.append(gam2[x])
            zygote.append(gam1[x])

    return tuple(zygote)

def print_punnett_square(punnett_square):
    # Convert the tuples into strings
    punnett_square = [[''.join(col) for col in row] for row in punnett_square]

    # Calculate the spacing we want for formatting
    min_col_width = len(punnett_square[-1][-1])
    col_width = min_col_width + 2

    # Form each line and print it
    line = ''
    for row in punnett_square:
        for col in row:
            line += '%-{}s'.format(col_width) % col
        print line
        line = ''

def main():

    # Get the possible gametes each parent can create
    gams1 = generate_gams(parent1)
    gams2 = generate_gams(parent2)

    # Start the punnett square table. Top left element is empty for proper
    # formatting
    punnet_square = [['']]

    # Populate top row of punnet square with gametes from parent2
    for g in gams2:
        punnet_square[0].append(g)

    # Populate left element in each row with gamete from parent1
    for g in gams1:
        punnet_square.append([g])

    # Fill in punnett square with gamete combinations
    current_row = 1
    for g1 in gams1:
        for g2 in gams2:
            zygote = combine_gams(g1, g2)
            punnet_square[current_row].append(zygote)
        current_row += 1

    print_punnett_square(punnet_square)

if __name__ == "__main__":
    import sys

    # Check the right number of arguments are given
    if len(sys.argv) == 1:
        parent1 = raw_input("Enter parent 1's genotype (e.x., WwTt):").strip()
        parent2 = raw_input("Enter parent 2's genotype (make sure to use the same trait order as parent 1):").strip()
        print parent1
        print parent2

    elif len(sys.argv) == 3:
        # Split input argument from e.g., "WwTt" into [['W','w'],['T','t']]
        parent1 = sys.argv[1]
        parent2 = sys.argv[2]

    else:
        print 'Improper usage. Please use like this:\n'\
              '{0} PARENT1 PARENT2\n'\
              'Example:\n'\
              '{0} WwTT wwTt'.format(sys.argv[0])
        exit(EXIT_BAD_ARGS)

    parent1 = [[g[0],g[1]] for g in re.findall('..', parent1)]
    parent2 = [[g[0],g[1]] for g in re.findall('..', parent2)]

    main()