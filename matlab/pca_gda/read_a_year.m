
if year_to_load==1 || year_to_load==11 || year_to_load==21
    if train_not_dev==true
        article_number=700;
        if year_to_load==1
            filename='../../Data/1/AWarr_train.txt';
            filenameY='../../Data/1/Ylabels_train.txt';
        end
        if year_to_load==11
            filename='../../Data/2/AWarr_train.txt';
            filenameY='../../Data/2/Ylabels_train.txt';
        end
        if year_to_load==21
            filename='../../Data/3/AWarr_train.txt';
            filenameY='../../Data/3/Ylabels_train.txt';
        end
    else
        article_number=200;
        if year_to_load==1
            filename='../../Data/1/AWarr_dev.txt';
            filenameY='../../Data/1/Ylabels_dev.txt';
        end
        if year_to_load==11
            filename='../../Data/2/AWarr_dev.txt';
            filenameY='../../Data/2/Ylabels_dev.txt';
        end
        if year_to_load==21
            filename='../../Data/3/AWarr_dev.txt';
            filenameY='../../Data/3/Ylabels_dev.txt';
        end
    end
    fileID = fopen(filename,'r'); 
    fileIDY= fopen(filenameY,'r'); 
    article_counter=1;
    y_dat=fscanf(fileIDY,'%d');
end
year_features=zeros(article_number*12,10000);
year_num_articles=0;
while(y_dat(article_counter)<=mod(year_to_load-1,10)*12+11 && ~feof(fileID))    
    M=fscanf(fileID,'%d',10000);
    su=sum(M);
    if su>=10
        year_num_articles=year_num_articles+1;
        year_features(year_num_articles,:)=M/su;        
    end
    fscanf(fileID,'%d',1);        
    
    %if(mod(year_num_articles,article_number)==0) 
    %    fprintf('training data: article number %d scanned\n',year_num_articles);
    %end
    
    article_counter=article_counter+1;
    if article_counter>12*10*article_number
        break;
    end
end
year_to_load=year_to_load+1;
if(year_to_load==31)
    year_to_load=1;
end
year_features=year_features(1:year_num_articles,:);
