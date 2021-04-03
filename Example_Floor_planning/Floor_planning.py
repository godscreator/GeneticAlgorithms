from Genetic.MultiObjectiveAlgorithms import *
import random


class Plan(Gene):
    blocks = []
    nets = []

    @classmethod
    def add_block(cls, breadth, height):
        cls.blocks.append((breadth, height))

    @classmethod
    def add_net(cls, block_a, block_b):
        cls.nets.append((block_a, block_b))

    @classmethod
    def create_random(cls) -> 'Plan':
        block_bag = list(range(len(cls.blocks)))
        random.shuffle(block_bag)
        tree = []
        count = 0
        bag_ind = 0
        while count >= 2 or bag_ind < len(block_bag):
            if count >= 2 and bag_ind < len(block_bag):
                r = random.random()
                if r >= 0.5:
                    tree.append(block_bag[bag_ind])
                    count += 1
                    bag_ind += 1
                else:
                    x = random.random()
                    if x >= 0.5:
                        tree.append('H')
                    else:
                        tree.append('V')
                    count -= 1
            elif count >= 2:
                x = random.random()
                if x >= 0.5:
                    tree.append('H')
                else:
                    tree.append('V')
                count -= 1
            elif bag_ind < len(block_bag):
                tree.append(block_bag[bag_ind])
                count += 1
                bag_ind += 1
        return Plan(tree)

    def __init__(self, tree):
        self.tree = tree

    def mutate(self) -> None:
        a = random.randint(0, len(self.tree) - 1)
        if self.tree[a] == 'H':
            self.tree[a] = 'V'
        elif self.tree[a] == 'V':
            self.tree[a] = 'H'
        else:
            a = random.randint(1, len(Plan.blocks)-1)
            b = random.randint(a+1, len(Plan.blocks))
            c = 0
            x, y = 0, 0
            bag = set(range(len(Plan.blocks)))
            for i in range(len(self.tree)):
                if self.tree[i] in bag:
                    c += 1
                    if c == a:
                        x = i
                    if c == b:
                        y = i
            self.tree[x], self.tree[y] = self.tree[y], self.tree[x]

    @staticmethod
    def crossover(parent_a: 'Plan', parent_b: 'Plan') -> ('Plan', 'Plan'):
        child_a = parent_a.tree[:]
        child_b = parent_b.tree[:]
        a_ind = 0
        b_ind = 0
        bag = set(range(len(Plan.blocks)))
        for i in parent_b.tree:
            if i in bag:
                while a_ind < len(child_a) and (child_a[a_ind] not in bag):
                    a_ind += 1
                if a_ind >= len(child_a):
                    break
                child_a[a_ind] = i
                a_ind += 1
        for i in parent_a.tree:
            if i in bag:
                while b_ind < len(child_b) and child_b[b_ind] not in bag:
                    b_ind += 1
                if b_ind >= len(child_b):
                    break
                child_b[b_ind] = i
                b_ind += 1
        return Plan(child_a), Plan(child_b)

    def calculate_fitness(self) -> List[float]:
        stack = []
        bag = set(range(len(Plan.blocks)))
        for i in self.tree:
            if i in bag:
                stack.append(Plan.blocks[i])
            elif i == 'H':
                x_b, x_h = stack.pop()
                y_b, y_h = stack.pop()
                stack.append((max(x_b, y_b), x_h + y_h))
            elif i == 'V':
                x_b, x_h = stack.pop()
                y_b, y_h = stack.pop()
                stack.append((x_b + y_b, max(x_h, y_h)))
        b, h = stack[0]
        area = b * h
        delay = 0
        return [area, delay]
