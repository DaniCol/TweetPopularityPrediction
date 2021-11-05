import os
import numpy as np
from scipy import stats
import random 

def neg_power_law(alpha, mu, size=1):
    """
    Returns a 1D-array of samples drawn from a negative power law distribution
    
    alpha -- power parameter of the power-law mark distribution
    mu    -- min value parameter of the power-law mark distribution
    size  -- number of samples
    """
    
    u = np.random.uniform(size=size)
    X = mu * np.exp(np.log(u) / (1. - alpha))
    if size==1:
        return X[0]
    else:
        return X

def simulate_marked_exp_hawkes_process(params, m0, alpha, mu, max_size=10000):
    """
    Returns a 2D-array whose rows contain marked time points simulated from an exponential Hawkes process
    
    params   -- parameter tuple (p,beta) of the generating process
    m0       -- magnitude of the initial tweet at t = 0.
    alpha    -- power parameter of the power-law mark distribution
    mu       -- min value parameter of the power-law mark distribution
    max_size -- maximal authorized size of the cascade
    """
    
    p, beta = params    
    
    # Every row contains a marked time point (ti,mi).
    # Create an unitialized array for optimization purpose (only memory allocation)
    T = np.empty((max_size,2),dtype=float)
    
    intensity = beta * p * m0
    t, m = 0., m0
    
    # Main loop
    for i in range(max_size):
        # Save the current point before generating the next one.
        T[i] = (t,m)
        
        # Sample inter-event time v from a homogeneous Poisson process
        u = np.random.uniform()
        v = -np.log(u)
        
        # Apply the inversion equation
        w = 1. - beta / intensity * v
        # Tests if process stops generating points.
        if w <= 0.:
            T = T[:i,:]
            break
            
        # Otherwise computes the time jump dt and new time point t
        dt = - np.log(w) / beta
        t += dt
        
        # And update intensity accordingly
        m = neg_power_law(alpha, mu)
        lambda_plus = p * m
        intensity = intensity * np.exp(-beta * dt) + beta * lambda_plus        
    return T


def data_to_kafka_message(cascade):
    """
    Return a tuple (key, value) to be send through a kafka topic

    cascade   -- 2D-array whose rows contain marked time points

    """
    key = "1" 
    Value = { 'type' : 'serie', 'cid': 'tw23981', 'msg' : 'blah blah', 'T_obs': cascade[-1][0], 'tweets': cascade }
    return key,Value

def create_fake_data():
    """
    Return simulated data formated as a tuple (key,value) ready to be sent to a kafka topic
    """

    # Init parameters
    p, beta = 0.025, 1/3600.
    alpha, mu = 2.4, 10
    m0 = 1000
    n_star = p * mu * (alpha - 1) / (alpha - 2)
    print(f"n_star = {n_star:.2f}")

    # Create simulated data and convert to python list 
    cascade = list(simulate_marked_exp_hawkes_process((p,beta), m0, alpha, mu, max_size=10000).tolist())

    return data_to_kafka_message(cascade)



