import numpy as np
import pandas as pd


class DTLearner:
	def __init__(self, leaf_size=1, verbose=False):
		self.tree = {}
		self.leaf_size = leaf_size
		self.verbose = verbose
		# self.x_train = None
		# self.y_train = None

	def add_evidence(self, x_train, y_train):
		# self.x_train = x_train
		# self.y_train = y_train
		self.build_tree(x_train, y_train)

	def split(self, X, y):
		if len(y) <= self.leaf_size:
			node = {"type": "end_node",
			        "value": np.median(y)}
			return node
		# if depth < 0:
		# 	return 0
		#
		# if all(yi == 0 for yi in y):
		# 	return 0
		# elif all(yi == 1 for yi in y):
		# 	return 1

		# max_info_gain = 0
		split_attribute, split_value = find_best_split_feature(X, y)

		if split_value is None:  # no info gain
			return y[0]

		X_left, X_right, y_left, y_right = partition_classes(X, y, split_attribute, split_value)

		# if X_left == None:  # should rarely happen
		# 	return 0

		new_left_leaf = self.split(X_left, y_left)
		new_right_leaf = self.split(X_right, y_right)

		node = {"left": new_left_leaf,
		        "right": new_right_leaf,
		        "split_attribute": split_attribute,
		        "split_value": split_value,
		        "type": "split_node"}
		return node

	def build_tree(self, X, y):
		self.tree = self.split(X, y)

	def traverse(self, record, node):
		if node["type"] == "end_node":
			return node["value"]
		# if node == 0:
		# 	return 0
		# elif node == 1:
		# 	return 1

		split_attribute = node["split_attribute"]
		split_value = node["split_value"]

		if record[split_attribute] <= split_value:
			return self.traverse(record, node["left"])
		else:
			return self.traverse(record, node["right"])

	def query(self, Xtest):
		Y = []
		for x in Xtest:
			Y.append(self.traverse(x, self.tree))
		return Y


def find_best_split_feature(X, y):
	num_features = X.shape[1]
	max_corr = None
	max_corr_col = None
	for i in range(0, num_features):
		curr_corr = np.max(np.abs(np.corrcoef(X[:,i], y)))
		if max_corr == None:
			max_corr = curr_corr
			max_corr_col = i
		else:
			if curr_corr > max_corr:
				max_corr = curr_corr
				max_corr_col = i
	return max_corr_col, np.median(X[:,max_corr_col])


def partition_classes(X, y, split_attribute, split_val):
	X_left = np.empty((0, X.shape[1]))
	X_right = np.empty((0, X.shape[1]))

	y_left = np.empty((0, 1))
	y_right = np.empty((0, 1))
	# if isinstance(split_val, str):  # split_attribute is categorical
	for i in range(len(y)):
		if X[i][split_attribute] <= split_val:
			X_left = np.append(X_left, [X[i]], axis=0) # X_left.append(X[i])
			y_left = np.append(y_left, y[i]) # y_left.append(y[i])
		else:
			X_right = np.append(X_right, [X[i]], axis=0) # X_right.append(X[i])
			y_right = np.append(y_right, y[i]) # y_right.append(y[i])
	# else:  # split_attribute is numeric
	# 	for i in range(len(y)):
	# 		if X[i][split_attribute] <= split_val:
	# 			X_left.append(X[i])
	# 			y_left.append(y[i])
	# 		else:
	# 			X_right.append(X[i])
	# 			y_right.append(y[i])

	return X_left, X_right, y_left, y_right

# xt = np.array([[4, 2],[6, 4],[7, 7]])
# yt = np.array([1,2,3])
# ls = 1
# dt = DTLearner(leaf_size=ls, verbose=False)
# dt.add_evidence(xt, yt)
# print(dt.query([[5,4]]))

alldata = np.genfromtxt('D:/Programming/CS7646/assess_learners/Data/Istanbul.csv', delimiter=",")
# Skip the date column and header row if we're working on Istanbul data
alldata = alldata[1:, 1:]
datasize = alldata.shape[0]
cutoff = int(datasize * 0.6)
permutation = np.random.permutation(alldata.shape[0])
col_permutation = np.random.permutation(alldata.shape[1] - 1)
train_data = alldata[permutation[:cutoff], :]
# train_x = train_data[:,:-1]
train_x = train_data[:, col_permutation]
train_y = train_data[:, -1]
test_data = alldata[permutation[cutoff:], :]
# test_x = test_data[:,:-1]
test_x = test_data[:, col_permutation]
test_y = test_data[:, -1]

# np.random.seed(seed)
# random.seed(seed)
learner = DTLearner(leaf_size=1, verbose=False)
learner.add_evidence(train_x, train_y)
insample = learner.query(train_x)
outsample = learner.query(test_x)