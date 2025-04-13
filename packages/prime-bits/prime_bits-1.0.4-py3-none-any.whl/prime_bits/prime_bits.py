from random import getrandbits, randrange
from multiprocessing import Process, Queue


def get_prime(amount_of_bits: int, k=40) -> int:
    """Generate a prime number of exactly `amount_of_bits` using Miller-Rabin.
    Args:
        amount_of_bits (int): Number of bits for the prime.
        k (int): Miller-Rabin rounds for primality testing.
    
    Returns:
        int: A prime number with the specified bit length.
    """
    if not isinstance(amount_of_bits, int):
        raise ValueError("The variable `amount_of_bits` must be an int.")

    if amount_of_bits < 2:
        raise ValueError("Bit length must be at least 2.")

    while True:
        # Generate a random odd number with the exact bit length
        candidate = getrandbits(amount_of_bits)
        candidate |= (1 << (amount_of_bits - 1))  # Ensure top bit is set (exact bit length)
        candidate |= 1  # Ensure it's odd

        # Check primality
        if candidate % 3 == 0 or candidate % 5 == 0:  # Quick divisibility checks
            continue

        if is_prime(candidate, k):
            return candidate


def is_prime(n: int, k=40) -> bool:
    """Use the Miller-Rabin primality test to check if n is prime.
    Args:
        n (int): Number to test for primality.
        k (int): Number of rounds (higher = more accuracy).
    
    Returns:
        bool: True if probably prime, False if composite.
    """
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Quick divisibility checks for small primes
    for small_prime in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % small_prime == 0 and n != small_prime:
            return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Perform k trials
    for _ in range(k):
        a = randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite
    return True  # Probably prime



def find_safe_prime_worker(amount_of_bits: int, k: int, result_queue: Queue):
    """Worker function to find a safe prime and put it in the result queue."""
    while True:
        p = get_prime(amount_of_bits - 1, k)
        safe_prime_candidate = 2 * p + 1
        if is_prime(safe_prime_candidate, k):
            result_queue.put(safe_prime_candidate)
            break

def get_safe_prime(amount_of_bits: int, k=40, num_processes=4) -> int:
    """Generate a safe prime number using multiple processes.
    
    Args:
        amount_of_bits (int): Number of bits for the safe prime.
        k (int): Miller-Rabin rounds for primality testing.
        num_processes (int): Number of processes to use.
    
    Returns:
        int: A safe prime number with the specified bit length.
    """
    result_queue = Queue()
    processes = []

    # Start worker processes
    for _ in range(num_processes):
        process = Process(
            target=find_safe_prime_worker,
            args=(amount_of_bits, k, result_queue)
        )
        processes.append(process)
        process.start()

    # Wait for the first result
    safe_prime = result_queue.get()

    # Terminate all processes
    for process in processes:
        process.terminate()
        process.join()

    return safe_prime

