""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		     		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		     		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		     		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		     		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		     		  		  		    	 		 		   		 		  
or edited.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		     		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		     		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import math  		  	   		     		  		  		    	 		 		   		 		  
import sys  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import LinRegLearner as lrl  		  	   		     		  		  		    	 		 		   		 		  
import DTLearner
import RTLearner
import BagLearner
import InsaneLearner

import matplotlib.pyplot as plt
import time

if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)

    data = np.genfromtxt(sys.argv[1], delimiter=",")
    # Skip the date column and header row if we're working on Istanbul data
    if "Istanbul.csv" in sys.argv[1]:
        data = data[1:, 1:]
  		  	   		     		  		  		    	 		 		   		 		  
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
    learner = DTLearner.DTLearner(verbose=True)
    # learner = RTLearner.RTLearner(verbose=True)
    # learner = BagLearner.BagLearner(learner=DTLearner.DTLearner, kwargs={'leaf_size':10, 'verbose':False}, bags=10)
    # learner = InsaneLearner.InsaneLearner(verbose=False)
    learner.add_evidence(train_x, train_y)  # train it  		  	   		     		  		  		    	 		 		   		 		  
    print(learner.author())  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # evaluate in sample  		  	   		     		  		  		    	 		 		   		 		  
    pred_y = learner.query(train_x)  # get the predictions  		  	   		     		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print("In sample results")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		     		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=train_y)  		  	   		     		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # evaluate out of sample  		  	   		     		  		  		    	 		 		   		 		  
    pred_y = learner.query(test_x)  # get the predictions  		  	   		     		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print("Out of sample results")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		     		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=test_y)  		  	   		     		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")

    # Experiment 1
    def experiment1():
        max_leaf = 100
        samp_dt_train = []
        samp_dt_test = []
        for i in range(1, max_leaf): # leaf size
            learner = DTLearner.DTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_train = learner.query(train_x)
            pred_y_test = learner.query(test_x)
            samp_dt_train.append(math.sqrt(((train_y - pred_y_train) ** 2).sum() / train_y.shape[0]))
            samp_dt_test.append(math.sqrt(((test_y - pred_y_test) ** 2).sum() / test_y.shape[0]))
        plt.plot(samp_dt_train, 'b--')
        plt.plot(samp_dt_test, 'b-')

        samp_rt_train = []
        samp_rt_test = []
        for i in range(1, max_leaf): # leaf size
            learner = RTLearner.RTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_train = learner.query(train_x)
            pred_y_test = learner.query(test_x)
            samp_rt_train.append(math.sqrt(((train_y - pred_y_train) ** 2).sum() / train_y.shape[0]))
            samp_rt_test.append(math.sqrt(((test_y - pred_y_test) ** 2).sum() / test_y.shape[0]))
        plt.plot(samp_rt_train, 'r--')
        plt.plot(samp_rt_test, 'r-')

        plt.legend(['DTLearner (in-sample)', 'DTLearner (out-sample)', 'RTLearner (in-sample)', 'RTLearner (out-sample)'])
        plt.gca().set_xlabel('Leaf size')
        plt.gca().set_ylabel('RSME')
        plt.gca().set_title('Effects of leaf size on overfitting')
        plt.savefig('leaf_size_overfitting.png')

    def experiment2():
        bag_sizes = [1,2,5,10]
        max_leaf = 50
        samp_bag_dt = np.empty((len(bag_sizes), max_leaf-1))
        for i in range(0, len(bag_sizes)):
            for j in range(1, max_leaf):
                learner = BagLearner.BagLearner(learner=DTLearner.DTLearner, kwargs={'leaf_size': j, 'verbose': False}, bags=bag_sizes[i])
                learner.add_evidence(train_x, train_y)
                pred_y = learner.query(test_x)
                samp_bag_dt[i,j-1] = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        plt.plot(samp_bag_dt.T)
        legend_labels = []
        for b in bag_sizes:
            legend_labels.append(str(b) + ' bag(s)')
        plt.legend(legend_labels)

        plt.gca().set_xlabel('Leaf size')
        plt.gca().set_ylabel('RSME')
        plt.gca().set_title('Effects of bagging on overfitting')
        plt.savefig('bagging_overfitting.png')

    def experiment3_a():
        max_leaf = 50
        samp_dt_train = []
        for i in range(1, max_leaf):  # leaf size
            learner = DTLearner.DTLearner(leaf_size=i, verbose=False)
            t0 = time.time()
            learner.add_evidence(train_x, train_y)
            t1 = time.time()
            samp_dt_train.append(t1 - t0)
        plt.plot(samp_dt_train, 'b')

        samp_rt_train = []
        for i in range(1, max_leaf):  # leaf size
            learner = RTLearner.RTLearner(leaf_size=i, verbose=False)
            t0 = time.time()
            learner.add_evidence(train_x, train_y)
            t1 = time.time()
            samp_rt_train.append(t1 - t0)
        plt.plot(samp_rt_train, 'r')

        plt.legend(['DTLearner', 'RTLearner'])
        plt.gca().set_xlabel('Leaf size')
        plt.gca().set_ylabel('Training time [sec]')
        plt.gca().set_title('Tree building speed')
        plt.savefig('dt_vs_rt_time.png')

    def tree_depth(array, index):
        index_left = array[index, 2]
        index_right = array[index, 3]
        if np.isnan(index_left) and np.isnan(index_right):
            return 1
        elif np.isnan(index_left):
            return 1+tree_depth(array, int(index_right))
        elif np.isnan(index_right):
            return 1+tree_depth(array, int(index_left))
        return 1+max(tree_depth(array, int(index_left)), tree_depth(array, int(index_right)))

    def experiment3_b():
        max_leaf = 50
        samp_dt_train = []
        for i in range(1, max_leaf):  # leaf size
            learner = DTLearner.DTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            samp_dt_train.append(tree_depth(learner.tree, 0))
        plt.plot(samp_dt_train, 'b')

        samp_rt_train = []
        for i in range(1, max_leaf):  # leaf size
            learner = RTLearner.RTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            samp_rt_train.append(tree_depth(learner.tree, 0))
        plt.plot(samp_rt_train, 'r')

        plt.legend(['DTLearner', 'RTLearner'])
        plt.gca().set_xlabel('Leaf size')
        plt.gca().set_ylabel('Depth [nodes]')
        plt.gca().set_title('Tree depth')
        plt.savefig('dt_vs_rt_depth.png')

    # experiment1()
    # experiment2()
    # experiment3_a()
    experiment3_b()