"""Some utility functions specific to MEG data."""

from numpy import mean, nonzero, diff, arange, shape, array, amax, amin, size
from pylab import plot, figure, find
from utility import rms
#from pylab import *
#from peak_finding import *

def find_triggers(data, triggerLinesPotential=None, triggerHighThresh=None, triggerLowThresh=None):
    """Locates triggers in the trigger channels. Returns a list of arrays."""
    
    if not triggerLinesPotential:
        triggerLinesPotential = arange(160, 192)
        
    if not triggerHighThresh:
        triggerHighThresh = 5 # mV
    
    if not triggerLowThresh:
        triggerLowThresh = 0.2 # mV
        
    triggerHighThresh_mV = triggerHighThresh * 1000 # mV
    triggerLowThresh_mV  = triggerLowThresh  * 1000 # mV
    
    triggerData = f.root.raw_data[160:192, :].T * f.root.convfactor[160:192]
    
    # First find channels whose maximum is at least the "high" threshold and
    # whose minimum is at most the "low" threshold.
    
    triggerLinesTest = ((amax(triggerData, 0) > triggerHighThresh_mV) & (amin(triggerData, 0) < triggerLowThresh_mV))
    triggerDataProbable = triggerData[:,triggerLinesTest]
    triggerLinesProbable = triggerLinesPotential[triggerLinesTest]
    #del triggerData
    
    triggersNearHigh = mean(triggerDataProbable > triggerHighThresh_mV, 0)
    triggersNearLow = mean(triggerDataProbable < triggerLowThresh_mV, 0)
    
    triggerLinesHealthyHighRest =  (triggersNearHigh > 25 * triggersNearLow)
    triggerDataHighRestGood = triggerDataProbable[:,triggerLinesHealthyHighRest]
    triggerLinesHighRestGood = triggerLinesProbable[triggerLinesHealthyHighRest]
    triggerLinesHighRestGoodCount = size(triggerLinesHighRestGood)
    
    triggerLinesHealthyLowRest =  (triggersNearLow > 25 * triggersNearHigh)
    triggerDataLowRestGood = triggerDataProbable[:,triggerLinesHealthyLowRest]
    triggerLinesLowRestGood = triggerLinesProbable[triggerLinesHealthyLowRest]
    triggerLinesLowRestGoodCount = size(triggerLinesLowRestGood)
    
    if triggerLinesHighRestGoodCount > triggerLinesLowRestGoodCount:
        triggerDataGood = triggerDataHighRestGood
        triggerLinesGood = triggerLinesHighRestGood
        triggerLinesGoodCount = triggerLinesHighRestGoodCount
    else:
        triggerDataGood = triggerDataLowRestGood
        triggerLinesGood = triggerLinesLowRestGood
        triggerLinesGoodCount = triggerLinesLowRestGoodCount
        
    # del triggerDataProbable
    
    triggersList = []
    
    for iTrigger in range(triggerLinesGoodCount):
        if triggerLinesHighRestGoodCount > triggerLinesLowRestGoodCount:
            triggerSet = find(triggerDataGood[:, iTrigger] < triggerLowThresh_mV)
        else:
            triggerSet = find(triggerDataGood[:, iTrigger] > triggerHighThresh_mV)

        # the next line uses find and diff to discard samples of triggerSet
        # that immediately follow any other values that cross
        # the "set" threshold.
        
        triggerSamples = (triggerSet[hstack((0, find(diff(triggerSet) > 1)+1))])
        triggersList.append(triggerSamples)
    
    return triggerSamples
    

def baseline(epochs, epochs_pre):
    """Performs baselining. Averages the epoch before the stimulus and subtracts
    the mean from the whole epoch."""
    print "Baselining ..."
    for condition in arange(shape(epochs)[0]):
        for channel in arange(shape(epochs)[2]):
            baseline_mean = mean(epochs[condition, 0:epochs_pre, channel, :], 0)
            epochs[condition, :, channel, :] = \
                epochs[condition, :, channel, :] - baseline_mean
    return epochs
    

def plot_rms_mean_conditions(mean_epochs):
    """Plots the RMS of the mean for all conditions."""
    for condition in range(8):
        figure()
        plot(rms(mean_epochs, 2)[:, condition])

def difference_wave(standard, deviant):
    """Computes difference wave."""
    return deviant - standard