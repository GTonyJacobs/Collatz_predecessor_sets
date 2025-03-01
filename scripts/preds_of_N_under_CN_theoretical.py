import math

# Set parameter here
C = 1

gamma = math.log(3,2)

m = 1
count = 0
while True:
    ceiling = math.floor(math.log(C, 2) + m * gamma)
    numerator = sum([math.comb(k-1, m-1) for k in range(m, ceiling+1)])
    #print(f"{numerator}/{3 ** m}")
    new_count = numerator / 3 ** m
    count = count + new_count
    #print(new_count)
    if new_count < .0000001:
        break
    m += 1

print(f"{count:.3f}")
