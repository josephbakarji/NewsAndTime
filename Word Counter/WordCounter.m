clear all
close all
clc




months=dir('../fullarticles/');
mkdir('../fullarticlestext/');

%Put the matlab file in a folder which is contained in the working
%directory similar to the GitHub setup
%Start and end dates go here
start_year=2007;
start_month=01;

end_year=2009;
end_month=05;

numfolders=size(months);
numfolders=numfolders(1);
for i=1:numfolders
    foldername=months(i).name;
    if(strlength(foldername)>4)
        year=str2num(foldername(1:4));
        if(year>1000)
            month=str2num(foldername(6:strlength(foldername)));
            if( (year> start_year && year <end_year) || (start_year~= end_year && year==start_year && month>=start_month) || (start_year~= end_year && year==end_year && month<=end_month) || (start_year== end_year && year==start_year && month>=start_month && month<=end_month)) 
                fprintf('Im woroking on the articles of year %d month %d ... ',year,month);
                process(year,month); 
                fprintf('Okay done!\n',year,month);
            end
        end
    end
end
   


function process(year,month)
sourcefolderaddress =strcat('../fullarticles/',num2str(year),'_',num2str(month));
outputfolderaddress    =strcat('../fullarticlestext/',num2str(year),'_',num2str(month));
mkdir(outputfolderaddress);
files=dir(sourcefolderaddress);
numfiles=size(files);
numfiles=numfiles(1);
for i=1:numfiles
   if(strlength(files(i).name)>4)
       filename=files(i).name;
       sourcefileaddress=strcat(sourcefolderaddress,'/',filename);
       outputfileaddress=strcat(outputfolderaddress,'/',filename(1:strlength(filename)-4),'txt');
    %   outputfileaddress
       htmltotext(sourcefileaddress,outputfileaddress);
       
       
    
   end
end


end


%Year 2013 : <title> does not contain the title :'(
%for year=2007:2016 
%    original_file_name=strcat(int2str(year),'.html');
%    output_file_name  =strcat(int2str(year),'.txt');
%    htmltotext(original_file_name,output_file_name);   
%end

function htmltotext(original_file_name,output_put_name)
    file=fileread(original_file_name);
    title_starts=strfind(file,'<title>')+7;
    title_ends  =strfind(file,'</title>')-1;
    filesize=size(file);
    flag_title= title_not_confused(title_starts,title_ends);

    title=file(title_starts:title_ends);
    title=fix_string(title);
    
    story_paragraphs=strfind(file,'story-body-text story-content');
    
    %write to the file 
    wfile= fopen(output_put_name,'w');
    numpar=size(story_paragraphs);
    parcounter=0;
    fprintf(wfile,'ORIGINAL FILE NAME: <%s>\n\n',original_file_name);
    fprintf(wfile,'NUMBER OF PARAGRAPHS: <%d>\n\n',numpar(2));
    
    fprintf(wfile,'TITLE\n %s',title);
    for par_start= story_paragraphs
        parcounter=parcounter+1;
        if (parcounter== numpar(2))
            par_end= filesize(2);
        else 
            par_end= story_paragraphs(parcounter+1);
        end
        par_end= strfind(file(par_start:par_end),'</p>');
        
        par_end=par_end(1)+par_start-2;
        par_start=par_start+strfind(file(par_start:par_end),'>');
        paragraph=file(par_start:par_end);
        
        paragraph=fix_string(paragraph);
        paragraph=remove_hyperlinks(paragraph,original_file_name,numpar(2));
        
        fprintf(wfile,'\nPARAGRAPH <%d>\n %s',parcounter,paragraph);
        
        %file(par_start:par_end)
        %par_start
        %par_end
        
        %par_end= strfind(file(i:),'<\p>');
        
    end
    
    
    fclose(wfile);
end

function strout= remove_hyperlinks(str,original_file_name,nump)
begs= strfind(str,'<');
ends= strfind(str,'>');
sbegs=size(begs);
sends=size(ends);
if(sbegs(2)~=sends(2))
    fprintf('Im confused in the hyperlinks of the paragraph number %d in the file %s which is %s\n',nump, original_file_name,str);
end

if(sbegs(2)>0)
    strout='';
    begchar=1;
    
    for counter=1:sbegs(2)
        strout= strcat(strout,str(begchar:begs(counter)-1));
        
        begchar=ends(counter)+1;
    end
    strout= strcat(strout,str(begchar:strlength(str)));
else
    strout=str;
end

end

function str=fix_string(str)

%For now remove apostrophes s 
    %str=strrep(str,'’s','((apostrophe s))');
    %str=strrep(str,'’','((apostrophe at the end))');
    %str=strrep(str,'‘','((apostrophe at the beginning))');
str=strrep(str,'’s',' s');
str=strrep(str,'’',' ');
str=strrep(str,'‘',' ');

%Remove extra garbage
str=strrep(str,'“',' ');
str=strrep(str,'�',' ');
str=strrep(str,'&#8216;',' ');
str=strrep(str,'&#8217;',' ');
str=strrep(str,'�',' ');
str=strrep(str,'�',' ');


%Remove title stuff:
str=strrep(str,' - The New York Times','');
str=strrep(str,' - Slide Show - NYTimes.com','');
%Remove all NYTimes and The New York Times:
str=strrep(str,'The New York Times','');
str=strrep(str,'NYTimes','');
end

function flag_title=title_not_confused(title_starts,title_ends)
%Check if there is one title
    flag_title=1;
    a=size(title_starts);
    if( a(2) ~= 1)
        flag_title=0;
    end
    a=size(title_ends);
    if( a(2) ~= 1)
      flag_title=0;
    end
end
   
