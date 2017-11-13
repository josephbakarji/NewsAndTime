clear all
close all
clc

%Year 2013 : <title> does not contain the title :'(
for year=2007:2016 
    file=fileread(strcat(int2str(year),'.html'));
    title_starts=strfind(file,'<title>')+7;
    title_ends  =strfind(file,'</title>')-1;

    flag_title= title_not_confused(title_starts,title_ends);

    title=file(title_starts:title_ends);
    title=fix_string(title);
    title
end

function str=fix_string(str)
str=strrep(str,'’s','((apostrophe s))');
str=strrep(str,'’','((apostrophe at the end))');
str=strrep(str,'‘','((apostrophe at the beginning))');

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
   
