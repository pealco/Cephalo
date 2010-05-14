#from pylab import *
from itertools import izip
from utility import *
from numpy import *

def deriv(signal):
    first  = [signal[1] - signal[0]]
    middle = [(b-a)/2.0 for a, b in izip(signal, signal[2:])]
    last   = [signal[-1] - signal[-2]]
    
    return first + middle + last

def smooth(signal, smooth_width, n=1):
    """Smooths an array `signal` `n` times with a triangular smooth of width `smooth_width`.
    
    Parameters
    ----------
    signal : array_like
        Input array
    smooth_width : int
        The width of the smooth.
    n : int, optional
        The number of times signal is smoothed
    
    Returns
    -------
    signal : ndarray
        The signal, smoothed `n` times.
    """
        
    s = signal
    
    for _ in xrange(n):
        half_width = int(round(smooth_width/2.0))
        sum_points = sum(signal[:smooth_width])
        s = zeros(shape(signal))
        for k in xrange(len(signal) - smooth_width):
            s[k + half_width - 1] = sum_points
            sum_points -= signal[k]
            sum_points += signal[k + smooth_width]
        s /= float(smooth_width)
        signal = s
    
    return signal

def find_peaks(x, signal, slope_threshold, amplitude_threshold, smooth_width, peak_group):
    smoothed_derivative = smooth(deriv(signal), smooth_width, n=2)
    half_peak_group = int(round(float(peak_group)/2 + 1))
    P = []
    signal_length = len(signal)
            
    for j in xrange(smooth_width, len(signal) - smooth_width):
        
        # Conditions for being a peak:
        # (1) Crossing zero.
        # (2) Slope of derivative is larger than slope_threshold.
        # (3) Height of peak is larger than amp_threshold.
        crossing_zero_condition = sign(smoothed_derivative[j]) > sign(smoothed_derivative[j+1])
        slope_condition         = smoothed_derivative[j] - smoothed_derivative[j+1] > slope_threshold * signal[j]
        amplitude_condition     = signal[j] > amplitude_threshold
        
        if crossing_zero_condition and slope_condition and amplitude_condition:
            peak_group_x, peak_group_y = zeros(peak_group), zeros(peak_group)
            
            # Grab the `peak_group` points around the peak.
            # Store them in `peak_group_x` and `peak_group_y`
            for k in xrange(peak_group):
                peak_group_index = j + k - half_peak_group + 1
                if peak_group_index < 1: peak_group_index = 1
                if peak_group_index > signal_length: peak_group_index = signal_length
                peak_group_x[k] = x[peak_group_index]
                peak_group_y[k] = signal[peak_group_index]
            
            # Center scale `peak_group_x`.
            peak_group_x, peak_group_x_mean, peak_group_x_std = scale(peak_group_x, full=True)
            
            # Fit peak_group to a parabola to find the peak.
            coefficients, error = fit_parabola(peak_group_x, peak_group_y)
            c1, c2, c3 = reversed(coefficients)
            
            peak_x = -((peak_group_x_std * c2 / (2 * c3)) - peak_group_x_mean)
            peak_y = exp(c1 - c3 * (c2 / (2 * c3)) ** 2)
            
            P.append([peak_x, peak_y])
            print error

    return asarray(P)

def fit_parabola(x, y):
    coefficients = polyfit(x, log(abs(y)), deg=2)
    model_fit = polyval(coefficients, x)
    error = rms_error(x, model_fit)
    
    return coefficients, error

if __name__ == "__main__":
    x = arange(0, 60, 0.1)
    y = sin(x)
    print find_peaks(x, y, 0, 0.002, 7, 7)
    
    
    
    
    
    
    
    
    
    
