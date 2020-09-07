import numpy as np

class BagLearner:
	def author(self):
		return 'tkim338'

	def __init__(self, learner, kwargs, bags=1, boost=False, verbose=False):
		self.boost = boost
		self.verbose = verbose
		self.learners = []
		for i in range(0, bags):
			self.learners.append(learner(**kwargs))

	def add_evidence(self, x_train, y_train):
		bag_size = len(y_train)
		num_features = x_train.shape[1]
		x_subset = np.empty((0, num_features))
		y_subset = np.empty((0, 1))

		for i in range(0, bag_size):
			rand_ind = np.random.randint(0, bag_size)
			x_subset = np.append(x_subset, [x_train[rand_ind, :]], axis=0)
			y_subset = np.append(y_subset, y_train[rand_ind])

		for learner in self.learners:
			learner.add_evidence(x_subset, y_subset)

	def query(self, Xtest):
		samples = np.empty((0, Xtest.shape[0]))
		for learner in self.learners:
			samples = np.append(samples, [learner.query(Xtest)], axis=0)
		results = np.mean(samples, axis=0)
		return results