import pygame, sys
import numpy as np
import scipy as sp
import pylab as pl
import svmutil as sv
pygame.init()

LETTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "Y",
    "Z"
]


def predecir(surface, model):
    I = pygame.surfarray.array3d(surface)
    J = I.astype(np.float32).sum(axis = -1); J /= 3.0
    J = np.transpose(J)

    x_mask = [i for i in range(len(J.sum(axis = 0))) if J.sum(axis = 0)[i]]
    y_mask = [i for i in range(len(J.sum(axis = 1))) if J.sum(axis = 1)[i]]

    range_x = max(x_mask) - min(x_mask)
    range_y = max(y_mask) - min(y_mask)
    
    if not range_x > range_y:
        t_mask = y_mask
        y_mask = x_mask
        x_mask = t_mask
        range_x = max(x_mask) - min(x_mask)
        range_y = max(y_mask) - min(y_mask)

    min_h = min(x_mask);
    max_h = max(x_mask);
    min_v = max(np.ceil(np.mean([max(y_mask), min(y_mask)]) - range_x / 2.0), 1);
    max_v = min(np.ceil(np.mean([max(y_mask), min(y_mask)]) + range_x / 2.0), surface.get_width());

    x = J[min_h: max_h, min_v: max_v]
    x = sp.misc.imresize(x, [20, 20], 'bicubic')
    x = list(x.rehape(-1, order = 'F'))

    a = sv.svm_predict([-1], [x], model)

    return LETTERS(a[0][0])


def main():

    model = sv.svm_load_model("model")

    size = width, height = 400, 400

    black = 0,0,0
    white = 255,255,255

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Reconocedor de caracteres.")

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)
        pygame.display.flip()

if __name__ == '__main__':
    main()



