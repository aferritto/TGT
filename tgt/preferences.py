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
POP = 300
NGEN = 10
MU = 50
LAMBDA = 100
CXPB = 0.65
MUTPB = 0.25
SHAPE = (HEIGHT, WIDTH)
PKW = {} # partial function kwargs

'''
Whether or not to parallelize the computation
Note: may decrease performance due to communication overhead
'''
parallelize = False