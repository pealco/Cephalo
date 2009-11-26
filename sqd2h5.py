from numpy import *
import tables
from pysqd import SquidData
import sys
import os.path

def load(squid, h5f):
    for channel in xrange(squid.channel_count):
        print "Reading channel %d ..." % channel
        h5f.root.raw_data[channel, :] = squid.get_channel(channel)
    
if __name__ == "__main__":
    
    for sqd_filename in sys.argv[1:]:
        print sqd_filename
        
        squid = SquidData(sqd_filename)
        
        h5_filename = os.path.splitext(sqd_filename)[0] + ".h5"
        array_shape = (squid.channel_count, squid.actual_sample_count)
        
        h5f = tables.openFile(h5_filename, mode='w', title="MEG data")
        
        h5f.createCArray(
            where=h5f.root, 
            name='raw_data', 
            atom=tables.Int16Atom(), 
            shape=array_shape, 
            filters=tables.Filters(1))


        h5f.createCArray(
            where=h5f.root, 
            name='convfactor', 
            atom=tables.Float32Atom(), 
            shape=shape(squid.convfactor), 
            filters=tables.Filters(1))
        h5f.root.convfactor[:] = squid.convfactor
        
        load(squid, h5f)
        
        print "Output %s" % h5_filename
        h5f.close()
