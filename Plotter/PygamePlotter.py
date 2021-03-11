import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame

matplotlib.use("Agg")


def get_fig_size(size):
    dpi = plt.rcParams['figure.dpi']  # get the default dpi value
    return size[0] / dpi, size[1] / dpi  # saving the figure size


class Plotter:
    def __init__(self, screen, pos, size):
        self.pos = pos
        self.size = size
        self.fig = Figure(figsize=get_fig_size(size))
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.screen = screen

    def clear(self):
        self.ax.clear()

    def show(self):
        self.fig.tight_layout()
        self.canvas.draw()
        renderer = self.canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = self.canvas.get_width_height()
        img = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(img, (self.pos[0], self.pos[1]))
