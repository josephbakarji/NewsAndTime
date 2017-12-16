%load('../data/mean_value_for_exp.mat');
%load('../data/dev_data.mat');

%% 
eps=0.0000001;
mod_bayes_matrix=bayes_matrix+eps;
select_word=1:10000;
predicted_logbayes=zeros(30,1200,30);
tic;
%all_probs=zeros(30,200,30,10000);
for year = 1 : 30
   % fprintf('Year %d ...',year);
    year_features=reshape(dev_data(year,:,:),[1200,10000]);
    for art=200:1200
        predicted_logbayes(year,art,:)=...
            sum(...
            -(1./mod_bayes_matrix(:,select_word)).*year_features(art,select_word)...-log(mod_bayes_matrix(:,select_word))...
            ,2);
    end
    %fprintf('scanned!\n');
    ttoc=toc;
    %fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
end
%% 
%% 
% predicted_logbayes=zeros(30,1200,30);
% tic;
% word_pred_prob=zeros(10000,1);
% word_pred_prob_sum=zeros(10000,1);
% for year = 1 : 30
%     fprintf('Year %d ...',year);
%     for art=1:20
%         for w=1:10000
%             word_pred_prob(w)= word_pred_prob(w)+ exp(all_probs(year,art,year,w));
%             word_pred_prob_sum(w)=word_pred_prob_sum(w)+sum(exp(all_probs(year,art,:,w)));
%         end
%     end
%     fprintf('scanned!\n');
%     ttoc=toc;
%     fprintf('remaining time %f seconds\n',ttoc*(30-year)/year);
% end
%% 
%word_pred_prob=word_pred_prob./ word_pred_prob_sum;
%word_pred_prob=word_pred_prob-1/30;
%selected_words=find(word_pred_prob>0)

%(pred)





%% 








%plot_prediced










