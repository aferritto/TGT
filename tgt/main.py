import numpy as np
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from functools import partial
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tgt import heightmapGenerator
from tgt import visualizer as vis
from tgt import preferences as pref
import tgt.preferences as pref

from tgt import helpers

ngen = 50
mu = 50
lmda = 100
cxpb = 0.7
mutpb = 0.2
shp = (pref.HEIGHT, pref.WIDTH)

## keywork arguments to fix
pkw = {}

init_rand = partial(heightmapGenerator.generate_basic_perlin_noise, *shp, **pkw)

creator.create("FitnessMax", base.Fitness, weights=(1,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
hof = tools.HallOfFame(3, similar=np.allclose)

toolbox.register("individual", heightmapGenerator.init_once, creator.Individual, init_rand)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", heightmapGenerator.score)
toolbox.register("mate", heightmapGenerator.breed)
toolbox.register("mutate", heightmapGenerator.mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)


def main():
    pop = toolbox.population(n=100)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=2, stats=stats, halloffame=hof)

    X = np.arange(shp[0])
    Y = np.arange(shp[1])
    # Z = np.ndarray(buffer=hof.items[0][...], shape=shp)
    Z = np.asarray(hof.items[0][...])
    # mlab.surf(Z)
    # mlab.show()

    # plt.imshow(Z, cmap='viridis')
    # plt.show()

    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
    """
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    im = ax2.imshow(Z, cmap='hot')
    fig2.show()
    """


if __name__ == '__main__':
    main()
#=======
'''
The is the main file for the project.
A user should be able to run this file after
setting desired parameters and terrain should be generated.
'''
'''from tgt import heightmapGenerator as hmg
from tgt import visualizer as vis
from tgt import preferences as pref

def main():
    pref.updateFromConfig("dummyfile.txt") # no-op for now
    heightmap = hmg.generate(pref.HEIGHT, pref.WIDTH, pref.OCTAVES)
    vis.plot2D(heightmap, False)
    vis.plot3D(heightmap, False)

if __name__ == '__main__': main()
>>>>>>> master'''
