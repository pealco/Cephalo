from numpy import *
from scipy.io import mio
from pylab import *
#import psyco
#psyco.full()

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
                epoch_start = triggers[t,condition] - stimulus_pre;
                epoch_end   = triggers[t,condition] + stimulus_post;
                the_epoch = data[channel][range(epoch_start, epoch_end + 1)];
                epochs[condition, :, channel_index, t] = the_epoch;
    return epochs

def baseline(epochs):
    for condition in arange(shape(epochs)[0]):
        for channel in arange(shape(epochs)[2]):
            epochs[condition, :, channel, :] = epochs[condition, :, channel, :] - mean(epochs[condition, 0:100, channel, :], 0)
    return epochs
                
def rms(data, axis=0):
    return transpose(sqrt(sum((data ** 2), axis)/shape(data)[axis]))

def reject(epochs):
    maxdiff = zeros(shape(epochs)[3])
    bigdiff = zeros(shape(epochs)[3])
    for epoch in arange(shape(epochs)[3]):
        signal = rms(epochs[0, :, :, epoch], 1)
        for t in arange(50, shape(signal)[0] - 50):
            ampa = mean(signal[t-50:t])
            ampb = mean(signal[t:t+50])
            diff = abs(ampb - ampa)
            if diff > maxdiff[epoch]: 
                maxdiff[epoch] = diff
                bigdiff[epoch] = t
            
    return maxdiff, bigdiff

def load_data(thefile):
    x = mio.loadmat(thefile)
    data     = x["data"]
    triggers = x["triggers"]
    
    return data, triggers

x = mio.loadmat("R1158.mat")
data     = x["data"]
triggers = x["triggers"]
front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23]

epochs = epoch(data, triggers, front_sensors, range(8))
epochs = baseline(epochs.copy())
mean_epochs = mean(epochs, 3)

rejected_epochs = 

figure()
#plot(mean_epochs[1,:,:])
plot(rms(mean_epochs, 2)[:, 0])
print "plot 1"

figure()
bar(arange(0,200), reject(epochs)[0])
print "plot 2"

figure()
hist(reject(epochs)[1], 12)
print "plot 3"

show()