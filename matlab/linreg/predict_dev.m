%load('../data/dev_data.mat');
load('../data/theta.mat');
eps=0.0000001;
predicted_linreg=zeros(30,1200);
tic;
for year = 1 : 30 
    fprintf('Year %d ...',year);
    year_features=[ones(1200,1) reshape(dev_data(year,:,:),[1200,10000])];
    predicted_linreg(year,:)=year_features*theta/12+1;
    fprintf('scanned!\n');
    ttoc=toc;
    fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
end
