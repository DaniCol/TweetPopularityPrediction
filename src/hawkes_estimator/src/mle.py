import numpy as np


def loglikelihood(params, history, t):
    """
    Returns the loglikelihood of a Hawkes process with exponential kernel
    computed with a linear time complexity
        
    params   -- parameter tuple (p,beta) of the Hawkes process
    history  -- (n,2) numpy array containing marked time points (t_i,m_i)  
    t        -- current time (i.e end of observation window)
    """
    
    p,beta = params    
    
    if p <= 0 or p >= 1 or beta <= 0.: return -np.inf

    n = len(history)
    tis = history[:,0]
    mis = history[:,1]
    
    LL = (n-1) * np.log(p * beta)
    logA = -np.inf
    prev_ti, prev_mi = history[0]
    
    i = 0
    for ti,mi in history[1:]:
        if(prev_mi + np.exp(logA) <= 0):
            print("Bad value", prev_mi + np.exp(logA))
        
        logA = np.log(prev_mi + np.exp(logA)) - beta * (ti - prev_ti)
        LL += logA
        prev_ti,prev_mi = ti,mi
        i += 1
        
    logA = np.log(prev_mi + np.exp(logA)) - beta * (t - prev_ti)
    LL -= p * (np.sum(mis) - np.exp(logA))

    return LL