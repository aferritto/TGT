import numpy as np


def init_once(cls, fn):
    """
    :param cls: a class to instantiate
    :param fn: a function of no arguments to call and pass to cls
    :return: cls(fn())
    """

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
    mult = 20 * int(mult)
    mask = mult * np.random.rand(*individual.shape)

    individual[...] = individual + mask
    return individual,


def score(individual: np.ndarray) -> tuple:
    """
    :param individual: candidate to score
    :return: tuple of scores for the individual
    """

    metrics = [loc_glbl_var, sea_level, bedrock, mountains]
    result = tuple(metric(individual) for metric in metrics)
    return result


def loc_glbl_var(individual: np.ndarray) -> float:
    """
    Computes score as function of quadrant and global variance
    :param individual: candidate to score
    :return: sum of quadrant variance - 5*global variance
    """

    mids = tuple(map(lambda x: int(x/2), individual.shape))
    s1 = np.var(individual[:mids[0], :mids[1]])
    s2 = np.var(individual[:mids[0], mids[1]:])
    s3 = np.var(individual[mids[0]:, :mids[1]])
    s4 = np.var(individual[mids[0]:, mids[1]:])
    result = s1 + s2 + s3 + s4 - 10*np.var(individual[...])
    return float(result)


def sea_level(individual: np.ndarray, target: float=25.0) ->float:
    """
    :param individual: candidate to score
    :param target: ideal sea level height
    :return: |individual - target|_2
    """

    return np.linalg.norm(individual - target)


def bedrock(individual: np.ndarray, target: float=-2000.0) -> float:
    """
    :param individual: candidate to score
    :param target: ideal bedrock height
    :return: |min(individual) - target|_2
    """

    return np.linalg.norm(np.min(individual) - target)


def mountains(individual: np.ndarray, target: float=3500.0) -> float:
    """
    :param individual: candidate to score
    :param target: ideal mountains heights
    :return: |max(individual) - target|_2
    """

    return np.linalg.norm(np.max(individual) - target)
