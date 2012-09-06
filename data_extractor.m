% data_extractor.m

% data_extractor.m extrae los datos a partir de cada imagen
% y obtiene los archivos, x, y y labels, x es un archivo de
% m lineas donde m es el número de instancias de la base de
% datos y en cada linea, n numeros de punto flotante repre-
% sentando cada característica de la instancia.

% inicializador

clear('all');
clc;

num_files = 100;
num_instances_per_file = 26;
m = num_files * num_instances_per_file;
n = 20 * 20;

X = zeros(m, n);
y = zeros(m, 1);
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',...
          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',...
          'U', 'V', 'W', 'X', 'Y', 'Z']';

% Debug label

DEBUG = 0;

% ciclo sobre todas las imagenes disponibles


for i = 1:100,
    I = imread(sprintf('data/letras%d.png', i));
    
    for j = 0:25
        id = (i - 1) * 26 + j + 1;
        x = I(1 + 50 * j : 50 * (j + 1), 1:50);
        [k,l] = find(x > 0);

        if (range(k) > range(l))
            min_h = min(k);
            max_h = max(k);
            min_v = max(ceil(mean(l) - range(k) / 2), 1);
            max_v = min(ceil(mean(l) + range(k) / 2), 50);
        else
            t = l; l = k; k = t;
            min_h = min(k);
            max_h = max(k);
            min_v = max(ceil(mean(l) - range(k) / 2), 1);
            max_v = min(ceil(mean(l) + range(k) / 2), 50);
        end

        x = x(min_h: max_h, min_v: max_v);
        x = imresize(x, [20 20], 'bicubic');

        X(id, :) = x(:);
        y(id) = j + 1; 
    end
end

% clear used variables

clear x min_h min_v max_h max_v id num_files num_instances_per_file i j k l m n I t

% write .mat

save data.mat X y labels

% Write .txt data

save data.txt X -ascii
save labels.txt y -ascii