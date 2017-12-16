This would compute preform the Linear regression.

LinReg : Perform an online linear regression. The data set is so large that it cannot be loaded at once, so we split it in mini-batches and load them one by one.
WARNING: the input is now text file, the format is different form the sparse matrix input of python files, and takes a lot of 
memory, so it is not uploaded to the GitHub.

predict_dev : makes predictions on the dev set (and test set when modified) and computes the probability of each article being assigned to different years. The output is in the input for the plotter script (in a different folder)
 