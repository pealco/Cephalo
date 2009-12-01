"""Some utility functions."""

from numpy import sqrt, mean
import os

def rms_error(array_a, array_b, axis=0):
    """Computes RMS error."""
    return rms(array_a - array_b, axis=axis)

def rms(data, axis=0):
    """Computes root mean square (RMS)."""
    return sqrt(mean(data ** 2, axis))
    
def scale(_array, full=False):
    """Scales an array to unit standard devations. (AKA z-score.)"""
    a_mean = _array.mean()
    a_std = _array.std(ddof=1)
    a_scaled = (_array - a_mean) / a_std
    
    if full:
        return a_scaled, a_mean, a_std
    else:
        return a_scaled

def save_table(filename, contents):
    """Saves a table to file."""
    
    filename = os.path.normpath(filename)
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        
    _file = open(filename, 'w')
    _file.write(contents)
    _file.close()

def get_hemisphere(channel, axis, boolean=False):
    """Determines in which hemisphere (both left/right, anterior/posterior)
    a channel is located."""
    
    left      = [ 0,  1,   2,   3,   4,   5,   6,   7,   8,   9,  11, 
                  33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  
                  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
                  58,  64,  67,  71,  73,  74,  75,  76,  77,  78,
                  79,  80,  82,  83,  84,  85,  87,  88,  90,  91,  
                 105, 106, 107, 108, 109, 110, 126, 127, 128, 129, 
                 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 
                 140, 142, 150, 151]
                 
    right     = [ 10,  12,  13,  14,  15,  16,  17,  18,  19,  20, 
                  21,  22,  23,  24,  25,  26,  27,  28,  29,  30, 
                  31,  32,  53,  54,  55,  56,  57,  59,  60,  61,
                  62,  63,  65,  66,  68,  69,  70,  72,  81,  86,
                  89,  92,  93,  94,  95,  96,  97,  98,  99, 100, 
                 101, 102, 103, 104, 111, 112, 113, 114, 115, 116, 
                 117, 118, 119, 120, 121, 122, 123, 124, 125, 141, 
                 143, 144, 145, 146, 147, 148, 149, 152, 153, 154, 
                 155, 156]
    
    anterior  = range(157)
    
    posterior = [ ]
    
    if axis == "x":
        if channel in left:
            hemisphere = "left"
        elif channel in right:
            hemisphere = "right"
        else:
            raise ValueError("Channel %d is not a valid channel." % channel) 
    elif axis == "y":
        if channel in anterior:
            hemisphere = "anterior"
        elif channel in posterior:
            hemisphere = "posterior"
        else:
            raise ValueError("Channel %d is not a valid channel." % channel)
            
    if boolean:
        if hemisphere == "left" or hemisphere == "anterior":
            return False
        else:
            return True
    else:
        return hemisphere
                
            
    