import numpy as np
import pandas as pd
import math

import util


class RTLearner:
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

		if len(y_left) == 0 or len(y_right) == 0:
			self.tree[node_index] = [None, None, None, None, np.median(y)]
			return

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
		split_value = self.tree[node_index, 1]

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
	max_corr_col = np.random.randint(0, num_features)
	return max_corr_col, np.median(X[:,max_corr_col])

def partition_classes(X, y, split_attribute, split_val):
	X_left = X[X[:, split_attribute] <= split_val, :]
	X_right = X[X[:, split_attribute] > split_val, :]
	y_left = y[X[:, split_attribute] <= split_val]
	y_right = y[X[:, split_attribute] > split_val]

	return X_left, X_right, y_left, y_right
