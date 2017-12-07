import numpy as np
import scipy.sparse 
import tensorflow as tf
from config import *
from helpfunc import ensure_dir

def loadY(dataset,part):
	filepath=tabledir+"ml_dir/"+str(dataset)+"/Ylabels_"+part+".txt"
	file = open(filepath)
	col=[]
	for line in file:
		col.append(int(line))

	row =(list(range(len(col))))
	value =(list(np.ones(len(col))))

	y=scipy.sparse.csr_matrix((value, (row, col)), shape=(len(col), np.amax(col)+1)).toarray()
	return y

def loadX(dataset,part):
	filepath=tabledir+"ml_dir/"+str(dataset)+"/AWarr_"+part+".npz"
	Xt=scipy.sparse.load_npz(filepath).astype(np.int16)
	Xt=Xt.todense()

	return Xt

def next_batch(num, data, labels):
    '''
    Return a total of `num` random samples and labels. 
    '''
    idx = np.arange(0 , len(data))
    np.random.shuffle(idx)
    idx = idx[:num]
    data_shuffle = [data[ i] for i in idx]
    labels_shuffle = [labels[ i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

def BuildLearnAlgo(n,c,a,mod_type):
# n: number of features, c: number of classes months

    if mod_type==0:
        x = tf.placeholder(tf.float32, [None, n])
        W = tf.Variable(tf.zeros([n, c]))
        b = tf.Variable(tf.zeros([c]))
        y = tf.nn.softmax(tf.matmul(x, W) + b)
        y_ = tf.placeholder(tf.float32, [None, c])
    else:

        print('Model have not be defined yet')


    Loss_Fn = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(a).minimize(Loss_Fn)

    return x, y , y_,train_step
	
def TrainLearnAlng(Xt,Yt,Xd,Yd,x, y , y_,train_step,epochs,batchsize,f):
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    dist = tf.reduce_mean(tf.cast(tf.abs(tf.argmax(y,1)-tf.argmax(y_,1)), tf.float32))
    num_batch=len(Xt)//batchsize
    np.random.seed(100)
    for i in range(epochs):
        p = np.random.permutation(Xt.shape[0])
      #  l = np.random.permutation(Xd.shape[0])
        for j in range(num_batch):
            batch_xs= Xt[p[j*batchsize:(j+1)*batchsize],:]
            batch_ys= Yt[p[j*batchsize:(j+1)*batchsize],:]
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
            #print(j)
        accu_tr,dist_tr=sess.run(accuracy, feed_dict={x: Xt[p[0:100000],:], y_: Yt[p[0:100000],:]}),sess.run(dist, feed_dict={x: Xt[p[0:100000],:], y_: Yt[p[0:100000],:]})     
        accu_dev,dist_dev=sess.run(accuracy, feed_dict={x: Xd, y_: Yd}),sess.run(dist, feed_dict={x: Xd, y_: Yd})
        print(i,accu_tr,dist_tr,accu_dev,dist_dev)
        f.write('\n'+str(i)+' '+str(accu_tr)+' '+str(dist_tr)+' '+str(accu_dev)+' '+str(dist_dev))
        #f.write('\n '+i' '+accu_tr' '+dist_tr' '+accu_dev' '+dist_dev)

def RunLearnAgg(dataset,a,batchsize,epochs,mod_type):

    run_dir=tabledir+'runs/'+str(dataset)+'/'
    ensure_dir(run_dir)
  
    f = open(run_dir+str(mod_type)+str(mod_type)+'_'+str(a)+'_'+str(epochs)+'.txt', 'w')
    f.write('Dataset: '+ str(dataset))
    f.write('\nModel Type: '+ str(mod_type))
    f.write('\nNumber of Epochs: '+ str(epochs))
      
    Xt=loadX(dataset,'train')
    Yt=loadY(dataset,'train')
    Xd=loadX(dataset,'test')
    Yd=loadY(dataset,'test')
    
    n=Xt.shape[1]
    c=Yt.shape[1]
    x, y , y_,train_step=BuildLearnAlgo(n,c,a,mod_type)

    TrainLearnAlng(Xt,Yt,Xd,Yd,x, y , y_,train_step,epochs,batchsize,f)
    f.close()


if __name__ == "__main__":
    
    dataset=6
    a=5.5
    batchsize=720
    epochs=100
    mod_type=0

    RunLearnAgg(dataset,a,batchsize,epochs,mod_type)

    
    
    

