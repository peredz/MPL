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
        std::cout << c << std::endl;
    }
}

int main()
{
    fib_numbers(10);
}