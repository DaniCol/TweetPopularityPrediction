import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
from tqdm.notebook import tqdm
import scipy.optimize as optim

def plot_estimates(est_LLs, est_params, cascade):
    T = est_LLs[:,0]

    # First we need to compute loglikelihoods for the true parameters
    LLs = np.empty_like(T)
    n_samples = np.empty_like(T)
    tis = cascade[:,0]

    for i,t in enumerate(tqdm(T)):
        partial_cascade = cascade[tis < t]
        LLs[i] = loglikelihood((p, beta), partial_cascade, t) 
        n_samples[i] = len(partial_cascade)


    # Then we can draw the subplots
    _, axis = plt.subplots(3)
    
    axis[0].plot(T/60, est_LLs[:,1] / n_samples, label='$log\mathcal{L}_{est}/sample$')
    axis[0].plot(T/60, LLs / n_samples, label='$log\mathcal{L}_{true}/sample$')
    axis[0].legend() 

    axis[1].plot(T/60, est_params[:,1], label='$p_{est}$')
    axis[1].plot(T/60, p * np.ones_like(T), label='$p_{true}$')
    axis[1].legend() 

    axis[2].plot(T/60, est_params[:,2], label='$beta_{est}$')
    axis[2].plot(T/60, beta * np.ones_like(T), label='$beta_{true}$')
    axis[2].set_ylim((0,0.002))
    axis[2].legend() 