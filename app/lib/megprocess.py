from numpy import *
from pylab import *
from filters import *
import tables
from epoch_rejection import *
from peak_finding import *

def find_triggers(data, trigger_channels):
    """Locates triggers in the trigger channels. Returns a list of arrays."""
    
    threshold = (25-1) / float(5 * 2)
    triggers = [nonzero(diff(data[trigger_channel, :]) > threshold)[0] for trigger_channel in trigger_channels]
    for i in range(len(triggers)):
        triggers[i] = triggers[i][triggers[i] > 100]
        trigger_pairs = zip(triggers[i], triggers[i][1:])
        triggers[i] = [trigger_pair[0] for trigger_pair in trigger_pairs if diff(trigger_pair) > 100]
    
    return triggers

def baseline(epochs, epochs_pre):
    print "Baselining ..."
    for condition in arange(shape(epochs)[0]):
        for channel in arange(shape(epochs)[2]):
            epochs[condition, :, channel, :] = epochs[condition, :, channel, :] - mean(epochs[condition, 0:epochs_pre, channel, :], 0)
    return epochs
    

def plot_rms_mean_conditions(mean_epochs):
    for condition in range(8):
        figure()
        plot(rms(mean_epochs, 2)[:, condition])

def difference_wave(standard, deviant): 
    return deviant - standard