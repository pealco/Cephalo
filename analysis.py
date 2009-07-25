from megprocess import *
import scipy.ndimage as ndimage
import numpy as numpy
import threading
import re
import csv
import pickle

def plot_mmf(standards,deviants,labels,sname):        
    diffWave = []
    for i in arange(8):
        diffWave.append(difference_wave(standards[i],deviants[i]))
    fig1 = figure()
    fig1.subplotpars.hspace = 0.4
    for i in arange(8):
        subplot(4,2,i+1)
        title(sname+" "+labels[i])
        plot(standards[i], label="standard")
        plot(deviants[i], label="deviant")
#       xlim(200, 400)
        xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
        ylim(0, 70)
        legend()
    
    fig2 = figure()
#    fig2.subplotpars.hspace = 0.4
    for i in [0,2,4,6]:
        subplot(2,2,(i/2)+1)
        title(sname+" "+labels[i]+", "+labels[i+1])
        plot(diffWave[i], label=labels[i])
        plot(diffWave[i+1], label=labels[i+1])
        axhline(0,color='r')
#        xlim(200, 400)
        xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
        ylim(-50, 50)
        legend()

def find_peak(fullarray, center=100, window=25, prestim = 100, edgesize = 3, name = 'm100'):
    """Find local maximum nearest to center within +/- window 
        (compensates for prestim interval;)
        (defaults: find m100 within 25ms of 100ms, prestim interval 100ms)
    """
    leftbound = center + prestim - window
    rightbound = center + prestim + window
    arr = fullarray[4][leftbound:rightbound]
    max_points = arr == ndimage.maximum_filter(arr, 3, mode='nearest')
    maxima = [indices[max_points] for indices in  numpy.indices(arr.shape)] 
    abs_max = abs(maxima[0]-window)
    latency = maxima[0][argmin(abs_max)]+(prestim-window)
    amplitude = fullarray[4][latency+prestim]
    leftedge = arange(center-window,center-window+edgesize)
    rightedge = arange(center+window-edgesize,center+window)
    edges = concatenate((leftedge,rightedge))
    if latency in edges:
        reject_peak = 'y'
        approve = figure(1)
        title(fullarray[0]+" "+fullarray[1]+" "+fullarray[2]+" "+fullarray[3]+" "+name)
        xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
        plot(fullarray[4])
        axhline(amplitude,color='r')
        axvline(latency+prestim,color='r')
        axvline(leftbound, color='g')
        axvline(rightbound, color='g')        
        bg = AsyncShow()
        bg.start()
        reject_peak = raw_input("Suspicious peak; reject? ([y],n)")
        close(1)
        bg.join()
    else:
        reject_peak = 'n'
    if reject_peak == 'y':
        amplitude = 0
        latency = 0
    return amplitude, latency

    
def meanwindow(data, start = 150, end = 251):
    return mean(data[start+100:end+100])
    
def process(matfile, channels_of_interest, conds, currsubset):

    data, triggers = load_data(matfile)
    front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23]
    
    currchans = [x for x in channels_of_interest if x in currsubset]
    loaded_channels = front_sensors + currchans
    
    epochs = epoch(data, triggers, loaded_channels, range(conds)) # Raw epochs.
    epochs = baseline(epochs.copy())
    
    for c in loaded_channels:
        data[c] = lowpass(data[c], 1000, 20)
        
    epochs_filt = epoch(data, triggers, loaded_channels, range(conds)) # Filtered epochs.
    epochs_filt = baseline(epochs_filt.copy())
    
    mean_epochs = zeros((2, shape(epochs)[1], len(currchans)))    
    for c in range(conds):
        accepted_epochs = reject_epochs(epochs[c, :, :, :], method="diff")
        mean_epochs[c, :, :] = mean(epochs_filt[c, :, len(front_sensors):, accepted_epochs], 0)
    
    rms_mean_epochs = rms(mean_epochs, 2)
    
    return rms_mean_epochs

class AsyncShow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        show()

def writeToR(rawdata,filename='outfile.csv'):
    rout = []
    for result in rawdata:
        m100amp, m100lat = find_peak(result)
        mmf = meanwindow(result[4],150,250)
        rout.append([result[0],result[1],result[2],result[3],m100amp, m100lat, mmf])

    fout = open(filename,'w')

    csvout = csv.writer(fout,delimiter=',')

    for r in rout:
        csvout.writerow(r)

    fout.close()

    
def unpickle_process():
    
    fhandle = open('results.pickled', 'r')
    results = pickle.load(fhandle)
    fhandle.close()
    writeToR(results)
    



def normal_process():

    left_hemisphere =[1 , 2,  3,  4,  5,  6,  7,  8,  9,  11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 58, 64, 67, 71, 73, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 87, 88, 90, 91,  105, 106, 107, 108, 109, 110, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 142, 150, 151]
    right_hemisphere=[10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 65, 66, 68, 69, 70, 72, 81, 86, 89, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 141, 143, 144, 145, 146, 147, 148, 149, 152, 153, 154, 155, 156]

    subsets = [left_hemisphere, right_hemisphere]
    subsetnames = ["left_hemisphere", "right_hemisphere"]

    subjs1a = [
            ["R1134 Diads-2 1a 11.14.08 Run3_denoised.mat",[25, 26, 48, 52, 58, 59, 60, 62, 63, 64, 67, 76, 77, 86, 88, 90, 96, 143, 144, 151]],
            ["R1127 Diads-2 1a.8-11-08.Run2_denoised.mat",[25, 38, 39, 43, 44, 59, 60, 63, 65, 77, 80, 87, 88, 90, 96, 99, 121, 129, 143, 144]],
            ["R1227 Diads-2 1A 1.29.09 Run3_denoised.mat",[26, 27, 43, 44, 48, 59, 60, 63, 76, 77, 82, 85, 88, 90, 97, 119, 132, 144, 145, 156]],
            ["R1122 Diads2.1a.8.13.08 Run2_denoised.mat",[38, 44, 59, 60, 61, 62, 63, 79, 80, 85, 88, 90, 97, 118, 119, 127, 137, 138, 144, 145]],
            ["R1200 Diads2 1a 12.10.08 Run3_denoised.mat",[21, 26, 28, 39, 43, 44, 47, 48, 56, 57, 59, 60, 65, 68, 76, 77, 80, 82, 88, 96]],
            ["R1317 Diads2 6.18.09 1a Run2 _denoised.mat",[25, 43, 44, 59, 60, 63, 65, 77, 80, 82, 85, 86, 87, 88, 90, 99, 129, 143, 144, 156]]
    ]
    subjs1b = [
            ["R1134 Diads-2 1b 11.14.08 Run2_denoised.mat",[25, 26, 48, 52, 58, 59, 60, 62, 63, 64, 67, 76, 77, 86, 88, 90, 96, 143, 144, 151]],
            ["R1127 Diads-2.1b.8-11-08.Run2_denoised.mat",[25, 38, 39, 43, 44, 59, 60, 63, 65, 77, 80, 87, 88, 90, 96, 99, 121, 129, 143, 144]],
            ["R1227 Diads-2 1B 1.29.09 Run2_denoised.mat",[26, 27, 43, 44, 48, 59, 60, 63, 76, 77, 82, 85, 88, 90, 97, 119, 132, 144, 145, 156]],
            ["R1122 Diads2.1b.8.13.08 Run3_denoised.mat",[38, 44, 59, 60, 61, 62, 63, 79, 80, 85, 88, 90, 97, 118, 119, 127, 137, 138, 144, 145]],
            ["R1200 Diads2 1b 12.10.08 Run2_denoised.mat",[21, 26, 28, 39, 43, 44, 47, 48, 56, 57, 59, 60, 65, 68, 76, 77, 80, 82, 88, 96]],
            ["R1317 Diads2 6.18.09 1b Run3 _denoised.mat",[25, 43, 44, 59, 60, 63, 65, 77, 80, 82, 85, 86, 87, 88, 90, 99, 129, 143, 144, 156]]
    ]    
    subjs2a = [
            ["R0836 Diads-2 2a 9.26.08 Run6_denoised.mat",[22, 23, 24, 39, 43, 44, 48, 60, 61, 68, 69, 76, 77, 82, 85, 88, 90, 96, 97, 144]],
            ["R354 Diads2.2a.8.11.08_denoised.mat",[25, 39, 44, 65, 66, 79, 80, 85, 88, 90, 96, 99, 116, 117, 121, 127, 137, 138, 143, 144]],
            ["R1201 Diads2 2a 12.11.08 Run3_denoised.mat",[26, 42, 43, 44, 59, 60, 61, 63, 77, 80, 82, 87, 88, 90, 96, 97, 119, 127, 144, 145]],
            ["R1108 Diads2.2a. 8.12.08 Run2_denoised.mat",[2, 3, 21, 22, 24, 39, 43, 44, 46, 47, 60, 61, 68, 69, 77, 87, 88, 96, 97, 119]],
            ["R1133 Diads-2 2a 11.14.08 Run4_denoised.mat",[24, 26, 38, 39, 43, 44, 56, 59, 60, 63, 68, 77, 82, 87, 88, 90, 96, 97, 119, 137]]
    ]    
    subjs2b = [
            ["R1133 Diads-2 2b 11.14.08 Run3_denoised.mat",[24, 26, 38, 39, 43, 44, 56, 59, 60, 63, 68, 77, 82, 87, 88, 90, 96, 97, 119, 137]],
            ["R1201 Diads2 2b 12.11.08 Run2_denoised.mat",[26, 42, 43, 44, 59, 60, 61, 63, 77, 80, 82, 87, 88, 90, 96, 97, 119, 127, 144, 145]],
            ["R0836 Diads-2 2b 9.26.08 Run7_denoised.mat",[22, 23, 24, 39, 43, 44, 48, 60, 61, 68, 69, 76, 77, 82, 85, 88, 90, 96, 97, 144]],
            ["R354 Diads2.2b.8.11.08_denoised.mat",[25, 39, 44, 65, 66, 79, 80, 85, 88, 90, 96, 99, 116, 117, 121, 127, 137, 138, 143, 144]],
            ["R1108 Diads2.2b. 8.12.08 Run3_denoised.mat",[2, 3, 21, 22, 24, 39, 43, 44, 46, 47, 60, 61, 68, 69, 77, 87, 88, 96, 97, 119]]
    ]    
    subjs3a = [
            ["R0874 Diads-2 3a 11.21.08 Run3_denoised.mat",[43, 59, 60, 63, 65, 68, 80, 82, 85, 87, 88, 90, 96, 97, 99, 119, 132, 137, 138, 144]],
#            ["R1186 Dyads2-3a 11.20.08 Run3_denoised.mat",[42, 43, 44, 59, 65, 69, 75, 76, 77, 82, 85, 88, 90, 94, 99, 116, 117, 121, 143, 144]],
            ["R1016 Diads2 3a 3.17.09 Run3_denoised.mat",[52, 59, 68, 92, 96, 97, 99, 116, 117, 119, 126, 127, 130, 131, 135, 136, 138, 140, 144, 147]],
#            ["R1072 Diads-2 3a 8.11.08 Run2_denoised.mat",[26, 43, 44, 47, 48, 53, 54, 59, 60, 61, 63, 77, 80, 82, 85, 88, 90, 96, 97, 119]],
            ["R1093 Diads2.3a.8.13.08.Run2_denoised.mat",[44, 68, 77, 79, 80, 85, 87, 88, 90, 94, 96, 99, 116, 117, 118, 121, 127, 131, 144, 152]],
            ["R1141 Diads-2 3a 10.06.08 Run 6_denoised.mat",[24, 39, 43, 44, 59, 60, 61, 63, 79, 80, 86, 88, 90, 96, 121, 127, 137, 138, 143, 144]]
    ]
    subjs3b = [
#            ["R1186 Dyads2-3b 11.20.08 Run2_denoised.mat",[42, 43, 44, 59, 65, 69, 75, 76, 77, 82, 85, 88, 90, 94, 99, 116, 117, 121, 143, 144]],
            ["R1141 Diads-2 3b 10.06.08 Run 7_denoised.mat",[24, 39, 43, 44, 59, 60, 61, 63, 79, 80, 86, 88, 90, 96, 121, 127, 137, 138, 143, 144]],
            ["R0874 Diads-2 3b 11.21.08 Run2_denoised.mat",[43, 59, 60, 63, 65, 68, 80, 82, 85, 87, 88, 90, 96, 97, 99, 119, 132, 137, 138, 144]],
            ["R1016 Diads2 3b 3.17.09 Run2_denoised.mat",[52, 59, 68, 92, 96, 97, 99, 116, 117, 119, 126, 127, 130, 131, 135, 136, 138, 140, 144, 147]],
#            ["R1072 Diads-2 3b 8.11.08 Run3_denoised.mat",[26, 43, 44, 47, 48, 53, 54, 59, 60, 61, 63, 77, 80, 82, 85, 88, 90, 96, 97, 119]],
            ["R1093 Diads2.3b.8.13.08.Run3_denoised.mat",[44, 68, 77, 79, 80, 85, 87, 88, 90, 94, 96, 99, 116, 117, 118, 121, 127, 131, 144, 152]]
    ]
    subjs4a = [
            ["R1328 Diads 4a 06.01.09 Run2_denoised.mat",[4, 21, 22, 26, 38, 39, 43, 44, 59, 60, 77, 87, 88, 90, 96, 97, 118, 119, 127, 145]],
            ["R1354 Diads 2 4a 7.1.09 Run 2_denoised.mat",[2, 22, 23, 24, 28, 36, 37, 39, 43, 44, 47, 48, 56, 57, 60, 61, 66, 68, 77, 80]],
            ["R1203 Diads 2 4a 6.30.09 Run 3_denoised.mat",[39, 43, 44, 60, 63, 68, 76, 77, 80, 85, 88, 90, 96, 97, 99, 100, 116, 119, 127, 144]],
            ["R1232 Diads-2 4a 2.6.09 Run3_denoised.mat",[42, 43, 44, 59, 60, 61, 62, 63, 68, 69, 76, 77, 82, 85, 87, 88, 90, 96, 97, 144]],
            ["R1147 Diads-2 4a 11.10.08 Run2_denoised.mat",[43, 44, 55, 56, 59, 60, 63, 68, 80, 85, 88, 90, 96, 97, 99, 117, 127, 137, 138]]
    ]
    subjs4b = [
            ["R1328 Diads 4b 06.01.09 Run3_denoised.mat",[4, 21, 22, 26, 38, 39, 43, 44, 59, 60, 77, 87, 88, 90, 96, 97, 118, 119, 127, 145]],
            ["R1354 Diads 2 4b 7.1.09 Run 3 _denoised.mat",[2, 22, 23, 24, 28, 36, 37, 39, 43, 44, 47, 48, 56, 57, 60, 61, 66, 68, 77, 80]],
            ["R1203 Diads 2 4b 6.30.09 Run 2_denoised.mat",[39, 43, 44, 60, 63, 68, 76, 77, 80, 85, 88, 90, 96, 97, 99, 100, 116, 119, 127, 144]],
            ["R1147 Diads-2 4b 11.10.08 Run3_denoised.mat",[43, 44, 55, 56, 59, 60, 63, 68, 80, 85, 88, 90, 96, 97, 99, 117, 127, 137, 138]],
            ["R1232 Diads-2 4b 2.6.09 Run2_denoised.mat",[42, 43, 44, 59, 60, 61, 62, 63, 68, 69, 76, 77, 82, 85, 87, 88, 90, 96, 97, 144]]
    ]    

    results = [] 
    
    numre = re.compile(r'R(\d\d\d\d?).*')

    labels=["oct1_sine","7th_sine","oct2_sine","2oct_sine","oct1_vowel","7th_vowel","oct2_vowel","2oct_vowel"]
    for sindex, subset in enumerate(subsets):
        a1 = [process(data, channels, 2,subset) for data, channels in subjs1a]
        b1 = [process(data, channels, 2,subset) for data, channels in subjs1b]    
        a2 = [process(data, channels, 2,subset) for data, channels in subjs2a]
        b2 = [process(data, channels, 2,subset) for data, channels in subjs2b]
        a3 = [process(data, channels, 2,subset) for data, channels in subjs3a]
        b3 = [process(data, channels, 2,subset) for data, channels in subjs3b]
        a4 = [process(data, channels, 2,subset) for data, channels in subjs4a]    
        b4 = [process(data, channels, 2,subset) for data, channels in subjs4b]    
        
        a1nums = [numre.sub('\\1',data) for data,channels in subjs1a]
        b1nums = [numre.sub('\\1',data) for data,channels in subjs1b]
        a2nums = [numre.sub('\\1',data) for data,channels in subjs2a]
        b2nums = [numre.sub('\\1',data) for data,channels in subjs2b]
        a3nums = [numre.sub('\\1',data) for data,channels in subjs3a]
        b3nums = [numre.sub('\\1',data) for data,channels in subjs3b]
        a4nums = [numre.sub('\\1',data) for data,channels in subjs4a]
        b4nums = [numre.sub('\\1',data) for data,channels in subjs4b]
        
        subjnums = [b1nums, a1nums, a2nums, b2nums, b3nums, a3nums, a4nums, b4nums]
        standards=[[x[0] for x in b1],[x[0] for x in a1],[x[0] for x in a2],[x[0] for x in b2],[x[0] for x in b3],[x[0] for x in a3],[x[0] for x in a4],[x[0] for x in b4]]
        deviants=[[x[1] for x in b1],[x[1] for x in a1],[x[1] for x in a2],[x[1] for x in b2],[x[1] for x in b3],[x[1] for x in a3],[x[1] for x in a4],[x[1] for x in b4]]

        for cindex, condition in enumerate(labels):
            for i, subjnum in enumerate(subjnums[cindex]): 
                currstd = standards[cindex][i]
                results.append([subjnum,condition,'std',subsetnames[sindex],currstd])
                currdev = deviants[cindex][i]
                results.append([subjnum,condition,'dev',subsetnames[sindex],currdev])
        
        avgstandards = [mean(x, axis=0) for x in standards]
        avgdeviants = [mean(x, axis=0) for x in deviants]
       
        plot_mmf(avgstandards,avgdeviants,labels,subsetnames[sindex])
                            
    p = open("results.pickled",'w')
    pickle.dump(results,p)
    p.close()
    writeToR(results)
    show()

#        avg1a = mean(a1, axis=0)
#        avg1b = mean(b1, axis=0)
#        avg2a = mean(a2, axis=0)
#        avg2b = mean(b2, axis=0)
#        avg3a = mean(a3, axis=0)
#        avg3b = mean(b3, axis=0)
#        avg4a = mean(a4, axis=0)
#        avg4b = mean(b4, axis=0)        
        
        
#        standards=[avg1b[0,:],avg1a[0,:],avg2a[0,:],avg2b[0,:],avg3b[0,:],avg3a[0,:],avg4a[0,:],avg4b[0,:]]    
#        deviants=[avg1b[1,:],avg1a[1,:],avg2a[1,:],avg2b[1,:],avg3b[1,:],avg3a[1,:],avg4a[1,:],avg4b[1,:]]
    
    
    
if __name__ == "__main__":

#    normal_process()
    unpickle_process()
