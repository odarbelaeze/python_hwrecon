#!/usr/bin/env python

import svmutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np

class GammaCPair(object):
    """docstring for GammaCPair"""
    def __init__(self, gamma, C):
        super(GammaCPair, self).__init__()
        self.gamma = gamma
        self.C = C
    def __str__(self):
        return 'G{0} C{1}'.format(self.gamma, self.C)
    def get_parameter(self):
        return '-t 2 -q -gamma {0} -C {1}'

def main():
    y, x = svmutil.svm_read_problem("char_recon_shuffled.db")
    x_train = x[:1800]
    y_train = y[:1800]
    x_val = x[1800:]
    y_val = y[1800:]

    gamma_c_pairs = [GammaCPair(1.0 / (2.0 * (3.0 ** log_sigma) ** 2), 3.0 ** log_C)
                     for log_sigma in [7]
                     for log_C     in [3]
                    ]

    log_log_pairs = [[log_sigma, log_C]
                     for log_sigma in np.arange(6, 10, 0.5)
                     for log_C     in np.arange(0, 5, 0.5)
                    ]

    def cv(gamma_c):
        return get_cross_val(x_train, y_train, x_val, y_val, gamma_c)

    cross_val = []

    for gamma_c in gamma_c_pairs:
        cross_val.append(cv(gamma_c))

    f = open("gamma_c", "w")
    for i in range(len(gamma_c_pairs)):
        f.write("{0}   {1}   {2}\n".format(log_log_pairs[i][0], log_log_pairs[i][1], cross_val[i]))
    f.close()

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

def get_cross_val(x, y, x_val, y_val, gamma_c):
    prob  = svmutil.svm_problem(y, x)
    param = svmutil.svm_parameter('-t 2 -q -c {0} -g {1}'.format(gamma_c.C, gamma_c.gamma))
    m = svmutil.svm_train(prob, param)

    svmutil.svm_save_model("model", m)

    p_label_validation, p_acc_validation, p_val_validation = svmutil.svm_predict(y_val, x_val, m)

    return p_acc_validation[0]


if __name__ == '__main__':
		main()
