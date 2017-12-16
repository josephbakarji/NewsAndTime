mu=load('../data/mu.mat');
fprintf('mu loaded\n');
latent=load('../data/latent_s.mat');
fprintf('latent loaded\n');
coeff=load('../data/coeff_s.mat');
fprintf('coeff loaded\n');

mu=mu.('average_vectors');
latent=latent.('latent_s');
coeff=coeff.('coeff_s');

clear average_vectors
clear latent_s
clear coeff_s



