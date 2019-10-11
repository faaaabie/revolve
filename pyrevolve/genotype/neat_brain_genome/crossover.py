import random

class NEATCrossoverConf:
    def __init__(self):
        self.mate_average = True
        self.interspecies_crossover = True


def standard_crossover(parents, NeatCrossoverConf, crossover_conf, lsystem_conf):
    """
    Creates an child (genotype) through crossover with two parents

    :param parents: parents brain genome to be used for crossover
    :param NeatCrossoverConf: NEAT genotype configuration object
    :param crossover_conf: CrossoverConfig for lsystem
    :return: genotype result of the crossover
    """
    assert len(parents) == 2

    crossover_attempt = random.uniform(0.0, 1.0)
    if crossover_attempt > crossover_conf.crossover_prob:
         new_genotype = parents[0].genotype._brain_genome
    else:
        mother = parents[0]
        father = parents[1]
        new_genotype = mother.Mate(father,
                                   NeatCrossoverConf.mate_average,
                                   NeatCrossoverConf.interspecies_crossover,
                                   lsystem_conf.neat.rng,
                                   lsystem_conf.neat.multineat_params
                                   )
    return new_genotype
