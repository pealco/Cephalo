from numpy import *
import tables
from pysqd import SquidData

squid = SquidData('R0874.sqd')

filename = "R0874.h5"
array_shape   = (squid.channel_count, squid.actual_sample_count)
array_atom    = tables.UInt8Atom()
array_filters = tables.Filters(complevel=1, complib='zlib')

h5f = tables.openFile(filename, 'w')

data = h5f.createCArray(h5f.root, 'carray', array_atom, array_shape, filters=array_filters)

for channel in xrange(squid.channel_count):
    print "Reading channel %d ..." % channel
    print shape(squid.get_channel(channel))

h5f.close()