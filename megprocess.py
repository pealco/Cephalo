from numpy import *
from scipy.io import mio
from pylab import *
from filter import *
import psyco
psyco.full()

def load_data(thefile):
    print "Loading data ..."
    matfile  = mio.loadmat(thefile)
    data     = matfile["data"]
    triggers = matfile["triggers"]
    
    return data, triggers

def epoch(data, triggers, channels, conditions):
    """Pulls out the epochs from the long data file."""
    
    stimulus_pre  = 100
    stimulus_post = 500
    epoch_length  = stimulus_pre + 1 + stimulus_post # + 1 for the actual stimulus, which occurs at 0
    
    epochs = zeros((len(conditions), epoch_length, len(channels), len(triggers))) # Preallocate memory.
    
    for (channel_index, channel) in enumerate(channels):
        print "Epoching channel %s ..." % channel
        for condition in conditions: 
            for t in range(shape(triggers[:, condition])[0]):
                epoch_start = triggers[t, condition] - stimulus_pre
                epoch_end   = triggers[t, condition] + stimulus_post
                the_epoch = data[channel][range(epoch_start, epoch_end + 1)]
                epochs[condition, :, channel_index, t] = the_epoch
    return epochs


def baseline(epochs):
    print "Baselining ..."
    for condition in arange(shape(epochs)[0]):
        for channel in arange(shape(epochs)[2]):
            epochs[condition, :, channel, :] = epochs[condition, :, channel, :] - mean(epochs[condition, 0:100, channel, :], 0)
    return epochs
                
def rms(data, axis=0): 
    return sqrt(mean(data ** 2, axis))

def find_maxdiff(epochs):
    maxdiff = zeros(shape(epochs)[2])
    bigdiff = zeros(shape(epochs)[2])
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
    else:
        print "Rejecting epochs using difference method ..."
        return reject_by_diff_method(data)

def reject_by_std_method(data):
    samples, channels, epochs = shape(data)
    
    rejected_epochs = []
    accepted_epochs = []
    
    for epoch in xrange(epochs):
        signal = rms(data[:, :, epoch], 1) # signal: samples
        deviations = zeros((samples - 200))
        mean_signal = mean(signal)
        std_signal  = std(signal)
        for t in arange(shape(deviations)[0]):
            deviations[t] = std(signal[t:t+200])
        
        deviations = abs(deviations - std_signal)
        if max(deviations) >= 90:
            rejected_epochs += [epoch]
        
        if max(deviations) < 90:
            accepted_epochs += [epoch]
            
    print  rejected_epochs
    return accepted_epochs
    
    
def reject_by_diff_method(data):
    samples, channels, epochs = shape(data)
    
    maxdiffs = find_maxdiff(data)
    maxdiffs_mean = mean(maxdiffs)
    maxdiffs_std  = std(maxdiffs)
    
    rejected_epochs = arange(len(maxdiffs))[maxdiffs > maxdiffs_mean + 2*maxdiffs_std]
    accepted_epochs = arange(len(maxdiffs))[maxdiffs <= maxdiffs_mean + 2*maxdiffs_std]
    
    print rejected_epochs
    return accepted_epochs
    

def plot_rms_mean_conditions(mean_epochs):
    for condition in range(8):
        figure()
        plot(rms(mean_epochs, 2)[:, condition])

def difference_wave(standard, deviant): 
    return deviant - standard