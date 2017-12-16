%load_pca
%%%%%%%%%%%%%%%%%%%%%%%%%%
year_to_load=1;
train_not_dev=false;
%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 
% bayes_matrix=zeros(30,10000);
% err_bayes_matrix=zeros(20,30,10000);
% 
% 
% tic;
% for year=1:30
%     fprintf('Year %d ...\n',year);
%     read_a_year    
%     fprintf('scanned!\n');
%     bayes_matrix(year,:)=mean(year_features);    
%     totn=size(year_features,1);
%     for por=1:20
%        err_bayes_matrix(por,year,:)=mean(year_features(1:round(por*totn/20),:)); 
%     end
%     ttoc=toc;
%     fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
%  end
%% 
%%%%%%%%%%%%%load dev

dev_data=zeros(30,1200,10000);
tic;
for year=1:30
   fprintf('Year %d ...\n',year);
   read_a_year    
   fprintf('scanned!\n');
   dev_data(year,:,:) = year_features(1:1200,:);
   ttoc=toc;
   fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
end


