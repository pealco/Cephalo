from numpy import shape, mean, std, zeros, where, alen, abs, maximum, \
histogram, nan, ma, isnan
from numpy import log2
from utility import *
#from pylab import *

def find_maximum_differences(data):
    samples, channels, epochs = shape(data)
    window_size = 50
    maximum_difference = zeros(epochs)
    signal = rms(data, axis=1)
    for t in xrange(window_size, alen(signal) - window_size):
        window_mean_a = mean(signal[t-window_size:t], axis=0)
        window_mean_b = mean(signal[t:t+window_size], axis=0)
        window_mean_difference = abs(window_mean_b - window_mean_a)
        maximum_difference = maximum(maximum_difference, window_mean_difference)
           
    return maximum_difference

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
    
    data_mean = mean(data)
    data_std  = std(data, ddof=1)
    cutoff = data_mean + (2 * data_std)
    extreme_value_counts = []
    for epoch in xrange(epochs):
        signal = rms(data[..., epoch], 1) # signal: samples
        extreme_value_count = alen(signal[signal > cutoff])
        extreme_value_counts.append(extreme_value_count)
        
    extreme_value_count_mean = mean(extreme_value_counts)
    extreme_value_count_std = std(extreme_value_counts, ddof=1)
    count_cutoff = extreme_value_count_mean + (3 * extreme_value_count_std)
    
    rejected_epochs = where(extreme_value_counts >= count_cutoff)[0]
    accepted_epochs = where(extreme_value_counts < count_cutoff)[0]
            
    print rejected_epochs
    return accepted_epochs, rejected_epochs
    
    
def reject_by_diff_method(data):
    threshold = 2
    samples, channels, epochs = shape(data)
    
    maximum_differences = find_maximum_differences(data)
    
    maximum_differences = scale(maximum_differences)
    
    rejected_epochs = where(maximum_differences >= threshold)[0]
    accepted_epochs = where(maximum_differences < threshold)[0]
    
    print rejected_epochs
    return accepted_epochs, rejected_epochs

def entropy(signal, bins=64):
    '''Compute entropy.'''
    counts = histogram(signal, bins=bins)[0]
    ps = counts/float(sum(counts))  # coerce to float and normalize
    ps = ps[nonzero(ps)]            # toss out zeros
    H = -sum(ps * log2(ps))         # compute entropy
    
    return H
    
def reject_by_entropy(data):
    samples, channels, epochs = shape(data)
    entropies = array([entropy(data[..., epoch]) for epoch in xrange(epochs)])
    
    entropies = scale(entropies)
    rejected_epochs = where(entropies > 2.0)[0]
    accepted_epochs = where(entropies <= 2.0)[0]
    #rejected_epochs = [epoch for H, epoch in zip(entropies, range(epochs)) if H > 2.0]
    #accepted_epochs = list(set(range(epochs)) - set(rejected_epochs))
    
    print rejected_epochs
    return accepted_epochs, rejected_epochs
    
def reject_by_prob(data):
    counts = [histogram(epochs[:,:,chan,:], bins=4165, normed=True)[0] for chan in xrange(157)]
    J = []

        
        
        