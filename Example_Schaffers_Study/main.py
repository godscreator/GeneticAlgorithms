from Schaffer import *

import pygame
from Plotter.PygamePlotter import Plotter

# initialize the pygame
pygame.init()

# create the screen
screenX = 790
screenY = 790
screen = pygame.display.set_mode((screenX, screenY))

# Title and Icon
pygame.display.set_caption("Schaffer's Study")

rect1 = pygame.Rect(10, 10, 380, 380)
solution_panel = (10, 10, 380, 380)
rect2 = pygame.Rect(10, 400, 380, 380)
objective_panel = (10, 400, 380, 380)
rect3 = pygame.Rect(400, 10, 380, 380)
update_panel = (400, 10, 380, 380)
rect4 = pygame.Rect(400, 400, 380, 380)
generation_panel = (400, 400, 380, 380)

objective_graph = Plotter(screen, (objective_panel[0], objective_panel[1]), (objective_panel[2], objective_panel[3]))
solution_graph = Plotter(screen, (solution_panel[0], solution_panel[1]), (solution_panel[2], solution_panel[3]))

# text
font = pygame.font.Font('freesansbold.ttf', 16)


def draw_text(s, pos, color=(0, 0, 0)):
    text = font.render(s, True, color)
    screen.blit(text, pos)


gen_count = 0
pool = get_schaffer_pool(100)
pool.initialize_population()

# Game Loop
FPS = 1  # frames per second setting
fpsClock = pygame.time.Clock()
running = True
while running:
    # background
    screen.fill((127, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), rect1)
    pygame.draw.rect(screen, (255, 255, 255), rect2)
    pygame.draw.rect(screen, (255, 255, 255), rect3)
    pygame.draw.rect(screen, (255, 255, 255), rect4)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pool.generate()
    best_genes = pool.get_best_genes()
    best_genes.sort(key=lambda g: math.pow(g.x, 2))
    gen_count += 1

    # display graph
    objective_graph.clear()
    objective_graph.ax.scatter([-i.fitness[0] for i in pool.wrappers], [-i.fitness[1] for i in pool.wrappers],
                               color='black')
    objective_graph.ax.scatter([math.pow(i.x, 2) for i in best_genes], [math.pow(i.x - 2, 2) for i in best_genes],
                               color='red')
    objective_graph.ax.plot([math.pow(i.x, 2) for i in best_genes], [math.pow(i.x - 2, 2) for i in best_genes],
                            color='red')
    objective_graph.ax.set_title("objective")
    objective_graph.ax.set_xlabel("x^2")
    objective_graph.ax.set_ylabel("(x-2)^2")
    objective_graph.show()

    # display graph
    solution_graph.clear()
    solution_graph.ax.scatter(list(range(1, pool.population_size + 1)), [i.gene.x for i in pool.wrappers])
    solution_graph.ax.set_title("solution")
    solution_graph.ax.set_xlabel("position")
    solution_graph.ax.set_ylabel("x")
    solution_graph.show()

    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
