clear all
close all
clc



file=fileread('01tape.html');
title_starts=strfind(file,'<title>')+7;
title_ends  =strfind(file,'</title>')-1;

flag_title= title_not_confused(title_starts,title_ends);

title=file(title_starts:title_ends);
title=fix_string(title);
title


function str=fix_string(str)
str=strrep(str,'’s','');
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
   
