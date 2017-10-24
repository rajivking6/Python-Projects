import lmoments3 as lm
import numpy as np
from scipy import stats
from sklearn import metrics
def onerowstats(x,n):
    return np.array([np.mean(x),np.median(x),stats.skew(x),stats.kurtosis(x),np.std(x),sumofmaxs_or_mins(x,10),sumofmaxs_or_mins(x,10,max_or_min="min"),RMS(x),interquartile_range(x),*lstats(x,n)])
def matrix_stats(X,n=4):
    '''
    Order of stats: standard dev, skewness, kurtosis, l-scale, l-skewness,lkurtosis
    ^that is if n=4, if not 4 the order will be the same but additonal L-moments will added to the end, 1 per each value of n that increases
    Input: Matrix of rows of data 
    Output: 'summary' of each in row vectors joined into a matrix,
    basically a matrix of stats summarizing the data matrix
    '''
    X = np.array(X)
    stats = []
    try:
        for x in X:
            stats.append(onerowstats(x,n))
    except TypeError:
        stats.append(onerowstats(X,n))
    return np.array(stats)
def lkurtosis(x):
    return lm.lmom_ratios(x)[3]
def lskewness(x):
    return lm.lmom_ratios(x)[2]
def lscale(x):
    return lm.lmom_ratios(x)[1]
def mean(x):
    return lm.lmom_ratios(x)[0]
def sumofmaxs_or_mins(x,n,max_or_min="max"):
    if max_or_min == "min":
        index = np.argpartition(x,-n)[:-n]
        return np.sum(x[index])
    elif max_or_min == "max":
        index = np.argpartition(x,n)[n:]
        return np.sum(x[index])
    else:
        raise ValueError("max_or_min must equal exactly either 'max' or 'min'")
def interquartile_range(x):
    '''
    Input: arraylike x

    Output: the interquartile range of x


    '''
    q75, q25 = np.percentile(x, [75 ,25])
    iqr = q75 - q25
    return iqr
def RMS(x):
    '''
    Input: arraylike x

    Output: the root mean square of x


    '''
    return np.sqrt(mean(x**2))
def lstats(x,n):
    '''
    n is the number of  the lratios you wish to include, starting at L2 to exclude mean
    the function return L2,L3,L4 if n=4
    '''
    lratios = lm.lmom_ratios(x,nmom=n)
    return lratios[1:n]
if __name__ =="__main__":
    #testing 
    import time
    from gmuwork.shortcuts import quick_pfp2_file_reader
    s1 = quick_pfp2_file_reader("C:/Users/Rajiv Sarvepalli/Projects/Data for GMU/AllData/dataSet2/State1")
    s2 = quick_pfp2_file_reader("C:/Users/Rajiv Sarvepalli/Projects/Data for GMU/AllData/dataSet2/State2")
    s3 = quick_pfp2_file_reader("C:/Users/Rajiv Sarvepalli/Projects/Data for GMU/AllData/dataSet2/State3")
    s4 = quick_pfp2_file_reader("C:/Users/Rajiv Sarvepalli/Projects/Data for GMU/AllData/dataSet2/State4")
    sT = quick_pfp2_file_reader("C:/Users/Rajiv Sarvepalli/Projects/Data for GMU/AllData/dataSet2/StateTamper")
    d = np.concatenate((s1,s2,s3,s4,sT),axis=0)
    start_time = time.time()
    y = matrix_stats(d)
    print(time.time()-start_time)