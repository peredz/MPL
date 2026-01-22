def fib_numbers(n):
    a = 0
    b = 1
    c = 0
    for i in range(0, n):
        c = a + b
        a = b
        b = c
        print( a)

def find_divisors(n):
    for i in range(1, n):
        if n % i == 0:
            print( i)

def is_prime_number(n):
    for i in range(2, n):
        if n % i == 0:
            print( n, ' is not prime number')
            print( 'it can be divided by', i)
            return
    print( n, ' is prime number')

if __name__ == '__main__':
    fib_numbers(10)
    find_divisors(801)
    find_divisors(809)
    is_prime_number(809)

