import sys
from megprocess import *
from peak_finding import *

megdata = load_data("R0874.h5")

if "/epochs_filtered" not in megdata:
    print "No epochs in file."
    sys.exit(0)
else:
    
    