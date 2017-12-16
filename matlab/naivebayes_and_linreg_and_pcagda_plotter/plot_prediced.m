%plots predicted_logbayes
%% 
%Select Plot
%plotname='naive_bayes';
%plotname='GDA_PCA';
%plotname="Linreg";
plotname='Combination';
%% Read the histogram
binrange=-30:31;
bin_data=histcounts([],binrange);
bin_data_middle=histcounts([],binrange);
bin_data_randomguess=histcounts([],binrange);
for year=1:30
    for art=200:1200
        bayes_probs=reshape(predicted_logbayes(year,art,:),[1,30])+QAdd;
        bayes_probs=bayes_probs/100000;
        
        pca_probs=reshape(predicted_PCA(year,art,:),[1,30]);
        pca_probs=pca_probs/10000;
        linreg_probs=normpdf(1:30,predicted_linreg(year,art),5.87);
        
        if(plotname=="naive_bayes")
            probs=bayes_probs;
        end
        if(plotname=="GDA_PCA")
             probs=pca_probs;
        end
        if(plotname=="Linreg")
           probs=log(linreg_probs);
        end
        if(plotname=="Combination")
            probs=1*bayes_probs+0.009*log(linreg_probs);
        end
        
        [~,pred]=max(probs);
        bin_data=bin_data+histcounts(pred-year,binrange);
        bin_data_middle=bin_data_middle+histcounts(15.5-year,binrange);
        bin_data_randomguess=bin_data_randomguess+histcounts(randi([1,30])-year,binrange);
    end
end
%% Compute std
avg=0;
totn=0;
tsq=0;
for i=1:61
    totn=totn+bin_data(i);
    avg=avg+bin_data(i)*i;
    tsq=tsq+bin_data(i)*i*i;
end
avg=avg/totn;
tsq=tsq/totn;
fprintf('\n%d\n%d\n%d\n%f %f\n',totn,avg,sqrt(tsq-avg*avg),(bin_data(31))/totn,(bin_data(30)+bin_data(31)+bin_data(32))/totn,(bin_data(30)+bin_data(31)+bin_data(32)+bin_data(29)+bin_data(33))/totn);
%fprintf('std: %d',sqrt(tsq-avg*avg));
%% Plot the histogram
f = figure();
bar(-30:30,100*bin_data_randomguess/totn,'FaceColor',[0.8 0.8 1]);
if(plotname=="naive_bayes")
    title('Naive Bayes: Difference between the predicted and actual dates');
end
if(plotname=="GDA_PCA")
    title('PCA + GDA: Difference between the predicted and actual dates');
end
if(plotname=="Linreg")
    title('Linear regression: Difference between the predicted and actual dates');
end
if(plotname=="Combination")
    title('Combination of all models: Difference between the predicted and actual dates');
end
        
        
title('Naive Bayes: Difference between the predicted and actual dates');

ylabel('Percentage of articels')
xlabel('Predicted publication year - actual publication year');
%hold on
%bar(-30:30,bin_data_randomguess,'FaceColor',[1 0.8 0.8]);

hold on
bar(-30:30,100*bin_data/totn,0.5,'FaceColor',[0.8 0 0]);

if(plotname=="naive_bayes")
legend('Random guess','Naive Bayes');
end
if(plotname=="GDA_PCA")
    legend('Random guess','GDA_PCA');
end
if(plotname=="Linreg")
    legend('Random guess','Linear regression');
end
if(plotname=="Combination")
    legend('Random guess','Our model');
end

hold off
saveas(f, './plot.pdf');


