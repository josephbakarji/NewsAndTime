This would compute preform the PCA and GDA analysis.

read_a_year : loads different years of data from the BOW matrix. To avoid memory problems, it loads each year at each calling.
WARNING: the input is now text file, the format is different form the sparse matrix input of python files, and takes a lot of 
memory, so it is not uploaded to the GitHub.

load_bayes : Not the best name for this script. This basically computes the yearly average and standard devation of PCA components. This is the input for the predict_dev script.

Online_PCA : performs an online PCA, loads data in mini-batches and performs PCA.

predict_dev : makes predictions on the dev set (and test set when modified) and computes the probability of each article being assigned to different years, using GDA. The output is in the input for the plotter script (in a different folder)
 