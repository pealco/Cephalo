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

def epoch(data, triggers, channels, config, name="epochs"):
    """Pulls out the epochs from the long data file."""
    
    conditions = config.num_of_conditions
    expected_epochs = config.expected_epochs
    stimulus_pre = config.epoch_pre
    stimulus_post = config.epoch_post
    
    epoch_length  = stimulus_pre + 1 + stimulus_post # Add 1 for 0 point.
    
    epochs = zeros((conditions, epoch_length, len(channels), expected_epochs))
    
    for (channel_index, channel) in enumerate(channels):
        print "Epoching channel %s ..." % channel
        the_chan = data[channel][:]
        for condition in range(conditions): 
            epoch_indices = range(len(triggers[condition]))
            random.shuffle(epoch_indices)
            epoch_indices = epoch_indices[:expected_epochs]
            
            for i, t in enumerate(epoch_indices):
                epoch_start = triggers[condition][t] - stimulus_pre
                epoch_end   = triggers[condition][t] + stimulus_post
                the_epoch = the_chan[range(epoch_start, epoch_end + 1)]
                epochs[condition, :, channel_index, i] = the_epoch
    
    
    
    ## This should work in the next version of pytables. Uses fancy indexing.   
    #for condition in conditions: 
    #    print "Epoching condition %s ..." % condition
    #    for t in range(max_epochs):
    #        epoch_start = triggers[condition][t] - stimulus_pre
    #        epoch_end   = triggers[condition][t] + stimulus_post
    #        the_epoch = data[channels][range(epoch_start, epoch_end + 1)]
    #        epochs[condition, :, :, t] = the_epoch
            
            
    return epochs

def save_epochs(megdata, epochs, epochs_filtered):
    """ This needs cleaning up to avoid repitition."""
    
    print "Saving epochs ..."
    print shape(epochs)
    
    #megdata.root.epochs.remove()
    #megdata.root.epochs_filtered.remove()
    
    if "/epochs" not in megdata:
        megdata.createCArray(
            where=megdata.root, 
            name="epochs", 
            atom=tables.Float32Atom(), 
            shape=shape(epochs),
            filters=tables.Filters(1))
        
    if "/epochs_filtered" not in megdata:
        megdata.createCArray(
            where=megdata.root,
            name="epochs_filtered",
            atom=tables.Float32Atom(),
            shape=shape(epochs_filtered),
            filters=tables.Filters(1))
    
    megdata.root.epochs[:] = epochs
    megdata.root.epochs_filtered[:] = epochs_filtered
    
    print "Done saving ..."

def baseline(epochs, epochs_pre):
    print "Baselining ..."
    for condition in arange(shape(epochs)[0]):
        for channel in arange(shape(epochs)[2]):
            epochs[condition, :, channel, :] = epochs[condition, :, channel, :] - mean(epochs[condition, 0:epochs_pre, channel, :], 0)
    return epochs
                
def rms(data, axis=0): 
    return sqrt(mean(data ** 2, axis))

def plot_rms_mean_conditions(mean_epochs):
    for condition in range(8):
        figure()
        plot(rms(mean_epochs, 2)[:, condition])

def difference_wave(standard, deviant): 
    return deviant - standard