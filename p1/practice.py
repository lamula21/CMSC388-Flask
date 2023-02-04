def hello_world():
    """ Returns 'Hello, World!'

    Arguments:
    None

    Usage:
    >>> hello_world()
    'Hello, World!'
    """
    return 'Hello, World!'


def sum_unique(l):
    """ Sums values in l, not counting duplicates.

    Arguments:
    l -- a list of integers

    Usage:
    >>> sum_unique([])
    0
    >>> sum_unique([4, 4, 5])
    9
    >>> sum_unique([4, 2, 5])
    11
    >>> sum_unique([2, 2, 2, 2, 1])
    3
    """
    set = { each for each in l}
    return sum(set)


def palindrome(x):
    """ Determines if x, an integer or string, is a palindrome, i.e.
    has the same value reversed.

    Arguments:
    x -- an integer or string

    Usage:
    >>> palindrome(1331)
    True
    >>> palindrome('racecar')
    True
    >>> palindrome(1234)
    False
    >>> palindrome('python')
    False
    """
    x_string = str(x)
    length = len(x_string)

    for i in range(length):
        if x_string[i] != x_string[length - i - 1]:
            return False
        
    return True

def sum_multiples(num):
    """ Sums up all multiples of 3 and 5 upto and not including num.

    Arguments:
    num -- a positive integer

    Usage:
    >>> sum_multiples(10) # Multiples: [3, 5, 6, 9]
    23
    >>> sum_multiples(3) # Multiples: []
    0
    >>> sum_multiples(5) # Multiples: [3]
    3
    >>> sum_multiples(16) # Multiples: [3, 5, 6, 9, 10, 12, 15]
    60
    """
    newSet = set()

    for i in range(num):
        if i%3 == 0 or i%5 == 0:
            newSet.add(i)
    newList = list(newSet)

    # If the list is empty, return 0
    if len(newList) == 0:
        return 0
    
    return sum(newList)


def num_func_mapper(nums, funs):
    """Applies each function in funs to the list of numbers, nums, and
    returns a list consisting of the results of those functions. 

    Arguments:
    nums -- a sequence of numbers
    funs -- a sequence of functions
          - each function in funs acts on a sequence of numbers and returns a number

    Usage:
    >>> f_list = [sum_unique, sum]
    >>> num_list = [2, 2, 2, 4, 5]
    >>> num_func_mapper(num_list, f_list)
    [11, 15]
    """
    newList = list()

    for fun in funs:
        newList.append(fun(nums))
    
    return newList

def pythagorean_triples(n):
    """ Finds all pythagorean triples where a, b, and c (sides of the triangle)
    are all less than n units long. This function should not return distinct tuples
    that still represent the same triangle. For example, (3, 4, 5) and (4, 3, 5)
    are both valid pythagorean triples, but only the first should be in the final list.

    The tuple elements should be sorted in ascending order, and the
    list of tuples should be sorted in ascending order by the last element of the tuple.

    Arguments:
    n -- a positive integer

    Usage:
    >>> pythagorean_triples(10)
    [(3, 4, 5)]
    >>> pythagorean_triples(11)
    [(3, 4, 5), (6, 8, 10)]
    >>> pythagorean_triples(20)
    [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
    """

    # n = 11

    # Getting odd list
    odd = list(filter( lambda x: x%2 != 0, range(n)))
    odd.sort()  # [1, 3, 5, 7, 9]

    # Getting even list
    even = list(filter( lambda x: x%2 == 0, range(n)))
    even.sort() # [0, 2, 4, 6, 8]

    mySet = set()

    # If “x” is odd, then the Pythagorean triple = x, (x2/2) – 0.5, (x2/2) + 0.5
    for each in odd:
        a = each                         # 1 | 3 | 5  | 7  | 9
        b = int((pow(each,2)/2) - 0.5)   # 0 | 4 | 12 | 24 | 40 
        c = int((pow(each,2)/2) + 0.5)   # 1 | 5 | 13 | 25 | 41
        if b < 1 or b >= n:
            continue
        if c < 1 or c >= n:
            continue

        tuple_sorted = tuple(sorted((a,b,c)))   # sort tuple
        mySet.add(tuple_sorted)                 # add tuple to set

    # If “x” is even, then the Pythagorean triple = x, (x/2)2-1, (x/2)2+1.
    for each in even:
        a = each                     # 0  | 2 | 4 | 6  | 8 
        b = int(pow(each/2,2) - 1)   # -1 | 0 | 3 | 8  | 15
        c = int(pow(each/2,2) + 1)   # 1  | 2 | 5 | 10 | 17

        if b < 1 or b >= n:
            continue
        if c < 1 or c >= n:
            continue

        tuple_sorted = tuple(sorted((a,b,c))) # sort tuple
        mySet.add(tuple_sorted)               # add tuple to set

    # mySet = {(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)}
    
    # Find mutiples of the triples
    multipleSet =   set()
    for a, b, c in mySet:
        for i in range(1, n):
            new_a = a*i
            new_b = b*i
            new_c = c*i

            if new_a >= n or new_b >= n or new_c >= n:
                continue

            #otherwise
            multipleSet.add((new_a, new_b, new_c))

    mySet = mySet.union(multipleSet) # Added (3k ,4k, 5k) , (5k ,12k, 13k), (7k, 24k, 25k), ...


    # Convert set to list
    myList = list(mySet)

    # Sort list of tuples according to key (sorted by last element)
    newListSorted = sorted(myList, key= lambda each_tuple : each_tuple[2])  # each_tuple[2] = last element of (a,b,c)
    # i.e: [(6, 8, 10), (3, 4, 5)]
    #   => [(3, 4, 5), (6, 8, 10)]
    
    return newListSorted


def custom_sort(lst):
    """ Use Python's built-in sort function to sort the list so that the odd numbers (in the same order as in the original list) come first, and then the even numbers (also in the same order).

    Examples:

    >>> custom_sort([1, 2, 3, 4, 5])
    [(1, 3, 5, 2, 4)]
    (Hint: use a lambda function) 
    """

    # Getting odd list
    odd = list(filter( lambda x: x%2 != 0, lst))
    odd.sort()

    # Getting even list
    even = list(filter( lambda x: x%2 == 0, lst))
    even.sort()

    # Join two lists
    odd_even = odd + even

    return odd_even




