import pygame, sys
import numpy as np
import scipy as sp
import svmutil as sv
pygame.init()

DEBUG = False

if DEBUG:
    import pylab as pl

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
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z"
]

print len(LETTERS)

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
    x = sp.misc.imresize(x, [20, 20])

    if DEBUG:
        pl.imshow(x, cmap = pl.cm.gray)
        pl.show()

    x = list(x.reshape(-1, order = 'F'))

    a = sv.svm_predict([-1], [x], model)

    return LETTERS[int(a[0][0]) - 1]


def main():

    model = sv.svm_load_model("model")

    size = width, height = 400, 400

    black = 0,0,0
    white = 255,255,255

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("HW_Recon | Ingrese un caracter.")

    data_flag = False
    last_pos = []


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        mg = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()

        if mg == (0,0,1) and data_flag:
            a = predecir(screen, model)
            print a
            pygame.display.set_caption("HW_Recon| Letra: {0}".format(a))

        if mg == (1,0,0) and not last_pos:
            last_pos = mpos
            data_flag = True

        if mg == (1,0,0) and last_pos:
            if np.linalg.norm(np.array(mpos) - np.array(last_pos)) < 20:
                pygame.draw.line(screen, white, last_pos, mpos, 30)
            last_pos = mpos

        if mg == (0,1,0) and data_flag:
            data_flag = False
            last_pos = []
            screen.fill(black)
            pygame.display.set_caption("HW_Recon | Ingrese un caracter.")

        pygame.display.flip()

if __name__ == '__main__':
    main()



