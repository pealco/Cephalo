def rms_error(a, b):
    return rms(a - b)

def rms(data, axis=0):
    return sqrt(mean(data ** 2, axis))
    
def scale(a, full=False):
    a_mean = a.mean()
    a_std = a.std(ddof=1)
    a_scaled = (a - a_mean) / a_std
    
    if full:
        return a_scaled, a_mean, a_std
    else:
        return a_scaled