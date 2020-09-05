import numpy as np
import pandas as pd
import math


class DTLearner:
	def author(self):
		return 'tkim338'

	def __init__(self, leaf_size=1, verbose=False):
		self.tree = np.empty((1, 5)) # columns: split_feature | split_val | left_node_index | right_node_index | leaf_val
		self.leaf_size = leaf_size
		self.verbose = verbose

	def add_evidence(self, x_train, y_train):
		self.split(0, x_train, y_train)

	def split(self, node_index, X, y):
		if len(y) <= self.leaf_size:
			self.tree[node_index] = [None, None, None, None, np.median(y)]
			return

		split_attribute, split_value = find_best_split_feature(X, y)
		X_left, X_right, y_left, y_right = partition_classes(X, y, split_attribute, split_value)

		self.tree = np.append(self.tree, np.empty((1,5)), axis=0)
		left_node_index = len(self.tree)-1

		self.tree = np.append(self.tree, np.empty((1,5)), axis=0)
		right_node_index = len(self.tree)-1

		self.tree[node_index] = np.array([split_attribute, split_value, left_node_index, right_node_index, None])

		self.split(left_node_index, X_left, y_left)
		self.split(right_node_index, X_right, y_right)

	def traverse(self, record, node_index):
		if not np.isnan(self.tree[node_index, 4]): # if not NaN, is leaf node
			return self.tree[node_index, 4]

		split_attribute = int(self.tree[node_index, 0])
		split_value = int(self.tree[node_index, 1])

		if record[split_attribute] <= split_value:
			return self.traverse(record, int(self.tree[node_index, 2]))
		else:
			return self.traverse(record, int(self.tree[node_index, 3]))

	def query(self, Xtest):
		Y = []
		for x in Xtest:
			Y.append(self.traverse(x, 0))
		return Y


def find_best_split_feature(X, y):
	num_features = X.shape[1]
	max_corr = None
	max_corr_col = None
	for i in range(0, num_features):
		curr_corr = np.max(np.abs(np.corrcoef(X[:,i], y)))
		if max_corr is None:
			max_corr = curr_corr
			max_corr_col = i
		else:
			if curr_corr > max_corr:
				max_corr = curr_corr
				max_corr_col = i
	return max_corr_col, np.median(X[:,max_corr_col])


def partition_classes(X, y, split_attribute, split_val):
	X_left = X[X[:, split_attribute] < split_val, :]
	X_right = X[X[:, split_attribute] > split_val, :]
	y_left = y[X[:, split_attribute] < split_val]
	y_right = y[X[:, split_attribute] > split_val]

	# values == median should be randomly assigned
	median_X = X[X[:, split_attribute] == split_val, :]
	median_Y = y[X[:, split_attribute] == split_val]
	random_assignment = np.random.choice([1, 0], len(median_Y))

	X_left = np.append(X_left, median_X[random_assignment == 1], axis=0)
	X_right = np.append(X_right, median_X[random_assignment == 0], axis=0)
	y_left = np.append(y_left, median_Y[random_assignment == 1])
	y_right = np.append(y_right, median_Y[random_assignment == 0])

	return X_left, X_right, y_left, y_right

# xt = np.array([[4, 2],[6, 4],[7, 7]])
# yt = np.array([1,2,3])
# ls = 1
# dt = DTLearner(leaf_size=ls, verbose=False)
# dt.add_evidence(xt, yt)
# print(dt.query([[5,4]]))

# alldata = np.genfromtxt('D:/Programming/CS7646/assess_learners/Data/Istanbul.csv', delimiter=",")
# # Skip the date column and header row if we're working on Istanbul data
# alldata = alldata[1:, 1:]
# datasize = alldata.shape[0]
# cutoff = int(datasize * 0.6)
# permutation = np.random.permutation(alldata.shape[0])
# col_permutation = np.random.permutation(alldata.shape[1] - 1)
# train_data = alldata[permutation[:cutoff], :]
# # train_x = train_data[:,:-1]
# train_x = train_data[:, col_permutation]
# train_y = train_data[:, -1]
# test_data = alldata[permutation[cutoff:], :]
# # test_x = test_data[:,:-1]
# test_x = test_data[:, col_permutation]
# test_y = test_data[:, -1]
#
# learner = DTLearner(leaf_size=1, verbose=False)
# learner.add_evidence(train_x, train_y)
# insample = learner.query(train_x)
# outsample = learner.query(test_x)


inf = open('./Data/ripple.csv')
data = np.array(
	[list(map(float, s.strip().split(","))) for s in inf.readlines()]
)

# compute how much of the data is training and testing
train_rows = int(0.6 * data.shape[0])
test_rows = data.shape[0] - train_rows

# separate out training and testing data
train_x = data[:train_rows, 0:-1]
train_y = data[:train_rows, -1]
test_x = data[train_rows:, 0:-1]
test_y = data[train_rows:, -1]

print(f"{test_x.shape}")
print(f"{test_y.shape}")

# create a learner and train it
# learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner
learner = DTLearner(verbose=True)
learner.add_evidence(train_x, train_y)  # train it
print(learner.author())

# evaluate in sample
pred_y = learner.query(train_x)  # get the predictions
rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
print()
print("In sample results")
print(f"RMSE: {rmse}")
c = np.corrcoef(pred_y, y=train_y)
print(f"corr: {c[0, 1]}")

# evaluate out of sample
pred_y = learner.query(test_x)  # get the predictions
rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
print()
print("Out of sample results")
print(f"RMSE: {rmse}")
c = np.corrcoef(pred_y, y=test_y)
print(f"corr: {c[0, 1]}")
