'''
The is the main file for the project.
A user should be able to run this file after
setting desired parameters and terrain should be generated.
'''
from tgt import heightmapGenerator as hmg
from tgt import visualizer as vis
from tgt import preferences as pref

def main():
    pref.updateFromConfig("dummyfile.txt") # no-op for now
    heightmap = hmg.generate(pref.HEIGHT, pref.WIDTH, pref.OCTAVES)
    vis.plot2D(heightmap, False)
    vis.plot3D(heightmap, False)

if __name__ == '__main__': main()
