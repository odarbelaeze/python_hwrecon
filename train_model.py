#!/usr/bin/env python

import svmutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class GammaCPair(object):
	"""docstring for GammaCPair"""
	def __init__(self, gamma, C):
		super(GammaCPair, self).__init__()
		self.gamma = gamma
		self.C = C
	def __str__(self):
		return 'G{0}C{1}'.format(self.gamma, self.C)
	def get_parameter(self):
		return '-t 2 -q -gamma {0} -C {1}'

def main():
	y, x = svmutil.svm_read_problem("char_recon_shuffled.db")
	t_examples, t_acc, v_acc = svm_learning_curve(x, y)
	plt.plot(t_examples, t_acc, label = "train accuracy")
	plt.plot(t_examples, v_acc, label = "validation accuracy")
	plt.legend()
	plt.grid(True)
	plt.savefig("learning_curve_C100.png")

def svm_learning_curve(x, y):
	m = len(y)
	n = len(x)
	steep = m / 100;

	training_examples = []
	train_accuracy = []
	validation_accuracy = []

	for i in range(steep, m, steep):
		prob  = svmutil.svm_problem(y[:i], x[:i])
		param = svmutil.svm_parameter('-t 2 -q -c 0.01')
		m = svmutil.svm_train(prob, param)
		
		p_label_train, p_acc_train, p_val_train = svmutil.svm_predict(y[:i], x[:i], m)
		p_label_validation, p_acc_validation, p_val_validation = svmutil.svm_predict(y[i:], x[i:], m)
		print p_acc_train[0], "\t", p_acc_validation[0], "\n"

		training_examples.append(i)
		train_accuracy.append(p_acc_train[0])
		validation_accuracy.append(p_acc_validation[0])

	return training_examples, train_accuracy, validation_accuracy

def get_cross_val(x, y, gamma_c):
	pass


if __name__ == '__main__':
		main()
