from Floor_planning import *

blocks = [(2, 3), (3, 4), (3, 4)]
nets = [(0, 1), (1, 2)]
for i in blocks:
    Plan.add_block(i[0], i[1])
g = Plan.create_random()
print("g")
print(g.tree)
print(g.calculate_fitness())
h = Plan.create_random()
print("h")
print(h.tree)
print(h.calculate_fitness())
a, b = Plan.crossover(g, h)
print("a")
print(a.tree)
print(a.calculate_fitness())
print("b")
print(b.tree)
print(b.calculate_fitness())
for i in range(10):
    b.mutate()
    print("b")
    print(b.tree)
    print(b.calculate_fitness())
