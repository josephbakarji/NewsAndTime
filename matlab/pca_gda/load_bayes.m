%load_pca
%%%%%%%%%%%%%%%%%%%%%%%%%%
year_to_load=1;
train_not_dev=true;
%%%%%%%%%%%%%%%%%%%%%%%%%%
bayes_matrix_mean=zeros(30,10000);
bayes_matrix_std =zeros(30,10000);
tic;
for year=1:30
   fprintf('Year %d ...',year);
   read_a_year    
   fprintf('scanned!\n');
   year_features=(year_features-mu)*coeff;
   
   bayes_matrix_mean(year,:) = mean(year_features);
   
   
   bayes_matrix_std (year,:) = std (year_features);
   
   ttoc=toc;
   fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
end
save('../data/bayes_matrix_mean.mat','bayes_matrix_mean');
save('../data/bayes_matrix_std.mat' ,'bayes_matrix_std');
%%%%%%%%%%%%%load dev
% 
% dev_data=zeros(30,1200,10000);
% tic;
% for year=1:30
%    fprintf('Year %d ...\n',year);
%    read_a_year    
%    fprintf('scanned!\n');
%    dev_data(year,:,:) = year_features(1:1200,:);
%    ttoc=toc;
%    fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
% end

%% 
% for year = 1 : 30
%     fprintf('Year %d ...',year);
%     year_features=reshape(dev_data(year,:,:),[1200,10000]);
%     dev_data(year,:,:)=(year_features-mu)*coeff;
%     fprintf('scanned!\n');
%     ttoc=toc;
%     fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
% end
%% 







