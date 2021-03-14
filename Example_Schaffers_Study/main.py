from Schaffer import *
from prettytable import PrettyTable

gen_count = 0
pool = get_schaffer_pool(10)
pool.initialize_population()
while gen_count <= 50:
    print()
    print("Generation Count: ", gen_count)
    t = PrettyTable(["x", "x^2", "(x-2)^2", "rank", "crowd"])
    for i in pool.wrappers:
        t.add_row([i.gene.x, -i.fitness[0], -i.fitness[1], i.rank, i.cDist])
    print(t)
    pool.generate()
    gen_count += 1
