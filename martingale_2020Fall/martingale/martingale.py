""""""  		  	   		     		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
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
  		  	   		     		  		  		    	 		 		   		 		  
Student Name: Thomas Kim
GT User ID: tkim338
GT ID: 902871961
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def author():  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    return "tkim338"  # replace tb34 with your Georgia Tech username.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def gtid():  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    return 902871961  # replace with your GT ID number  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		     		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		     		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    result = False  		  	   		     		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		     		  		  		    	 		 		   		 		  
        result = True  		  	   		     		  		  		    	 		 		   		 		  
    return result  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def test_code():  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    win_prob = 18/38  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once  		  	   		     		  		  		    	 		 		   		 		  
    print(get_spin_result(win_prob))  # test the roulette spin  		  	   		     		  		  		    	 		 		   		 		  
    # add your code here to implement the experiments  		  	   		     		  		  		    	 		 		   		 		  

    # Experiment 1
    def run_sim():
        winnings = [0]

        bet = 1
        for i in range(1000):
            if winnings[-1] < 80:
                if get_spin_result(win_prob):
                    winnings.append(min(80, winnings[-1] + bet))
                else:
                    winnings.append(winnings[-1] - bet)
                    bet = bet * 2
            else:
                winnings.append(winnings[-1])
        return winnings

    def generate_figure_1():
        for i in range(10):
            w = run_sim()
            plt.plot(w)
        axes = set_plot_labels_experiment_1()
        axes.set_title("Multiple Runs")
        legend_labels = []
        for i in range(10):
            legend_labels.append('Run '+str(i+1))
        plt.legend(legend_labels)
        plt.savefig('./exp1_fig1.png')
        plt.clf()
    
    def generate_figure_2_3():
        history = []
        for i in range(1000):
            history.append(run_sim())

        np_arr_history = np.array(history)
        means = np.mean(np_arr_history, 0)
        std_devs = np.std(np_arr_history, 0)

        plt.plot(means)
        plt.plot(means + std_devs)
        plt.plot(means - std_devs)
        axes = set_plot_labels_experiment_1()
        axes.set_title("Mean Winnings")
        plt.legend(['Mean', 'Mean + Standard Deviation', 'Mean - Standard Deviation'])
        plt.savefig('./exp1_fig2.png')
        plt.clf()

        medians = np.median(np_arr_history, 0)
        plt.plot(medians)
        plt.plot(medians + std_devs)
        plt.plot(medians - std_devs)
        axes = set_plot_labels_experiment_1()
        axes.set_title("Median Winnings")
        plt.legend(['Median', 'Median + Standard Deviation', 'Median - Standard Deviation'])
        plt.savefig('./exp1_fig3.png')
        plt.clf()

    def set_plot_labels_experiment_1():
        axes = plt.gca()
        axes.set_xlim([0, 300])
        axes.set_ylim([-256, 100])
        axes.set_xlabel("Spin Number")
        axes.set_ylabel("Winnings")
        return axes

    generate_figure_1()
    generate_figure_2_3()

    # Experiment 2
    def run_sim_2():
        winnings = [0]

        bet = 1
        for i in range(1000):
            bet = min(bet, winnings[-1]+256)
            if -256 < winnings[-1] < 80:
                if get_spin_result(win_prob):
                    winnings.append(min(80, winnings[-1] + bet))
                else:
                    winnings.append(max(winnings[-1] - bet, -256))
                    bet = bet * 2
            else:
                winnings.append(winnings[-1])
        return winnings

    def generate_figure_4_5():
        history = []
        count = 0
        for i in range(1000):
            history.append(run_sim_2())
            if history[-1][-1] >=80:
                count += 1

        np_arr_history = np.array(history)
        means = np.mean(np_arr_history, 0)
        std_devs = np.std(np_arr_history, 0)

        plt.plot(means)
        plt.plot(means + std_devs)
        plt.plot(means - std_devs)
        axes = set_plot_labels_experiment_1()
        axes.set_title("Mean Winnings")
        plt.legend(['Mean', 'Mean + Standard Deviation', 'Mean - Standard Deviation'])
        plt.savefig('./exp2_fig4.png')
        plt.clf()

        medians = np.median(np_arr_history, 0)
        plt.plot(medians)
        plt.plot(medians + std_devs)
        plt.plot(medians - std_devs)
        axes = set_plot_labels_experiment_1()
        axes.set_title("Median Winnings")
        plt.legend(['Median', 'Median + Standard Deviation', 'Median - Standard Deviation'])
        plt.savefig('./exp2_fig5.png')
        plt.clf()

    generate_figure_4_5()
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    test_code()  		  	   		     		  		  		    	 		 		   		 		  
