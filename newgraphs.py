from megprocess import *
import csv
import pickle


fhandle = open('results.pickled','r')
results = pickle.load(fhandle)

conds = unique([x[1] for x in results])
hemi = unique([x[3] for x in results])
role = unique([x[2] for x in results])

collapse = []
for c in conds:
    for h in hemi:
        for r in role:
            temp=[]
            for i in results:
                if (i[1]==c and i[2]==r and i[3]==h):
                    temp.append(i[4])
            collapse.append([c,h,r,mean(temp,0)])
            
colcols = {}
for c in conds:
    for h in hemi:
        temp = {}
        for i in collapse:
            if (i[0]==c and i[1]==h):
                temp[i[2]]=i[3]
        colcols[c+h.replace('_hemisphere','')]=[temp['std'],temp['dev']]

figure(1)        
subplot(2,2,1)
title('Left Hemisphere\nOctave-Seventh (Sine)')
plot(colcols['oct1_sineleft'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct1_sineleft'][1], label="Octave_Dev",color='green')
plot(colcols['7th_sineleft'][0], label="Seventh_Std",color='lightblue')
plot(colcols['7th_sineleft'][1], label="Seventh_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

subplot(2,2,2)
title('Right Hemisphere\nOctave-Seventh (Sine)')
text(100,100,'Right Hemisphere')
plot(colcols['oct1_sineright'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct1_sineright'][1], label="Octave_Dev",color='green')
plot(colcols['7th_sineright'][0], label="Seventh_Std",color='lightblue')
plot(colcols['7th_sineright'][1], label="Seventh_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

subplot(2,2,3)
title('Left Hemisphere\nOctave-Seventh (Formant)')
plot(colcols['oct1_vowelleft'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct1_vowelleft'][1], label="Octave_Dev",color='green')
plot(colcols['7th_vowelleft'][0], label="Seventh_Std",color='lightblue')
plot(colcols['7th_vowelleft'][1], label="Seventh_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

subplot(2,2,4)
title('Right Hemisphere\nOctave-Seventh (Formant)')
plot(colcols['oct1_vowelright'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct1_vowelright'][1], label="Octave_Dev",color='green')
plot(colcols['7th_vowelright'][0], label="Seventh_Std",color='lightblue')
plot(colcols['7th_vowelright'][1], label="Seventh_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

figure(2)        
subplot(2,2,1)
title('Left Hemisphere\nOctave-Two Octaves (Sine)')
plot(colcols['oct2_sineleft'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct2_sineleft'][1], label="Octave_Dev",color='green')
plot(colcols['2oct_sineleft'][0], label="Two Octaves_Std",color='lightblue')
plot(colcols['2oct_sineleft'][1], label="Two Octaves_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

subplot(2,2,2)
title('Right Hemisphere\nOctave-Two Octaves (Sine)')
text(100,100,'Right Hemisphere')
plot(colcols['oct2_sineright'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct2_sineright'][1], label="Octave_Dev",color='green')
plot(colcols['2oct_sineright'][0], label="Two Octaves_Std",color='lightblue')
plot(colcols['2oct_sineright'][1], label="Two Octaves_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

subplot(2,2,3)
title('Left Hemisphere\nOctave-Two Octaves (Formant)')
plot(colcols['oct2_vowelleft'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct2_vowelleft'][1], label="Octave_Dev",color='green')
plot(colcols['2oct_vowelleft'][0], label="Two Octaves_Std",color='lightblue')
plot(colcols['2oct_vowelleft'][1], label="Two Octaves_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()

subplot(2,2,4)
title('Right Hemisphere\nOctave-Two Octaves (Formant)')
plot(colcols['oct2_vowelright'][0], label="Octave_Std",color='lightgreen')
plot(colcols['oct2_vowelright'][1], label="Octave_Dev",color='green')
plot(colcols['2oct_vowelright'][0], label="Two Octaves_Std",color='lightblue')
plot(colcols['2oct_vowelright'][1], label="Two Octaves_Dev",color='navy')
xticks(array([0,100,200,300,400,500,600]), ('-100', '0', '100', '200', '300','400','500') )
ylim(0, 75)
legend()
show()