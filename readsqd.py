from numpy import *
import tables
from pysqd import SquidData
import sys
import gc

def dump_garbage():
    """
    show us what's the garbage about
    """
        
    # force collection
    print "\nGARBAGE:"
    gc.collect()

    print "\nGARBAGE OBJECTS:"
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80: s = s[:80]
        print type(x),"\n  ", s

def load(squid, h5f):
    for channel in xrange(squid.channel_count):
        print "Reading channel %d ..." % channel
        h5f.root.raw_data[channel, :] = squid.get_channel(channel)
    
if __name__ == "__main__":
    import gc
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)
    
    
    for sqd_filename in sys.stdin:
        sqd_filename = sqd_filename.strip()
        print sqd_filename
        
        squid = SquidData(sqd_filename)
        
        h5_filename      = sqd_filename[0:-3] + "h5"
        array_shape      = (squid.channel_count, squid.actual_sample_count)
        #array_filters    = tables.Filters(complevel=1, complib='zlib')
        array_filters = tables.Filters(complevel=0)
        
        h5f = tables.openFile(h5_filename, mode='w', title="MEG data")
        
        h5f.createCArray(h5f.root, 'raw_data', tables.Int16Atom(), array_shape, filters=array_filters)
        h5f.createCArray(h5f.root, 'convfactor', tables.Float32Atom(), shape(squid.convfactor), filters=array_filters)
        h5f.root.convfactor[:] = squid.convfactor
        
        load(squid, h5f)
        
        print "Output %s" % h5_filename
        h5f.close()
        
        dump_garbage()