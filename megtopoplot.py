import matplotlib
#matplotlib.use('Agg')
from numpy import *
from scipy.io import mio
from pylab import *
import cProfile
#import psyco
import Image
#psyco.full()


def getSensorLocs():
    SENSOR_COORDS =  [
        [77.48, 91.71, -58.68, ], 
        [56.28, 105.15, -50.77, ], 
        [35.81, 115.02, -43.79, ], 
        [10.68, 120.84, -42.69, ], 
        [-18.56, 119.97, -40.68, ], 
        [-43.24, 114.67, -39.27, ], 
        [-63.44, 103.22, -43.81, ], 
        [-84.75, 89.73, -46.47, ], 
        [-103.47, 71.54, -44.68, ], 
        [-117.79, 50.30, -42.75, ], 
        [-119.79, -5.42, 57.87, ], 
        [-127.60, 7.09, -39.99, ], 
        [-127.67, -14.88, -40.66, ], 
        [-127.49, -18.32, 17.46, ], 
        [-111.62, -59.78, -46.71, ], 
        [-94.80, -78.88, -49.19, ], 
        [-74.15, -93.18, -47.08, ], 
        [-55.90, -105.52, -44.53, ], 
        [-34.20, -115.14, -44.97, ], 
        [-9.83, -123.20, -44.98, ], 
        [17.77, -121.17, -48.15, ], 
        [40.33, -109.33, -51.46, ], 
        [58.32, -98.79, -55.70, ], 
        [78.94, -87.27, -56.84, ], 
        [84.69, -85.41, -30.82, ], 
        [-40.40, -69.31, 107.99, ], 
        [17.12, -119.43, -18.13, ], 
        [-4.56, -118.70, -15.56, ], 
        [-55.09, -108.85, -17.95, ], 
        [-72.28, -30.09, 115.40, ], 
        [-92.42, -79.87, -21.14, ], 
        [-76.87, -5.15, 117.02, ], 
        [-131.13, -16.26, -12.63, ], 
        [-132.20, 9.78, -10.64, ], 
        [-114.90, 55.51, -11.51, ], 
        [-72.38, 17.32, 117.04, ], 
        [-80.92, 90.85, -21.21, ], 
        [-59.79, 103.81, -10.02, ], 
        [-10.97, 118.58, -14.41, ], 
        [14.43, 118.19, -16.67, ], 
        [-46.75, 56.59, 114.66, ], 
        [80.48, 89.58, -32.43, ], 
        [85.09, 89.16, 2.95, ], 
        [63.82, 101.72, 3.37, ], 
        [40.57, 111.80, 4.88, ], 
        [-24.62, 70.97, 113.86, ], 
        [-35.02, 112.97, 9.21, ], 
        [-58.75, 104.00, 11.18, ], 
        [-79.84, 91.10, 15.85, ], 
        [-113.08, 55.32, 17.96, ], 
        [-123.85, 32.75, 18.26, ], 
        [-129.19, 7.06, 18.27, ], 
        [38.09, 73.33, 107.91, ], 
        [-120.59, -43.02, 15.35, ], 
        [-107.44, -64.99, 13.44, ], 
        [-72.77, -94.31, 8.57, ], 
        [-52.14, -110.56, 7.46, ], 
        [-21.42, -117.21, 3.99, ], 
        [75.13, 41.73, 106.72, ], 
        [47.29, -113.28, 0.08, ], 
        [70.83, -97.76, -1.33, ], 
        [88.25, -85.36, -2.63, ], 
        [89.21, -83.32, 21.18, ], 
        [71.36, -97.09, 19.73, ], 
        [64.70, 27.68, 119.12, ], 
        [22.34, -118.48, 21.82, ], 
        [-0.29, -117.97, 20.71, ], 
        [51.04, 46.90, 120.42, ], 
        [-70.71, -94.17, 31.25, ], 
        [-88.51, -80.25, 35.76, ], 
        [-105.28, -61.85, 37.16, ], 
        [2.41, 61.68, 125.77, ], 
        [-123.45, -16.80, 38.44, ], 
        [-25.83, 53.32, 126.16, ], 
        [-120.30, 30.25, 39.94, ], 
        [-111.05, 51.63, 40.96, ], 
        [-95.94, 72.67, 40.49, ], 
        [-76.96, 90.47, 38.31, ], 
        [-55.73, 16.51, 129.05, ], 
        [-5.70, 116.21, 30.63, ], 
        [19.26, 115.15, 29.59, ], 
        [-54.06, -28.04, 124.58, ], 
        [66.91, 99.00, 26.48, ], 
        [87.48, 86.02, 27.91, ], 
        [81.94, 83.88, 51.40, ], 
        [41.23, 106.51, 50.89, ], 
        [-21.79, -63.13, 120.35, ], 
        [-35.70, 106.70, 54.09, ], 
        [-59.54, 96.81, 57.11, ], 
        [6.35, -69.44, 118.58, ], 
        [-80.24, 81.70, 59.28, ], 
        [-117.94, 18.29, 58.88, ], 
        [53.15, -49.61, 116.71, ], 
        [-115.74, -30.06, 57.03, ], 
        [-92.73, -70.60, 54.64, ], 
        [65.29, -31.85, 116.79, ], 
        [-54.80, -99.61, 49.47, ], 
        [-31.41, -112.06, 49.83, ], 
        [72.19, 8.11, 118.18, ], 
        [43.48, -108.39, 44.39, ], 
        [82.93, -84.60, 46.01], 
        [100.65, -70.04, 44.65], 
        [116.09, -50.89, 45.34], 
        [126.15, -26.48, 46.13], 
        [130.77, 0.55, 47.11], 
        [126.00, 27.34, 47.03], 
        [115.57, 49.65, 48.86], 
        [101.18, 68.11, 48.71], 
        [89.61, 67.58, 71.22], 
        [54.79, 6.70, 128.78], 
        [86.50, 19.28, 108.47], 
        [121.65, -0.17, 70.06], 
        [117.18, -27.51, 69.17], 
        [54.03, -15.06, 127.99], 
        [91.70, -69.21, 66.57], 
        [20.37, -48.71, 131.09], 
        [54.40, -94.98, 65.60], 
        [34.32, -103.09, 65.59], 
        [10.23, -105.39, 68.36], 
        [-17.04, -103.96, 69.15], 
        [-31.26, -30.03, 135.36], 
        [-80.50, -72.42, 75.32], 
        [-94.45, -55.06, 77.76], 
        [-105.34, -34.54, 79.14], 
        [-110.81, -11.75, 80.62], 
        [-38.85, -4.54, 136.36], 
        [-102.44, 34.05, 84.97], 
        [-87.74, 57.79, 83.19], 
        [-33.50, 21.87, 137.26], 
        [-27.30, 100.59, 77.06], 
        [2.71, 103.33, 74.00], 
        [29.96, 101.22, 72.45], 
        [52.42, 93.93, 71.82], 
        [19.95, 40.88, 135.47], 
        [64.82, 75.19, 90.09], 
        [45.97, 85.46, 90.00], 
        [-7.71, 92.02, 94.69], 
        [-54.67, 73.44, 98.20], 
        [-71.59, 56.36, 101.72], 
        [26.56, 18.62, 140.83], 
        [-92.22, 16.12, 102.62], 
        [-90.55, -32.33, 100.28], 
        [-1.11, 18.61, 144.80], 
        [-67.28, -69.80, 93.37], 
        [-48.69, -81.91, 91.19], 
        [-4.33, -95.55, 85.83], 
        [-0.90, -27.57, 142.88], 
        [61.99, -80.90, 85.73], 
        [92.90, -50.73, 87.19], 
        [25.31, -26.50, 138.85], 
        [105.58, 18.70, 92.26], 
        [97.81, 41.18, 95.87], 
        [38.82, -78.56, 100.91], 
        [89.52, -4.64, 107.41], 
        [85.97, -27.66, 105.56], 
        [74.98, -47.02, 103.48], 
        [-17.47, -81.12, 105.10] ]
        
    x = array([i[0] for i in SENSOR_COORDS])
    y = array([i[1] for i in SENSOR_COORDS])
    z = array([i[2] for i in SENSOR_COORDS])
        
    alphaCorr = arccos(z/max(z))    # use z to get the correct alpha, which is the angle with z-axis (in spherical coordinates)
    betaCorr = -arctan2(y,x)         # use x,y to get the correct beta, which is the angle with x-axis (in spherical coordinates)
 
    # flatten the sphere
    xx =  alphaCorr*sin(betaCorr)
    yy =  alphaCorr*cos(betaCorr)

    return xx, yy


def drawTopoHead(R = 2.04):
    incr = 0.02
    headpts = arange(-R,R,incr)
    plot(headpts, sqrt(abs(R**2-headpts**2)),'k',headpts, -sqrt(abs(R**2-headpts**2)),'k')
    plot([-0.1, 0, 0.1],[R, R+0.2, R],'k')
    
    earR=0.2
    earPtsL = arange(-R-earR,-R+0.02,incr)
    plot(earPtsL,sqrt(abs(earR**2-(earPtsL+R)**2)),'k')
    plot(earPtsL,-sqrt(abs(earR**2-(earPtsL+R)**2)),'k')
    
    earptsR = arange(R-.02,R+earR,incr)
    plot(earptsR,sqrt(abs(earR**2-(earptsR-R)**2)),'k')
    plot(earptsR,-sqrt(abs(earR**2-(earptsR-R)**2)),'k')
     
    earR=0.1
    earPtsL = arange(-R-earR,incr-R+0.02,incr)
    plot(earPtsL,sqrt(abs(earR**2-(earPtsL+R)**2)),'k')
    plot(earPtsL,-sqrt(abs(earR**2-(earPtsL+R)**2)),'k')
    
    earptsR = arange(R-0.02,R+earR,incr)
    plot(earptsR,sqrt(abs(earR**2-(earptsR-R)**2)),'k')
    plot(earptsR,-sqrt(abs(earR**2-(earptsR-R)**2)),'k')
'''    
def customMap(sinkmin, sourcemax,absmax):
    total = sourcemax - sinkmin
    zeropoint = abs(sinkmin)/total
    if max(abs(sinkmin),sourcemax,absmax) != absmax: # We're going to saturate
        redsat = min(zeropoint+(absmax/sourcemax)/2,1)
        bluesat = max(zeropoint-(absmax/abs(sinkmin))/2,0)
        cdict = {
            'red':  [(0,0,0),(bluesat,0,0),(zeropoint,1,1),(redsat,1,1),(1.0,1,1)],
            'blue': [(0,1,1),(bluesat,1,1),(zeropoint,1,1),(redsat,0,0),(1.0,0,0)],
            'green':[(0,0,0),(bluesat,0,0),(zeropoint,1,1),(redsat,0,0),(1.0,0,0)]
        }
    else: 
        redmax = sourcemax/absmax
        bluemax = abs(sinkmin)/absmax
        cdict = {
            'red':  [(0,0,0),(zeropoint,1,1),(1.0,redmax,redmax)],
            'blue': [(0,bluemax,bluemax),(zeropoint,1,1),(1.0,0,0)],
            'green':[(0,0,0),(zeropoint,1,1),(1.0,0,0)]
        }
        
    return matplotlib.colors.LinearSegmentedColormap('my_colromap',cdict,256)
'''  
def buRdMap():
    cdict = {
            'red':  [(0,0,0),(0.5,1,1),(1.0,1,1)],
            'blue': [(0,1,1),(0.5,1,1),(1.0,0,0)],
            'green':[(0,0,0),(0.5,1,1),(1.0,0,0)]
    }
    return matplotlib.colors.LinearSegmentedColormap('my_colromap',cdict,256)    

def blkMap():
    cdict ={'red' : [(0,0,0),(1,0,0)],
        'green' : [(0,0,0),(1,0,0)],
        'blue' : [(0,0,0),(1,0,0)]}
    
    return matplotlib.colors.LinearSegmentedColormap('my_colromap)',cdict,256)
 
def megTopoPlot(cdata, line='true',saturate = 700):
    [xi, yi] = meshgrid(arange(-135,135)/135.0*2.5, arange(-135,135)/135.0*2.5)
    [xx, yy] = getSensorLocs()
    toplot = griddata(xx,yy,cdata,xi,yi)
    mask = (sqrt(xi**2+yi**2) <= 2.05)
#    buRd = customMap(min(cdata),max(cdata),saturate)
    buRd = buRdMap()
    contourf(xi, yi, toplot, 15, norm = matplotlib.colors.Normalize(vmin = -1*saturate, vmax = saturate), cmap = buRd)
    colorbar()
    if line =='true':
        allblk = blkMap()
        contour(xi, yi, toplot, 15, cmap = allblk)
    drawTopoHead()
    xlim(-2.5,2.5)
    ylim(-2.5,2.5)
#    show()
    
def test():    

    data  = mio.loadmat('testdata.mat')
    data = data["onepoint"]
    figure()
    megTopoPlot(data, line = 'true', saturate = 700)
    savefig('testfig.png')
    im = Image.open('testfig.png')
    im.show()
    
if __name__ == "__main__":
    cProfile.run('test()')