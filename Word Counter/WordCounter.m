clear all
close all
clc

%Year 2013 : <title> does not contain the title :'(
for year=2007:2016 
    original_file_name=strcat(int2str(year),'.html');
    output_file_name  =strcat(int2str(year),'.txt');
    htmltotext(original_file_name,output_file_name);
    %end write
    
    
end

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
        paragraph=strrep(paragraph,'ù',' ');
        
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
strout
end

function str=fix_string(str)

%For now remove apostrophes s 
    %str=strrep(str,'â€™s','((apostrophe s))');
    %str=strrep(str,'â€™','((apostrophe at the end))');
    %str=strrep(str,'â€˜','((apostrophe at the beginning))');
str=strrep(str,'â€™s',' s');
str=strrep(str,'â€™',' ');
str=strrep(str,'â€˜',' ');

%Remove extra garbage
str=strrep(str,'â€œ',' ');
str=strrep(str,'â€',' ');
str=strrep(str,'&#8216;',' ');
str=strrep(str,'&#8217;',' ');
str=strrep(str,'ù',' ');
str=strrep(str,'”',' ');


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
   
