This would compute preform the Naive Bayes analysis.

read_a_year : loads different years of data from the BOW matrix. To avoid memory problems, it loads each year at each calling.
WARNING: the input is now text file, the format is different form the sparse matrix input of python files, and takes a lot of 
memory, so it is not uploaded to the GitHub.

load_bayes : Not the best name for this script. This basically computes the yearly average of each feature word. This is the input for the predict_dev script.

predict_dev : makes predictions on the dev set (and test set when modified) and computes the probability of each article being assigned to different years. The output is in the input for the plotter script (in a different folder)
 