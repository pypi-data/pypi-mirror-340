# Prime Bits

Prime Bits is a project focused on exploring and working with prime numbers in the context of computer science and programming.

## Features

- Efficient algorithms for prime number generation.
- Utilities for prime number validation.
- Tools for analyzing prime-related patterns.

## How to install

```bash
python3 -m pip install prime-bits
```

## How to use
```python
from prime_bits import get_prime

get_prime(1024) # 1024 -> number of bits in the number.
```

## Functions

- `get_prime` - You can see what that function does above. 👆

In the version `v1.0.4` I have added 2 additional functions.

- `get_safe_prime` - This function returns a safe prime number. (This uses multi-processing)
- `is_prime` - This function checks if the number given is a prime. (This uses the Miller-Rabin primality test)
  
```python
from prime_bits import get_safe_prime, is_prime


get_safe_prime(1024) # This will act the exact same way as the `get_prime` function. But it will ensure that the prime number given is a safe prime.

is_prime(some_prime_number) # This will checks using the Miller-Rabin primality test, is this number a prime. If so it will return True, False otherwise.
```

## General Utils

- `gdc(a, b)` - Calculate the Greatest Common Divisor (GCD) of two integers using the Euclidean algorithm.
- `lcm(a, b)` - Calculate the Least Common Multiple (LCM) of two integers.
- `euler_totient(n)` - Calculate Euler's Totient Function φ(n), which counts the integers from 1 to n that are coprime with n.



## License

This project is licensed under the MIT License.
