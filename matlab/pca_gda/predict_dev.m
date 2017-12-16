%% 
eps=0.0000001;
sc=1:10000;
tic;
predicted_PCA=zeros(30,1200,30);

for year = 1 : 30
    fprintf('Year %d ...',year);
    for art=1:200
        FV=reshape(dev_data(year,art,:),[1 10000]);
        predicted_PCA(year,art,:)=...
        -sum(...
        (bayes_matrix_mean(:,sc)-FV(sc)).*(bayes_matrix_mean(:,sc)-FV(sc))...
        ./(gaussian_disc_std(sc).*gaussian_disc_std(sc))...
        ... ./latent(sc)'...
        ,2);
    end
    fprintf('scanned!\n');
    ttoc=toc;
    fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
end
%% 
plot_prediced

% load('../data/mean_value_for_exp.mat');
% load('../data/dev_data.mat');
% load('../data/mean_value_for_exp.mat');




% eps=0.0000001;
% mod_bayes_matrix=bayes_matrix+eps;
% select_word=1:10000;
% predicted_logbayes=zeros(30,1200,30);
% tic;
% for year = 1 : 30
%     fprintf('Year %d ...',year);
%     year_features=reshape(dev_data(year,:,:),[1200,10000]);
%     for art=1:1200
%         predicted_logbayes(year,art,:)=...
%             sum(...
%             -(1./mod_bayes_matrix(:,select_word)).*year_features(art,select_word)...-log(mod_bayes_matrix(:,select_word))...
%             ,2);
%     end
%     fprintf('scanned!\n');
%     ttoc=toc;
%     fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
% end
% plot_prediced
