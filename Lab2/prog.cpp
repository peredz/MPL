#include <iostream>

void fib_numbers(int n)
{
    int a = 0;
    int b = 1;
    int c = 0;

    for (int i = 0; i < n; i++)
    {
        c = a + b;
        a = b;
        b = c;
        std::cout << a << std::endl;
    }
}

void find_divisors(int n)
{
    for (int i = 1; i < n; i++)
    {
        if (n % i == 0)
        {
        std::cout << i << std::endl;
        }
    }
}

void is_prime_number(int n)
{
    for (int i = 2; i < n; i++)
    {
        if (n % i == 0)
        {
        std::cout << n << ' is not prime number';
        std::cout << 'it can be divided by' << i;
        return;
        }
    }
    std::cout << n << ' is prime number';
}



int main()
{
    fib_numbers(10);
    find_divisors(801);
    find_divisors(809);
    is_prime_number(809);
}