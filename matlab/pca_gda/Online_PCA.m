training_size=700;

%%%%%%%%%%%%%% compute the average. comment or uncomment
%%%%%%%%%%%%%% sum_vectors=zeros...
%sum_vectors=zeros(1,10000);
% fileID = fopen('./Data/3/AWarr_train.txt','r');
% for month=1:12*10
%     mini_batch_svd=zeros(700,10000);
%     for row = 1 : training_size
%         M=fscanf(fileID,'%d',10000);
%         su=sum(M);
%         if su<10
%             mini_batch_svd(row,:)=M*0;
%         else
%             mini_batch_svd(row,:)=M/su;
%         end
%         fscanf(fileID,'%d',1);        
%     end
%     fprintf('training data: month number %d scanned\n',month);
%     sum_vectors=sum_vectors+sum(mini_batch_svd);
% end
%%%%%%average_vector
%average_vectors=sum_vectors/(12*30*training_size);
%%%%%%%%% coeff_raw
% coeff_raw=zeros(10000,10000);
% for file=1:3
%     if file==1
%         fileID = fopen('./Data/1/AWarr_train.txt','r');
%     elseif file==2
%         fileID = fopen('./Data/2/AWarr_train.txt','r');
%     else
%         fileID = fopen('./Data/3/AWarr_train.txt','r');
%     end
%     for month=1:12*10
%         mini_batch_svd=zeros(700,10000);
%         for row = 1 : training_size
%             M=fscanf(fileID,'%d',10000);
%             su=sum(M);
%             if su<10
%                 mini_batch_svd(row,:)=M*0;
%             else
%                 mini_batch_svd(row,:)=M/su;
%             end
%             fscanf(fileID,'%d',1);        
%         end
%         fprintf('training data: month number %d scanned\n',month);
%         mini_batch_svd=mini_batch_svd-average_vectors;
%         coeff_raw=coeff_raw+mini_batch_svd'*mini_batch_svd;
%     end
% endc


% M=rand(100,3);
% M1=M-sum(M)/100;
% M1=M1./ (vecnorm(M1)/10);
% 
% [V D]= eig(M1'*M1);
% V1=zeros(3);
% for row=1:3
%     for col=1:3
%         Vmod(row,col)=V(row,4-col);
%     end
% end
% [V1 sc latent]= pca(M1);
% 
% [V1./Vmod]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Creates coeff
% pca_numwords=10000;
% [coeff , latent]= eig(coeff_raw(1:pca_numwords,1:pca_numwords)'*coeff_raw(1:pca_numwords,1:pca_numwords));
% 
% latent=diag(latent);
% V1=zeros(pca_numwords);
% D1=zeros(1,pca_numwords);
% for col=1:pca_numwords
%         V1(:,col)=coeff(:,pca_numwords+1-col);
%         D1(col) =latent(pca_numwords+1-col);
% end
% coeff=V1;
% latent=D1';
%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Creates coeff
pca_numwords=10000;
coeff_raw_s=zeros(pca_numwords);
for row=1:pca_numwords
    for col=1:pca_numwords
        coeff_raw_s(row,col)=coeff_raw(row,col)/sqrt( coeff_raw(row,row) * coeff_raw(col,col));
    end
end

[coeff_s , latent_s]= eig(coeff_raw_s(1:pca_numwords,1:pca_numwords)'*coeff_raw_s(1:pca_numwords,1:pca_numwords));

latent_s=diag(latent_s);
V1=zeros(pca_numwords);
D1=zeros(1,pca_numwords);
for col=1:pca_numwords
        V1(:,col)=coeff_s(:,pca_numwords+1-col);
        D1(col) =latent_s(pca_numwords+1-col);
end
coeff_s=V1;
latent_s=D1';
%%%%%%%%%%%%%%%%%%%%%













%pca_numsamples=560;
%M=rand(pca_numsamples,pca_numwords);

%M1=M-sum(M)/pca_numsamples;
%M1=M1./ (vecnorm(M1)/sqrt(pca_numsamples));



%[matpca_coeff, matpca_score, matpca_latent]=pca(M1);
%[matpca_coeff ./ coeff]
%matpca_latent ./ latent




%M=rand(100,3);
%M=M-sum(M)/100
%M=M./ (vecnorm(M)/10);

