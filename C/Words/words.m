clear all
close all
clc

global totalnumwords
global allwords
global numwords
global max_num_words
global max_num_articles
global cutoff_frequency
totalnumwords=0;
allwords=strings(100000,1);
numwords=zeros(100000,1,'uint32');

%allwords(1,1)='b';
%allwords(2,1)='c';
%allwords(3,1)='e';
%allwords(4,1)='f';
%allwords(5,1)='i';
%allwords(6,1)='s';
%totalnumwords=6;
%[flag,pos]=find_pos('x');
%flag
%pos

months=dir('../fullarticlestext/');

%Put the matlab file in a folder which is contained in the working
%directory similar to the GitHub setup
%Start and end dates go here
start_year=2008;
start_month=01;

end_year=2009;
end_month=12;
max_num_words=20000;
max_num_articles=1000;
cutoff_frequency=1/40000;


numfolders=size(months);
numfolders=numfolders(1);
for i=1:numfolders
    foldername=months(i).name;
    if(strlength(foldername)>4)
        year=str2num(foldername(1:4));
        if(year>1000)
            month=str2num(foldername(6:strlength(foldername)));
            if( (year> start_year && year <end_year) || (start_year~= end_year && year==start_year && month>=start_month) || (start_year~= end_year && year==end_year && month<=end_month) || (start_year== end_year && year==start_year && month>=start_month && month<=end_month)) 
             %   fprintf('Im working on the articles of year %d month %d ... ',year,month);
                process_folder(year,month); 
             %   fprintf('Okay done!\n',year,month);
            end
        end
    end
end
   


function process_folder(year,month)
global totalnumwords
global allwords
global numwords

totalnumwords=0;
allwords=strings(100000,1);
numwords=zeros(100000,1,'uint32');


global max_num_articles
sourcefolderaddress =strcat('../fullarticlestext/',num2str(year),'_',num2str(month));
files=dir(sourcefolderaddress);
numfiles=size(files);
numfiles=min(max_num_articles,numfiles(1));
for i=1:numfiles
   if(strlength(files(i).name)>4)
       fprintf('File %d of year %d and month %d -  num of distinct words %d\n',i,year,month,totalnumwords);
       filename=files(i).name;
       sourcefileaddress=strcat(sourcefolderaddress,'/',filename);
       process_file(sourcefileaddress);
       %   outputfileaddress
%       htmltotext(sourcefileaddress,outputfileaddress);
   end
end
save_data_for_month(sourcefolderaddress);
end

function save_data_for_month(sourcefolderaddress)
global totalnumwords
global allwords
global numwords
global cutoff_frequency

twords=0;
for i=1:totalnumwords
   twords=twords+numwords(i,1); 
end
cutoff=double(twords)*cutoff_frequency;
outputfileaddress=strcat(sourcefolderaddress,'/DATA.txt');
wfile= fopen(outputfileaddress,'w');   
cnumber=1;
for i=1:totalnumwords
   if(double(numwords(i,1))>=cutoff)
       fprintf(wfile,'%d\t%s\t\t%f\t%d\n',cnumber,allwords(i,1),double(numwords(i,1))/cutoff,numwords(i,1));
       cnumber=cnumber+1;
   end
end


fclose(wfile);

end



function process_file(filename)
file=fileread(filename);
spar=strfind(file,'PARAGRAPH');
numpar=size(spar);
numpar=numpar(2);
for i=2:numpar-1
   paragraph=file(spar(i)+11:spar(i+1)-2);
   process_paragraph(paragraph);
end

if(numpar>0)
    paragraph=file(spar(numpar)+11:strlength(file));
    process_paragraph(paragraph);
end
end

function process_paragraph(paragraph)
   word_start=1;
   flag=0;
   length=strlength(paragraph);
   ispletter=isletter(paragraph);
   for i=1:length
       if(flag==0)
            if(ispletter(i)==1)
               word_start=i; 
               flag=1;
            end
       else
            if(ispletter(i)==0)
               process_word(paragraph(word_start:i-1));
               flag=0;
            end
           
       end
       
   end
end

function process_word(word)
    word=lower(word);
    add_word(word);
end


function add_word(word)
    global totalnumwords
    global allwords
    global numwords
    global max_num_words
    
    if(totalnumwords==0)
        totalnumwords=1;
        allwords(1,1)=word;
        numwords(1,1)=1;
    else
        [flag,pos]=find_pos(word);
        if(flag==1)
            numwords(pos,1)=numwords(pos,1)+1;
        elseif(flag==0 && totalnumwords<  max_num_words)
            for i=totalnumwords:-1:pos
               numwords(i+1,1)=numwords(i,1); 
               allwords(i+1,1)=allwords(i,1);  
            end
            allwords(pos,1)=word;
            numwords(pos,1)=1;
            totalnumwords=totalnumwords+1;
        end
    end
end

function [flag,pos]=find_pos(word)
    global totalnumwords
    global allwords

    R=totalnumwords;
    L=1;
    m=0;
    while(1<R-L)
        m=floor((R+L)/2);
        if(allwords(m,1)<word)
            L=m;
        else
            R=m;    
        end
    end
    if(allwords(R,1)==word)
        pos=R;
        flag=1;
    elseif(allwords(L,1)==word)
        pos=L;
        flag=1;
    else
        pos=R;
        flag=0;
    end
    
    if(word<allwords(1,1))
       flag=0;
       pos=1;
    end
    if(word>allwords(totalnumwords,1))
       flag=0;
       pos=totalnumwords+1;
    end
    
end








