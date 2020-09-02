import numpy as np
import pandas as pd

class RTLearner:
	def __init__(self, leaf_size = 1, verbose = False):
		self.leaf_size = leaf_size
		self.verbose = verbose
		self.x_train = None
		self.y_train = None

	def add_evidence(self, x_train, y_train):
		self.x_train = x_train
		self.y_train = y_train
		# something here
	
	def query(self, x_test):
		x_test
		# something here
		
	def find_best_split_feature(self):
		num_features = self.x_train.shape[1]
		max_corr = None
		max_corr_col = None
		for i in range(0, num_features):
			curr_corr = np.corrcoef(self.x_train[0][:], self.y_train)
			if max_corr == None:
				max_corr = curr_corr
				max_corr_col = i
			else:
				if curr_corr > max_corr:
					max_corr = curr_corr
					max_corr_col = i
		return max_corr_col