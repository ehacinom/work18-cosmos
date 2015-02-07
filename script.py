#!/usr/local/bin/python


from cosmoscatalog import Cosmos


cos = Cosmos()
cos.process()
rgb = cos.color()

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='white', palette='muted')

g = sns.jointplot(rgb[0][0], rgb[0][1], kind="hex", size = 7, space=0)
#sns.jointplot(rgb[1][0], rgb[1][1], kind="hex")
#sns.jointplot(rgb[2][0], rgb[2][1], kind="hex")
#sns.jointplot(rgb[3][0], rgb[3][1], kind="hex")

#plt.tight_layout()


