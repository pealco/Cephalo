from numpy import *
from scipy.io import mio
from scipy.signal import butter, lfilter
from pylab import *
import psyco
psyco.full()

def load_data(thefile):
    print "Loading data ..."
    matfile = mio.loadmat(thefile)
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
        if max(deviations) >= 250:
            rejected_epochs += [epoch]
        
        if max(deviations) < 250:
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
    
    
def lfilter_zi(b,a):
    #compute the zi state from the filter parameters. see [Gust96].

    #Based on:
    # [Gust96] Fredrik Gustafsson, Determining the initial states in forward-backward 
    # filtering, IEEE Transactions on Signal Processing, pp. 988--992, April 1996, 
    # Volume 44, Issue 4

    n=max(len(a),len(b))

    zin = (  eye(n-1) - hstack( (-a[1:n,newaxis],
                                 vstack((eye(n-2), zeros(n-2))))))

    zid=  b[1:n] - a[1:n]*b[0]

    zi_matrix=linalg.inv(zin)*(matrix(zid).transpose())
    zi_return=[]

    #convert the result into a regular array (not a matrix)
    for i in range(len(zi_matrix)):
      zi_return.append(float(zi_matrix[i][0]))

    return array(zi_return)
    

def filtfilt(b,a,x):
    #For now only accepting 1d arrays
    ntaps=max(len(a),len(b))
    edge=ntaps*3

    if x.ndim != 1:
        raise ValueError, "Filiflit is only accepting 1 dimension arrays."

    #x must be bigger than edge
    if x.size < edge:
        raise ValueError, "Input vector needs to be bigger than 3 * max(len(a),len(b)."

    if len(a) < ntaps:
        a=r_[a,zeros(len(b)-len(a))]

    if len(b) < ntaps:
        b=r_[b,zeros(len(a)-len(b))]

    zi=lfilter_zi(b,a)

    #Grow the signal to have edges for stabilizing 
    #the filter with inverted replicas of the signal
    s=r_[2*x[0]-x[edge:1:-1],x,2*x[-1]-x[-1:-edge:-1]]
    #in the case of one go we only need one of the extrems 
    # both are needed for filtfilt

    (y,zf)=lfilter(b,a,s,-1,zi*s[0])

    (y,zf)=lfilter(b,a,flipud(y),-1,zi*y[-1])

    return flipud(y[edge-1:-edge+1])


def lowpass(data, Fs, Flp):
    """Lowpass Butterworth filter."""

    # Nyquist frequency
    Fn = Fs/2.0
    
    # Filter order.
    N = 6
    
    # Filter design.
    b, a = butter(N, max(Flp)/Fn)
    
    return filtfilt(b, a, data)
    
def process(matfile, channels_of_interest):

    data, triggers = load_data(matfile)
    
    front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23]
    loaded_channels = front_sensors + channels_of_interest
    
    epochs = epoch(data, triggers, loaded_channels, range(8))
    epochs = baseline(epochs.copy())
    
    #for c in range(8):
    #    figure()
    #    #plot(mean(rms(epochs[c,:,:,:], 1), 1))
    #    title(r"Mean epochs for channel 0")
    #    plot(mean(epochs[c, :, 0, :], 1))
    #
    mean_epochs = zeros((8, shape(epochs)[1], len(channels_of_interest)))    
    for c in range(8):
        accepted_epochs = reject_epochs(epochs[c, :, :, :], method="diff")
        mean_epochs[c, :, :] = mean(epochs[c, :, len(front_sensors):, accepted_epochs], 0)
    
    rms_mean_epochs = rms(mean_epochs, 2)
    
    standard_1 = rms_mean_epochs[6, :]  # ledif standard
    deviant_1  = rms_mean_epochs[5, :]  # ledif deviant
    standard_2 = rms_mean_epochs[4, :]  # ldif  standard
    deviant_2  = rms_mean_epochs[7, :]  # ldif  deviant
    standard_3 = rms_mean_epochs[2, :]  # delif standard
    deviant_3  = rms_mean_epochs[1, :]  # delif deviant
    standard_4 = rms_mean_epochs[0, :]  # dlif  standard
    deviant_4  = rms_mean_epochs[3, :]  # dlif  deviant
    
    difference_wave_1 = difference_wave(standard_1, deviant_1) # ledif
    difference_wave_2 = difference_wave(standard_2, deviant_2) # ldif 
    difference_wave_3 = difference_wave(standard_3, deviant_3) # delif
    difference_wave_4 = difference_wave(standard_4, deviant_4) # dlif
    
    figure()
    
    subplot(211)
    title("ledif")
    plot(standard_1, label="standard")
    plot(deviant_1, label="deviant")
    #xlim(300, 400)
    ylim(0, 70)
    legend()
    
    subplot(212)
    title("ldif")
    plot(standard_2, label="standard")
    plot(deviant_2, label="deviant")
    #xlim(300, 400)
    ylim(0, 70)
    legend()
    
    figure()
    
    subplot(211)
    title("delif")
    plot(standard_3, label="standard")
    plot(deviant_3, label="deviant")
    #xlim(300, 400)
    ylim(0, 70)
    legend()
    
    subplot(212)
    title("dlif")
    plot(standard_4, label="standard")
    plot(deviant_4, label="deviant")
    #xlim(300, 400)
    ylim(0, 70)
    legend()

    figure()
    
    subplot(211)
    title("LD - Sonority -1")
    plot(difference_wave_1, label="ledif dv-st") # ledif
    plot(difference_wave_2, label="ldif dv-st") # ldif 
    #xlim(300, 400)
    ylim(-50, 50)
    legend()
    
    subplot(212)
    title("DL - Sonority +3")
    plot(difference_wave_3, label="delif dv-st") # delif
    plot(difference_wave_4, label="dlif dv-st") # dlif
    #xlim(300, 400)
    ylim(-50, 50)
    legend()
    
    ld_wave = difference_wave_1 - difference_wave_2
    dl_wave = difference_wave_3 - difference_wave_4
    
    figure()
    
    subplot(211)
    plot(ld_wave, label="LD")
    plot(dl_wave, label="DL")
    #xlim(300, 400)
    legend()
    
    subplot(212)
    plot(ld_wave - dl_wave)
    #xlim(300, 400)
    
    figure()
    
    title("deviants")
    plot(difference_wave_2, label="ldif")
    plot(difference_wave_4, label="delif")
    #xlim(300, 400)
    #ylim(0, 70)
    legend()

    
    show()


if __name__ == "__main__":
    #process("R1277-sonority-Filtered.sqd.mat", [43, 44, 80, 82, 85, 77, 87, 88, 90, 129, 63, 99, 116, 117, 118, 69, 94, 121, 122, 143])
    process("R1133-sonority-Filtered.sqd.mat", [39, 43, 44, 80, 82, 87, 88, 90, 129, 137])
    
    
    #R0874 [25, 26, 43, 44, 59, 60, 63, 65, 80, 82, 85, 87, 88, 90, 137, 143, 144, 145, 156]