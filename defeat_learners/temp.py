import numpy as np
from LinRegLearner import LinRegLearner
from DTLearner import DTLearner

# x = np.random.random((100, 5)) * 10
# y1 = np.array([x[:, 0] ** 2]).T
# y2 = np.random.random((100, 1)) * 1
#
# lr = LinRegLearner()
# dt = DTLearner()
#
# lr.add_evidence(x,y1)
# dt.add_evidence(x,y2)


# x0 = np.zeros((100, 2))
# y0 = np.random.random(size=(100,)) * 200 - 100
# x1 = np.random.random((100, 2)) * 10
# y1 = x1[:, 0] ** 2

x0 = np.zeros((100, 2))
y0 = np.random.random(size=(100,)) * 200 - 100
x1 = np.random.random((100, 2)) * 10
y1 = np.random.random((100,)) * 1

print()