import math

def is_admissible(n):
    return n % 6 in {1,5}

def collatz_step(numer, multiplier, denom):
    numer = multiplier * numer + denom
    v2 = (numer & -numer).bit_length() - 1
    numer >>= v2
    return numer, v2

def get_input():
    """Prompt the user for target and max seed, allowing 'q' to quit. Ensures valid positive integers."""  
    def get_positive_int(prompt):
        """Helper function to repeatedly prompt the user until a valid positive integer is entered."""
        while True:
            user_input = input(prompt).strip().lower()
            if user_input == 'q':
                return 'q'  # Signal to quit
            try:
                value = int(user_input)
                if value > 0:
                    return value
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    target = get_positive_int("Enter the target number (must be a positive integer, or 'q' to quit): ")
    if target == 'q':
        return 'q', 'q'
    max_seed = get_positive_int("Enter the maximum seed number (must be a positive integer, or 'q' to quit): ")
    if max_seed == 'q':
        return 'q', 'q'
    return target, max_seed

def find_predecessors(target, max_seed):
    """Generator yielding seeds whose trajectories contain target."""
    seed = 1
    found_seeds=set()
    while seed <= max_seed:
        if is_admissible(seed):
            n = seed
            while n != 1 and n != target:
                n, _ = collatz_step(n, 3, 1)
            if n in found_seeds:
                yield seed
            if n == target:
                found_seeds.add(seed)
                yield seed
        seed += 2

def main():
    C = 1
    counts = []
    for seed in range(28000,30000):
        if is_admissible(seed):
            predecessors = find_predecessors(seed, seed * C)
            #print(*predecessors, sep=", ")  # Print all found values in one go
            count = sum(1 for _ in find_predecessors(seed, seed * C))  # Count predecessors without storing them
            #print(seed, count)
            counts.append(count)
            #print(f"\n{count} seeds under {max_seed} have trajectories containing {target}\n")
    print(sum(counts)/len(counts))

if __name__ == "__main__":
    main()
