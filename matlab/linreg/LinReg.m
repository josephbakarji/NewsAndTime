%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%% Compute theta 

training_size=700;
inv_mat=zeros(10001);
mc=0;
y=zeros(1,10001);
for file=1:3
    if file==1
        fileID = fopen('./Data/1/AWarr_train.txt','r');
    elseif file==2
        fileID = fopen('./Data/2/AWarr_train.txt','r');
    else
        fileID = fopen('./Data/3/AWarr_train.txt','r');
    end
    for month=1:12*10
        mini_batch=zeros(training_size,10000);
        for row = 1 : training_size
            M=fscanf(fileID,'%d',10000);
            su=sum(M);
            if su<10
                mini_batch(row,:)=M*0;
            else
                mini_batch(row,:)=M/su;
            end
            fscanf(fileID,'%d',1);        
        end
        fprintf('training data: month number %d scanned\n',mc);
        mod_mini_batch = [ones(training_size,1) mini_batch];
        inv_mat=inv_mat+mod_mini_batch'*mod_mini_batch;
        y=y+mc*sum(mod_mini_batch);
        mc=mc+1;
    end
end
theta=inv_mat^(-1)*y';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%% Predict
binrange=-240:12:240;
dev_size=200;
month_count=0;
clear bin_data
pred_graph=zeros(360,1);
for decade=1:3
    if decade==1
        fileID = fopen('./Data/1/AWarr_dev.txt','r');
    elseif decade==2
        fileID = fopen('./Data/2/AWarr_dev.txt','r');
    else
        fileID = fopen('./Data/3/AWarr_dev.txt','r');
    end
    for month=1:12*10
        mini_batch=zeros(dev_size,10000);
        for row = 1 : dev_size
            M=fscanf(fileID,'%d',10000);
            su=sum(M);
            if su<10
                mini_batch(row,:)=M*0;
            else
                mini_batch(row,:)=M/su;
            end
            fscanf(fileID,'%d',1);        
        end
        fprintf('dev data: month number %d scanned\n',month_count);
        mod_mini_batch = [ones(dev_size,1) mini_batch];
        predicted  = mod_mini_batch*theta;
        predicted=predicted(predicted~=theta(1));
        predicted=190+(predicted-180)/0.47;
        middle_predicted=180*ones(length(predicted),1);
        if month_count==0
            bin_data=histcounts       (predicted-month_count,binrange);
            bin_data_middle=histcounts(middle_predicted-month_count,binrange);
        else
            bin_data=bin_data+histcounts(predicted-month_count,binrange);
            bin_data_middle=bin_data_middle+histcounts(middle_predicted-month_count,binrange);
        end
        pred_graph(month_count+1)=mean(predicted);
        month_count=month_count+1;
    end
end

bar(-20:19,bin_data_middle,'FaceColor',[0.8 0.8 1]);
title('Linear Regression: difference between the predicted and actual date');
ylabel('Number of articels')
xlabel('Predicted publication year- actual year');

hold on
bar(-20:19,bin_data,0.5,'FaceColor',[0.8 0 0]);
legend('Always select the middle date','Linear Regression Model');
hold off


%save('./Linreg_bin_data_middle_40years_window.mat','bin_data_middle');
%save('./Linreg_bin_data_40years_window.mat','bin_data');
avg=0;
totn=0;
tsq=0;
for i=1:40
    totn=totn+bin_data(i);
    avg=avg+bin_data(i)*i;
    tsq=tsq+bin_data(i)*i*i;
end
avg=avg/totn;
tsq=tsq/totn;
totn
avg
sqrt(tsq-avg*avg)












% score_1    =[ones(84000,1) score(:,1:1000)];
% score_dev_1=[ones(24000,1) score_dev(:,1:1000)];
% %theta=(X' * X)^(-1) * X' * y_train;
% theta=score_1\y_train;
% histogram(y_dev'-60,-120:4:120);
% hold on
% histogram(randi([0 119],1,24000)-y_dev',-120:4:120);
% hold on
% histogram((score_dev_1 * theta)-y_dev,-120:4:120);
% hold off