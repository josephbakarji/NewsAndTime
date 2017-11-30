clear all
close all
clc

tabledir = './tabledir/';
A = tdfread([tabledir, 'MonthWord_test.txt'], '\t');

year = A.YEAR;
months = A.MONTH;
words = fieldnames( rmfield(A, {'YEAR', 'MONTH'}) );

X = zeros(length(year), length(words));

for i = 1:numel(words)
    X(:,i) = A.(words{i});
end


    
