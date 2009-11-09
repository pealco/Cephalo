import sys
import yaml
import tables
from lib.megprocess import *

class Model():
    def get_config(self):
        try:
            config_file = sys.argv[1]
        except IndexError:
            config_file = raw_input("No configuration file specified. Specify one now: ")
        
        self.parse_config(config_file)
        
    def parse_config(self, config_file):
        stream = file(config_file, 'r')
        config = yaml.load(stream)
        
        # Set default experiment name.
        if 'name' in config:
            self.name = config['name']
        else:
            self.name = "Untitled MEG experiment"
        
        # Set default experimenter name
        if 'experimenter' in config:    
            self.experimenter = config['experimenter']
        else:
            self.experimenter = "Anonymous Experimenter"
        
        # Set default data directory.
        if 'data_directory' in config:
            self.data_directory = config['data_directory']
        else:
            self.data_directory = "."
            
        # Set epochs
        if 'epoch_pre' not in config:
            self.epoch_pre = 100
            print "epoch_pre unspecified. Setting to 100."
        else:
            self.epoch_pre = config['epoch_pre']
            
        if 'epoch_post' not in config:
            self.epoch_post = 500
            print "epoch_post unspecified. Setting to 500."
        else:
            self.epoch_post = config['epoch_post']
            
        if 'expected_epochs' not in config:
            self.expected_epochs = 100
            print "expected_epochs unspecified. Setting to 100."
        else:
            self.expected_epochs = config['expected_epochs']
        
        # Set default experiment design.
        # TODO: This should be removed once more experiment designs are implemented.
        if 'design' in config:
            self.design = config['design']
        else:
            self.design = "mmf"
            print "No design specified. Assuming this is an MMF design."

        # Load standard and deviants lists.
        if self.design.lower() == "mmf" or self.design.lower() == "mmn":
            if 'standards' not in config or 'deviants' not in config:
                raise ValueError("This is an MMF design and no standards or deviants are specified.")
            self.standards = config['standards']
            self.deviants = config['deviants']
            self.trigger_channels = self.standards.keys() + self.deviants.keys()
            self.num_of_conditions = len(self.trigger_channels)
            
        if 'subjects' not in config or config['subjects'] == {}:
            raise ValueError("No subjects specified.")
        else:
            self.subjects = config['subjects']
        
    def process(self, subject, channels_of_interest):
        h5_file = self.data_directory + subject + ".h5"
        
        print "Working on ", h5_file, "..."
        megdata = load_data(h5_file, self.trigger_channels)
        
        front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23]
        loaded_channels = front_sensors + channels_of_interest
        
        print "Filtering ..."
        for c in range(157):
            megdata.root.lowpass_data[c] = lowpass(megdata.root.raw_data[c] * megdata.root.convfactor[c], 1000, 20) 
        
        epochs = epoch(megdata.root.raw_data, megdata.root.triggers, loaded_channels, range(self.num_of_conditions)) # Raw epochs.
        epochs_filtered = epoch(megdata.root.lowpass_data, megdata.root.triggers, loaded_channels, range(self.num_of_conditions)) # Filtered epochs.
        
        epochs = baseline(epochs.copy())
        epochs_filtered = baseline(epochs_filtered.copy())
        
        save_epochs(megdata, epochs, epochs_filtered)
        
        mean_epochs = zeros((self.num_of_conditions, shape(epochs)[1], len(channels_of_interest)))    
        for c in range(8):
            accepted_epochs = reject_epochs(epochs[c, :, :, :], method="diff")
            rejected_epochs = list(set(range(shape(epochs[c,:,:,:])[2])) - set(accepted_epochs))

            mean_epochs[c,:,:] = mean(epochs_filtered[c, :, len(front_sensors):, accepted_epochs], 0)
        
        rms_mean_epochs = rms(mean_epochs, 2)
        
        megdata.close()
        
        return rms_mean_epochs
        
    def analyze(self):
        self.allsubjs = [self.process(subject, channels) for subject, channels in self.subjects.iteritems()]
        self.grand_average = mean(self.allsubjs, axis=0)
    
        
class View():
    def plot_mmf(self, grand_average):
        
        for standard in self.model.standards:
            
        
        for deviant in self.model.standards:
            pass
        
        standard_4 = grand_average[0, :]  # dlif  standard
        deviant_3  = grand_average[1, :]  # delif deviant
        standard_3 = grand_average[2, :]  # delif standard
        deviant_4  = grand_average[3, :]  # dlif  deviant
        standard_2 = grand_average[4, :]  # ldif  standard
        deviant_1  = grand_average[5, :]  # ledif deviant
        standard_1 = grand_average[6, :]  # ledif standard
        deviant_2  = grand_average[7, :]  # ldif  deviant


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
        
        show()
    
        
class Experiment():
    def __init__(self):
        self.model = Model()
        self.view = View()
        
        self.model.get_config()        
        self.model.analyze()
        
        self.view.plot_mmf(self.model.grand_average)
        

        
    

exp = Experiment()
