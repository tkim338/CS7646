import BagLearner
import LinRegLearner
class InsaneLearner(BagLearner.BagLearner):
	def author(self):
		return 'tkim338'
	def __init__(self, verbose=False):
		super().__init__(learner=BagLearner.BagLearner, kwargs={'learner':LinRegLearner.LinRegLearner, 'kwargs':{'verbose':verbose}, 'bags':20}, bags=20)