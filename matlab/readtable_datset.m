clear all
close all
clc

tabledir = '../tabledir/';
%A = tdfread([tabledir, 'MonthWord_198701_200712_700.txt'], '\t');
A = readtable([tabledir, 'MonthWord_198701_200712_700.txt'],'delimiter','\t');
year = A.YEAR;
months = A.MONTH;
words = A.Properties.VariableNames(3:end);

X = (table2array(A));
X(:,1:2)=[];

