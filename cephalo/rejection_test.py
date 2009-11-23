from pylab import *
from lib.megprocess import *
from lib.epoch_rejection import *
import tables

h5_filename = "../data/R1292.h5"
megdata = tables.openFile(h5_filename, mode = "r+")

data = megdata.root.raw_data_epochs[:]

for c in range(8):
    print c
    #print find_maxdiff(data[c, ...])
    #print find_maxdiff2(data[c, ...])
    #reject_by_std_method(data[c, ...])
    reject_by_diff_method(data[c, ...])

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