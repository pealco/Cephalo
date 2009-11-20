from pylab import *
from megprocess import *
from epoch_rejection import *
import tables

def realproba(data):
    bins = 1000
    SIZE = size(data)
    sortbox = zeros(bins)
    minimum = amin(data)
    maximum = amax(data)
    data = floor((data - minimum )/(maximum - minimum)*(bins-1))
    data = data.flatten()
    data = array(data, dtype="int")
    
    for index in range(SIZE):
        #print int(data[index])
        sortbox[int(data[index])] += 1
        
    probaMap = sortbox[data] / SIZE
    sortbox  = sortbox / SIZE
    
    return probaMap, sortbox
    
    
    
h5_filename = "data/R0874.h5"
megdata = tables.openFile(h5_filename, mode = "r+")

left_hemisphere  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 58, 64, 67, 71, 73, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 87, 88, 90, 91, 105, 106, 107, 108, 109, 110, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 142, 150, 151]

channels = list(set(left_hemisphere) & set([25, 43, 44, 59, 60, 61, 62, 63, 80, 82, 85, 88, 90, 119, 129, 137, 138, 143, 144, 156]))

cond0 = megdata.root.epochs[0, ...]

samples, channels, epochs = shape(cond0)

JP = zeros((channels, epochs))
for channel in range(channels):
    dataproba = realproba(cond0[:, channel, :])[0]
    for epoch in range(epochs):
        tmp = dataproba[epoch * samples:(epoch+1) * samples]
        JP[channel, epoch] = -sum(log(tmp))

JP = (JP - mean(JP))/std(JP, ddof=1)
print mean(JP, axis=0) > 2

#accepted_epochs = [reject_epochs(epochs[c, :, :, :], method="diff") for c in range(8)]
#rejected_epochs = [list(set(range(100)) - set(epoch_set)) for epoch_set in accepted_epochs]

#for c in range(8):
#    for e in range(100):
#        figure()
#        if e in accepted_epochs[c]:
#            title("Accepted")
#        else:
#            title("Rejected")
#        
#        for chan in range(27):
#            plot(epochs[c,:,chan,e])
#        ylim((-1000, 1000))
#        outname = "c%de%d.png" %(c, e)
#        savefig(outname, format='png' )
#        close()
            


#for es in accepted_epochs:
#    figure()
#    plot(mean(rms(epochs[c,:,-10:,es], 2), 0))
#            
#for es in rejected_epochs:
#    figure()
#    plot(mean(rms(epochs[c,:,-10:,es], 2), 0))
#        #plot(mean(rms(epochs[c,:,:,es], 1)))
#
#show()