from megprocess import *
from numpy import savetxt


def plot_mmf(rms_mean_epochs):

    standard_4 = rms_mean_epochs[0, :]  # dlif  standard
    deviant_3  = rms_mean_epochs[1, :]  # delif deviant
    standard_3 = rms_mean_epochs[2, :]  # delif standard
    deviant_4  = rms_mean_epochs[3, :]  # dlif  deviant
    standard_2 = rms_mean_epochs[4, :]  # ldif  standard
    deviant_1  = rms_mean_epochs[5, :]  # ledif deviant
    standard_1 = rms_mean_epochs[6, :]  # ledif standard
    deviant_2  = rms_mean_epochs[7, :]  # ldif  deviant

    
    difference_wave_1 = difference_wave(standard_1, deviant_1) # ledif
    difference_wave_2 = difference_wave(standard_2, deviant_2) # ldif 
    difference_wave_3 = difference_wave(standard_3, deviant_3) # delif
    difference_wave_4 = difference_wave(standard_4, deviant_4) # dlif
    
    figure()
    
    subplot(211)
    title("ledif")
    plot(standard_1, label="standard")
    plot(deviant_1, label="deviant")
    #xlim(300, 400)
    #ylim(0, 70)
    legend()
    
    subplot(212)
    title("ldif")
    plot(standard_2, label="standard")
    plot(deviant_2, label="deviant")
    #xlim(300, 400)
    #ylim(0, 70)
    legend()
    
    figure()
    
    subplot(211)
    title("delif")
    plot(standard_3, label="standard")
    plot(deviant_3, label="deviant")
    #xlim(300, 400)
    #ylim(0, 70)
    legend()
    
    subplot(212)
    title("dlif")
    plot(standard_4, label="standard")
    plot(deviant_4, label="deviant")
    #xlim(300, 400)
    #ylim(0, 70)
    legend()

    figure()
    
    subplot(211)
    title("LD - Sonority -1")
    plot(difference_wave_1, label="ledif dv-st") # ledif
    plot(difference_wave_2, label="ldif dv-st") # ldif 
    #xlim(300, 400)
    #ylim(-50, 50)
    legend()
    
    subplot(212)
    title("DL - Sonority +3")
    plot(difference_wave_3, label="delif dv-st") # delif
    plot(difference_wave_4, label="dlif dv-st") # dlif
    #xlim(300, 400)
    #ylim(-50, 50)
    legend()
    
    ld_wave = difference_wave_1 - difference_wave_2
    dl_wave = difference_wave_3 - difference_wave_4
    
    figure()
    
    subplot(211)
    plot(ld_wave, label="LD")
    plot(dl_wave, label="DL")
    #xlim(300, 400)
    legend()
    
    subplot(212)
    plot(ld_wave - dl_wave)
    #xlim(300, 400)
    
    figure()
    
    title("deviants")
    plot(difference_wave_2, label="ldif")
    plot(difference_wave_4, label="delif")
    #xlim(300, 400)
    #ylim(0, 70)
    legend()

    show()

def process(h5_file, channels_of_interest):
    
    print "Working on ", h5_file, "..."
    megdata = load_data(h5_file, [162, 163, 164, 165, 166, 167, 168, 169])
    
    front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23]
    loaded_channels = front_sensors + channels_of_interest
    
    print "Filtering ..."
    for c in range(157):
        megdata.root.lowpass_data[c] = lowpass(megdata.root.raw_data[c] * megdata.root.convfactor[c], 1000, 20) 
    
    epochs = epoch(megdata.root.raw_data, megdata.root.triggers, range(157), range(8)) # Raw epochs.
    epochs_filtered = epoch(megdata.root.lowpass_data, megdata.root.triggers, range(157), range(8)) # Filtered epochs.
    
    epochs = baseline(epochs.copy())
    epochs_filtered = baseline(epochs_filtered.copy())
    
    save_epochs(megdata, epochs, epochs_filtered)
    
    mean_epochs = zeros((8, shape(epochs)[1], len(channels_of_interest)))    
    for c in range(8):
    	accepted_epochs = reject_epochs(epochs[c, :, :, :], method="diff")
    	rejected_epochs = list(set(range(shape(epochs[c,:,:,:])[2])) - set(accepted_epochs))
    	#for e in rejected_epochs:
    	#    figure()
    	#    plot(epochs[c,:,:,e])
    	
    	#show()
    	mean_epochs[c,:,:] = mean(epochs_filtered[c, :, len(front_sensors):, accepted_epochs], 0)
    
    rms_mean_epochs = rms(mean_epochs, 2)
    
    megdata.close()
    
    return rms_mean_epochs


if __name__ == "__main__":

    left_hemisphere  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 58, 64, 67, 71, 73, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 87, 88, 90, 91, 105, 106, 107, 108, 109, 110, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 142, 150, 151]
    right_hemisphere = [10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 65, 66, 68, 69, 70, 72, 81, 86, 89, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 141, 143, 144, 145, 146, 147, 148, 149, 152, 153, 154, 155, 156]
    
    directory = ""
    
    subjects = [
        #(directory + "R0692.h5", [c for c in [25, 39, 40, 44, 59, 60, 80, 85, 90, 96, 99, 116, 117, 127, 137, 138, 143, 144, 156] if c in left_hemisphere]),
        #(directory + "R0874.h5", [c for c in [25, 43, 44, 59, 60, 61, 62, 63, 80, 82, 85, 88, 90, 119, 129, 137, 138, 143, 144, 156] if c in left_hemisphere])
        #(directory + "R1093.h5", [c for c in [44, 79, 80, 85, 88, 90, 96, 97, 99, 116, 117, 118, 121, 127, 129, 131, 137, 138, 143, 144, 152] if c in left_hemisphere])
        #(directory + "R1105.h5", [c for c in [45, 65, 66, 68, 69, 76, 77, 79, 80, 88, 90, 94, 96, 99, 117, 118, 121, 127, 130, 136] if c in left_hemisphere])
        (directory + "R1133.h5", [c for c in [39, 43, 44, 59, 60, 63, 65, 68, 80, 82, 87, 88, 90, 96, 97, 99, 119, 129, 137, 144] if c in left_hemisphere])
        #(directory + "R1193.h5", [c for c in [43, 44, 76, 77, 80, 82, 85, 88, 90, 127] if c in left_hemisphere]),
        #(directory + "R1277.h5", [c for c in [43, 44, 77, 80, 82, 85, 87, 88, 90, 129] if c in left_hemisphere]),
        #(directory + "R1292.h5", [c for c in [48, 65, 68, 69, 76, 77, 79, 80, 85, 88, 90, 94, 96, 99, 116, 117, 118, 121, 130, 131] if c in left_hemisphere]),
        #(directory + "R1344.h5", [c for c in [25, 39, 40, 43, 44, 45, 59, 60, 63, 65, 80, 82, 99, 127, 137, 138, 143, 144, 145, 156] if c in left_hemisphere])
        #(directory + "R1348.h5", [c for c in [39, 43, 44, 48, 56, 59, 60, 63, 65, 68, 76, 77, 80, 82, 88, 90, 96, 97, 99] if c in left_hemisphere])
    ]
    
    allsubjs = [process(h5_file, channels) for h5_file, channels in subjects]
    print shape(allsubjs)
    
    print "Grand averaging ..."
    grandaverage = mean(allsubjs, axis=0)
    
    print "Saving ..."
    savetxt("grandaverage.txt", grandaverage, delimiter=',')
    plot_mmf(grandaverage)
    
    
    
    #process("R1277-sonority-Filtered.sqd.mat", [43, 44, 80, 82, 85, 77, 87, 88, 90, 129, 63, 99, 116, 117, 118, 69, 94, 121, 122, 143])
    #R0874 [25, 26, 43, 44, 59, 60, 63, 65, 80, 82, 85, 87, 88, 90, 137, 143, 144, 145, 156]