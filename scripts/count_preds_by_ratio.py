import math
from collections import defaultdict

def is_admissible(n):
    """Check if a number is admissible (1 or 5 mod 6)."""
    return n % 6 in {1, 5}

def first_admissible_predecessor(n):
    """Find the first admissible predecessor of n.
       Return it, along with the corresponding power of 2."""
    if n % 18 in {11, 17}:
        return (2 * n - 1) // 3, 1
    if n % 18 in {1, 13}:
        return (4 * n - 1) // 3, 2
    if n % 18 == 5:
        return (8 * n - 1) // 3, 3
    if n % 18 == 7:
        return (16 * n - 1) // 3, 4

def next_pred(n):
    """Given an admissible predecessor, find the next one of the same order.
       Return it, along with its corresponding power of 2."""
    return (4 * n + 1, 2) if n % 6 == 1 else (16 * n + 5, 4)

def compute_k(n,depths):
    """This function computes a specific predecessor of n, given a specific depths vector."""
    current = n
    total_k=0
    for depth in depths:
        if depth == 1:  # Depth 1 always uses first_admissible_predecessor
            current,new_k = first_admissible_predecessor(current)
            total_k=total_k+new_k
        else:  # Depth > 1: Apply first_admissible_predecessor, then next_pred (depth-1) times
            current,new_k = first_admissible_predecessor(current)  # First step: apply first_admissible_predecessor
            total_k=total_k+new_k
            for _ in range(depth - 1):  # Apply next_pred (depth-1) times
                current,new_k = next_pred(current)
                total_k=total_k+new_k
    return current, total_k


def find_predecessors(ceiling, target_order, target_k):
    """The main algorithm, this function finds all admissible preds of the target ratio,
       in residue classes modulo `ceiling`."""
    target_hits = { }

    for n in range(1, ceiling, 2):
        if is_admissible(n):
            current = n
            if verbose:
                print(f"checking n={current}")
            target_hits[current] = []
            depths = [1] * target_order
            last_entry_incremented = len(depths) - 1
            exhausted = False

            while True:
                # Compute k from depths vector
                pred, k = compute_k(current,depths)
                if verbose:
                    print(f" {current}{depths} = {pred}. k={k} is ", end = "")

                if k < target_k:
                    if verbose:
                        print(f"too small!")
                    depths[-1] += 1
                else:
                    if k > target_k:
                        if verbose:
                            print(f"too big! ",end="")
                    if k == target_k:
                        if verbose:
                            print(f"just right! {current}{depths} is a hit! ", end="")
                        target_hits[current].append(pred)
                    if sum(depths) < target_k and target_order > 1: # not yet overflow
                        if verbose:
                            print()
                        depths[len(depths) - 2] += 1
                        last_entry_incremented = len(depths) - 2
                        depths[len(depths) - 1] = 1
                    else:
                        ## now we're in overflow mode
                        if verbose:
                            print(f"overflow")
                        overflow_entry = max(0, len(depths) - 2)
                        while overflow_entry > 0 and depths[overflow_entry] == 1:
                            overflow_entry -= 1
                        if overflow_entry == 0:
                            break
                        else:
                            depths[overflow_entry - 1] += 1
                            for i in range(overflow_entry, len(depths)):
                                depths[i] = 1
    if verbose:
        print()
    return target_hits

### Usage ###
target_order = 2   # How many predecessor layers to track
target_k = 12   # Desired power of 2
verbose = False  # Set to "True" for more detailed output

ceiling = 2 * 3 ** (target_order + 1)
print(f"\nSearching for predecessors of order m = {target_order} and degree k = {target_k}.")
print(f"That's a pred ratio of {2 ** target_k}/{3 ** target_order}. Checking admissible residue classes modulo {ceiling}...\n")

results = find_predecessors(ceiling, target_order,target_k)

if any(results.values()):
    total = 0
    for key, value in results.items():
        if value:
            preds = ", ".join(map(str, value))
            plural = "predecessors" if len(value) > 1 else "predecessor"
            print(f"{key} has {len(value)} matching {plural}, namely {preds}")
            total += len(value)
    print(f"\nThat's a total of {total} hits, in {2 * 3 ** (target_order)} classes, for a probability of {total//2}/{3 ** target_order}", end="")
    d = math.gcd(total, 3 ** target_order)
    if d > 1:
        print(f" (= {total // 2 // d}/{3 ** target_order // d})")
    else:
        print()
else:
    print("No starting values have matching predecessors")

