#!/usr/bin/env python

import svmutil

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
	y, x = svmutil.svm_read_problem('char_recon')


	prob  = svmutil.svm_problem(y[:2000], x[:2000])
	param = svmutil.svm_parameter('-t 2 -q')

	m = svmutil.svm_train(prob, param)
	p_label, p_acc, p_val = svmutil.svm_predict(y[2000:], x[2000:], m)

if __name__ == '__main__':
		main()	