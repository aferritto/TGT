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
from tgt import preferences as prefs
from scipy.ndimage import uniform_filter
from tgt import helpers


init_rand = partial(heightmapGenerator.perlin_rand, *prefs.SHAPE, **prefs.PKW)

creator.create("FitnessMax", base.Fitness, weights=prefs.WEIGHTS)
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("individual", heightmapGenerator.init_once, creator.Individual, init_rand)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", helpers.score)
toolbox.register("mate", heightmapGenerator.breed)
toolbox.register("mutate", heightmapGenerator.mutate)
toolbox.register("select", tools.selNSGA2)


def main():
    """
    The main function of the TGT application
    :return: None
    """

    hof = tools.HallOfFame(1, similar=np.allclose)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    if prefs.parallelize:
        import multiprocessing
        print("Using parallelization on {0} logical processors.".format(multiprocessing.cpu_count()))
        pool = multiprocessing.Pool()
        toolbox.register("map", pool.map)
    else:
        print("Not using parallelism.  Set parallelize = True in preferences.py to enable.")

    pop = toolbox.population(n=prefs.POP)

    algorithms.eaMuCommaLambda(pop, toolbox, mu=prefs.MU, lambda_=prefs.LAMBDA, cxpb=prefs.CXPB, mutpb=prefs.MUTPB,
                               ngen=prefs.NGEN, stats=stats, halloffame=hof)

    X = np.arange(prefs.SHAPE[0])
    Y = np.arange(prefs.SHAPE[1])
    Z = np.asarray(hof.items[0][...])
    Z = uniform_filter(Z, size=prefs.FILTER_SIZE)

    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

if __name__ == '__main__':
    main()
