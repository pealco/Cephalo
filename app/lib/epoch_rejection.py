from numpy import *
from numpy import log2
from utility import *
from pylab import *

def find_maxdiff(epochs):
    maxdiff = zeros(shape(epochs)[2])
    for epoch in arange(shape(epochs)[2]):
        signal = rms(epochs[:, :, epoch], 1)
        for t in arange(50, shape(signal)[0] - 50):
            ampa = mean(signal[t-50:t])
            ampb = mean(signal[t:t+50])
            diff = abs(ampb - ampa)
            if diff > maxdiff[epoch]: 
                maxdiff[epoch] = diff
           
    return maxdiff

def reject_epochs(data, method="std"):
    """
    Takes a set of epochs from one condition for all channels.
    samples x channels x epochs
    
    Returns a list of good epochs
    """
    
    if method == "std":
        print "Rejecting epochs using standard deviation method ..."
        return reject_by_std_method(data)
    elif method == "diff":
        print "Rejecting epochs using difference method ..."
        return reject_by_diff_method(data)
    elif method == "entropy":
        print "Rejecting epochs using entropy method ..."
        return reject_by_entropy(data)
    else:
        print 'Rejection method "%s" not available.' % method
        return data

def reject_by_std_method(data):
    samples, channels, epochs = shape(data)
    
    rejected_epochs = []
    accepted_epochs = []
    
    for epoch in xrange(epochs):
        signal = rms(data[:, :, epoch], 1) # signal: samples
        deviations = zeros((samples - 200))
        mean_signal = mean(signal)
        std_signal  = std(signal, ddof=1)
        for t in arange(shape(deviations)[0]):
            deviations[t] = std(signal[t:t+200], ddof=1)
        
        deviations = scale(deviations)
        if max(deviations) >= 3:
            rejected_epochs += [epoch]
        else:
            accepted_epochs += [epoch]
            
    print  rejected_epochs
    return accepted_epochs
    
    
def reject_by_diff_method(data):
    threshold = 1.25
    samples, channels, epochs = shape(data)
    
    maxdiffs = find_maxdiff(data)
    #maxdiffs_mean = mean(maxdiffs)
    #maxdiffs_std  = std(maxdiffs)
    
    maxdiffs = scale(maxdiffs)
    
    rejected_epochs = where(maxdiffs >= threshold)[0]
    accepted_epochs = where(maxdiffs < threshold)[0]
    
    #rejected_epochs = arange(len(maxdiffs))[maxdiffs > maxdiffs_mean + 2*maxdiffs_std]
    #accepted_epochs = arange(len(maxdiffs))[maxdiffs <= maxdiffs_mean + 2*maxdiffs_std]
    
    print rejected_epochs
    return accepted_epochs

def entropy(signal, bins=64):
    '''Compute entropy.'''
    counts = histogram(signal, bins=bins)[0]
    ps = counts/float(sum(counts))  # coerce to float and normalize
    ps = ps[nonzero(ps)]            # toss out zeros
    H = -sum(ps * log2(ps))         # compute entropy
    
    return H
    
def reject_by_entropy(data):
    samples, channels, epochs = shape(data)
    entropies = array([entropy(data[:, :-10, epoch]) for epoch in xrange(epochs)])
    
    entropies = scale(entropies)
    rejected_epochs = [epoch for H, epoch in zip(entropies, range(epochs)) if H > 1.5]
    accepted_epochs = list(set(range(epochs)) - set(rejected_epochs))
    
    print rejected_epochs
    return accepted_epochs
    
def reject_by_prob(data):
    counts = [histogram(epochs[:,:,chan,:], bins=4165, normed=True)[0] for chan in xrange(157)]
    J = []

        
        
        