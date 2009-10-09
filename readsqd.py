from numpy import *
import tables
from pysqd import SquidData
import sys

sqd_filename = sys.argv[1]

squid = SquidData(sqd_filename)

h5_filename = sqd_filename[0:-3] + "h5"
array_shape   = (squid.channel_count, squid.actual_sample_count)
array_atom    = tables.Int16Atom()
#array_filters = tables.Filters(complevel=1, complib='zlib')
array_filters = tables.Filters(complevel=0)

h5f = tables.openFile(h5_filename, 'w')

data = h5f.createCArray(h5f.root, 'data', array_atom, array_shape, filters=array_filters)


for channel in xrange(squid.channel_count):
    print "Reading channel %d ..." % channel
    data[channel, :] = squid.get_channel(channel)

print "Output %s" % h5_filename
h5f.close()