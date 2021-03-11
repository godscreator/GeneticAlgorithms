import pygame
import TSP
from Plotter.PygamePlotter import Plotter

# initialize the pygame
pygame.init()

# create the screen
screenX = 790
screenY = 790
screen = pygame.display.set_mode((screenX, screenY))

# Title and Icon
pygame.display.set_caption("Travelling Salesman")

# cities
cities = []


def draw_cities(cities, offset=(0, 0)):
    for city in cities:
        pygame.draw.circle(screen, (255, 0, 0), (city.x + offset[0], city.y + offset[1]), 4)
        pygame.draw.circle(screen, (255, 0, 0), (city.x + offset[0], city.y + offset[1]), 10, width=1)


# roads
population = []


def draw_roads(road, offset=(0, 0), color=(255, 255, 255)):
    if road:
        order = road.order
        if len(order) >= 2:
            for i in range(len(order)):
                a = cities[order[i]]
                b = cities[order[(i + 1) % len(order)]]
                pygame.draw.line(screen, color, (a.x + offset[0], a.y + offset[1]), (b.x + offset[0], b.y + offset[1]))


tsp = TSP.get_tsp_pool(population_size=1000)
count = 0
best_road = None

rect1 = pygame.Rect(10, 10, 380, 380)
best_panel = (10, 10, 380, 380)
rect2 = pygame.Rect(10, 400, 380, 380)
population_panel = (10, 400, 380, 380)
rect3 = pygame.Rect(400, 10, 380, 380)
update_panel = (400, 10, 380, 380)
rect4 = pygame.Rect(400, 400, 380, 380)
generation_panel = (400, 400, 380, 380)

pop_graph = Plotter(screen, (population_panel[0], population_panel[1]), (population_panel[2], population_panel[3]))
gen_graph = Plotter(screen, (generation_panel[0], generation_panel[1]), (generation_panel[2], generation_panel[3]))
# text
font = pygame.font.Font('freesansbold.ttf', 16)


def draw_text(s, pos, color=(0, 0, 0)):
    text = font.render(s, True, color)
    screen.blit(text, pos)


generation_number = 0
generation_distance = []
best_fitness = None
best_distance_all = None
best_road_ever = None
# Game Loop
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # if clicked inside best panel
            if best_panel[0] < x < best_panel[0] + best_panel[2] and best_panel[1] < y < best_panel[1] + best_panel[3]:
                # add a new city
                new_city = TSP.City(x, y)
                TSP.Path.add_city(new_city)
                cities = TSP.Path.cities
                tsp.initialize_population()
                population = tsp.get_population()
                generation_number = 0
                generation_distance.clear()
                best_distance_all = None
                best_road_ever = None
    if len(cities) >= 2:
        # create next generation
        tsp.generate()
        population = tsp.get_population()
        generation_number += 1
        road = tsp.get_best_gene()
        best_fitness = tsp.get_best_fitness()
        if road:
            best_road = road
            best_distance = road.calculate_distance()
            generation_distance.append(best_distance)
            if best_distance_all is None:
                best_distance_all = best_distance
                best_road_ever = best_road
            elif best_distance_all is not None and best_distance_all >= best_distance:
                best_distance_all = best_distance
                best_road_ever = best_road

    # display Best
    draw_cities(cities)
    draw_roads(best_road, color=(0, 0, 255))
    draw_text(" Best in generation:" + str(generation_number), (best_panel[0], best_panel[1]))

    # display best ever
    draw_cities(cities, offset=(update_panel[0], update_panel[1]))
    draw_roads(best_road_ever, color=(0, 255, 0), offset=(update_panel[0], update_panel[1]))
    s = "     Distance = " + (str(best_distance_all) if best_distance_all else "Unknown")
    draw_text("Best ever" + s, (update_panel[0], update_panel[1]))

    # display graph
    pop_graph.clear()
    pop_graph.ax.hist(tsp.get_fitness(), bins=20)
    pop_graph.ax.set_title("Frequency distribution")
    pop_graph.ax.set_xlabel("fitness")
    pop_graph.ax.set_ylabel("Frequency")
    pop_graph.show()

    # display graph
    gen_graph.clear()
    gen_graph.ax.plot(list(range(1, len(generation_distance) + 1)), generation_distance)
    gen_graph.ax.set_title("Best distance (y) vs generation(x)")
    gen_graph.ax.set_xlabel("Generation")
    gen_graph.ax.set_ylabel("Best Distance")
    gen_graph.show()

    pygame.display.update()

pygame.quit()
