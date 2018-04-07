"""
This class contains all the user preferences about the terrain to generate.
For now, the user needs to modify their preferences in this class; eventually,
it should be able to parse from a .txt file.
"""

#  Size of terrain space
HEIGHT = 512
WIDTH = 512

#  Perlin noise preferences
OCTAVES = 8

CELL_LENGTH = 16

'''
No-op at the moment
Update the preferenes from the file
@ param configFile the .txt file with the preferences
'''
def updateFromConfig(configFile):
    #  TODO: parse the preferences from a config file
    raise NotImplementedError()

'''
Genetic Algorithm Parameters
'''
POP = 150
NGEN = 50
MU = 50
LAMBDA = 75
CXPB = 0.65
MUTPB = 0.25
SHAPE = (HEIGHT, WIDTH)
PKW = {"octaves": OCTAVES}  # partial function kwargs
WEIGHTS = (10, -1, -2, -2)  # 4-tuple of real numbers (positive for maximize, negative for minimize)

'''
Whether or not to parallelize the computation
Note: may decrease performance due to communication overhead
'''
parallelize = False

'''
Postprocessing parameters
'''
FILTER_SIZE = 12