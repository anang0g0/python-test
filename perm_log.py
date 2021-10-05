import functools, itertools, random, math
from sympy.combinatorics import Permutation

def cycle_rounds(p1, p2, verbose = False):
    '''detect all cycles in p1 how many times rounded in p2
    Usage:
        >>> p = Permutation(10)(2,3,4,5)(6,7)
        >>> cycle_rounds(p,p**3)
        [(1, 2), (3, 4)]
    this means there are 2 cycles,
    size 2 cycle rounded 1 (actually 3, but it's identical)
    size 4 cycle rounded 3
    '''
    ret = {}
    c_p2 = p2.full_cyclic_form
    for c1 in p1.cyclic_form:
        c1_len = len(c1)
        if c1_len in ret: 
            continue
        if verbose:
            print("---")
        c1 = Permutation([c1])
        c = c1
        for i in range(1, c1_len + 1):
            c_c = c.cyclic_form
            if verbose:
                print(c_c)
            if all([c in c_p2 for c in c_c]):
                ret[c1_len] = i % c1_len
                break
            c = c * c1
    return [(r, l) for l, r in ret.items()]

def lcm(a, b):
    return a*b // math.gcd(a,b)

def euclid_x(a, b, c):
    ''' solve one of ax + by = c and return x
    Usage:
        >>> euclid_x(1, 2, 3)
        3
    '''

    def euclid1_x(a, b):
        ''' solve one of ax + by = 1 and return x
        '''
        if abs(b) == 1:
            return 0
        return (1 - b * euclid1_x(b, a % b)) // (a % b)

    gcd = math.gcd(a, b)
    if c % gcd != 0:
        raise ArithmeticError("unsolvable")
    if abs(gcd) == 1:
        return c * euclid1_x(a, b)
    return euclid_x(a//gcd, b//gcd, c//gcd)

def general_sim_con(r_l, verbose = False):
    '''solve general simultaneous congruence
    x = r1 mod l1
    x = r2 mod l2
      ...
    x = ri mod li
    ret: (r, l) where x = r + kl which satisfies all congruences
    Usage:
        >>> general_sim_con([(2,5), (3,7)])
        (17, 35)
    '''

    def general_sim_con2(one, two):
        ''' solve two general simultaneous congruence
        using bezout equation and Euclidian algorithm
        x = r1 mod l1
        x = r2 mod l2
        ret: (r, l) where x = r + kl which satisfies both congruences
        '''

        a1, n1 = one
        a2, n2 = two
        x = euclid_x(n1, n2, a2 - a1)
        a = n1 * x + a1
        _lcm = lcm(n1, n2)
        return a % _lcm, _lcm

    return functools.reduce(general_sim_con2, r_l)

def perm_log(sx, base, verbose = False):
    ''' get x from Permutations base, base ** x
    
    ret: (x, l) where l is the cyclic length of base
    Usage:
        >>> p = Permutation(10,9)(1,3,2,4)
        >>> perm_log(p**3, p)
        (3, 4)
    '''
    r_l = cycle_rounds(base, sx)

    if verbose:
        print("cycle_rounds: " + str(r_l))
        for r, l in r_l:
            print("x = %d mod %d" % (r, l))

    ret, m = general_sim_con(r_l, True)
    # m == functools.reduce(lcm, map(lambda a: a[1], r_l))
    return ret, m

if __name__ == '__main__':
    #import doctest
    #doctest.testmod()

    def test(s, x):
        sx = s**x

        print("%s ^ %d = %s" % (s.cyclic_form, x, sx.cyclic_form))
        log, l = perm_log(sx, s)
        print("kotae awase %d == %d (mod %d)" % (x, log , l))
        if x % l == log:
            print("success")
        else:
            raise Exception("fail")

    a = list(range(0,40))
    random.shuffle(a)
    test(Permutation(a), random.randint(10, 1000))