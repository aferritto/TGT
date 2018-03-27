import numpy as np


def init_once(cls, fn):

    return cls(fn())


def crossover(par1: np.ndarray, par2: np.ndarray) -> tuple:
    """
    :param par1: one parent
    :param par2: the other parent
    :return: children of the parents
    """
    tmp1 = par1.copy()
    tmp2 = par2.copy()
    par1[...] = tmp1 + tmp2
    par2[...] = tmp1 - tmp2
    return par2, par2


def mutate(individual: np.ndarray) -> tuple:
    """
    :param individual: candidate to mutate
    :return: mutated individual
    """

    mult = np.random.normal(0, np.sqrt(np.std(individual)))
    mult = int(mult)
    mask = mult * np.random.rand(*individual.shape)

    individual[...] = individual + mask
    return individual,


def score(individual: np.ndarray) -> tuple:
    """
    :param individual: candidate to score
    :return: tuple of scores for the individual
    """

    metrics = [loc_glbl_var, sea_level, bedrock, mountains]
    return tuple(metric(individual) for metric in metrics)


def loc_glbl_var(individual: np.ndarray):
    mids = list(map(lambda x: int(x/2), individual.shape))
    s1 = np.var(individual[:mids[0], :mids[1]])
    s2 = np.var(individual[:mids[0], mids[1]:])
    s3 = np.var(individual[mids[0]:, :mids[1]])
    s4 = np.var(individual[mids[0]:, mids[1]:])
    return s1 + s2 + s3 + s4 - 5*np.var(individual)


def sea_level(individual: np.ndarray, target: float=25.0) ->float:

    #return np.einsum('ij,ij->i', individual - target, individual - target)**0.5
    return np.linalg.norm(individual - target)


def bedrock(individual: np.ndarray, target: float=-2000.0) -> float:

    return np.linalg.norm(np.min(individual) - target)


def mountains(individal: np.ndarray, target: float=3500.0) -> float:

    return np.linalg.norm(np.max(individal) - target)