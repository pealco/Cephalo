import sys
import yaml
import tables
from lib.megprocess import *

class Configuration():
    def __init__(self):
        self.get_config()
    
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
            self.trigger_channels = sorted(self.standards.keys() + self.deviants.keys())
            self.num_of_conditions = len(self.trigger_channels)
    
        if 'subjects' not in config or config['subjects'] == {}:
            raise ValueError("No subjects specified.")
        else:
            self.subjects = config['subjects']

class Model():
    
    def __init__(self, config):
        self.config = config
    
    def process(self, subject, channels_of_interest):
        
        self.config.h5_file = self.config.data_directory + subject + ".h5"
        
        print "Working on ", h5_file, "..."
        data = Data(self.config.h5_file, self.config.trigger_channels)
                
        front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23]
        loaded_channels = front_sensors + channels_of_interest
        
        if "/lowpass_data" not in data.h5_file:
            print "Filtering ..."
            for c in range(157):
                data.h5_file.root.lowpass_data[c] = lowpass(data.h5_file.root.raw_data[c] * data.h5_file.root.convfactor[c], 1000, 20) 
        
        # Raw epochs.
        epochs = epoch(data.h5_file.root.raw_data, 
                       data.h5_file.root.triggers, 
                       loaded_channels, 
                       config=self.config) 
        
        # Filtered epochs.
        epochs_filtered = epoch(data.h5_file.root.lowpass_data, 
                                data.h5_file.root.triggers, 
                                loaded_channels, 
                                config=self.config) 
        
        data.epochs = baseline(epochs.copy(), self.config.epoch_pre)
        data.epochs_filtered = baseline(epochs_filtered.copy(), self.config.epoch_pre)
        
        #save_epochs(data, epochs, epochs_filtered)
        
        data.mean_epochs = zeros((self.config.num_of_conditions, shape(epochs)[1], len(channels_of_interest)))    
        for c in range(self.config.num_of_conditions):
            accepted_epochs = reject_epochs(epochs[c, :, :, :], method="diff")
            rejected_epochs = list(set(range(shape(epochs[c,:,:,:])[2])) - set(accepted_epochs))
            
            data.mean_epochs[c,:,:] = mean(data.epochs_filtered[c, :, len(front_sensors):, accepted_epochs], 0)
        
        #rms_mean_epochs = rms(mean_epochs, 2)
        
        data.h5_file.close()
        
        #return rms_mean_epochs
        return data
        
    def analyze(self):
        
        for subject, channels in self.config.subjects.iteritems():
            self.process(subject, channels)
        
        self.mean_epochs = [self.process(subject, channels) for subject, channels in self.config.subjects.iteritems()]
        
        #self.allsubjs = [self.process(subject, channels) for subject, channels in self.config.subjects.iteritems()]
        
        #self.grand_average = mean(self.allsubjs, axis=0)
        

class View():
    
    def __init__(self, model):
        self.model = model
    
    def plot_mmf(self):
        
        for standard in self.model.config.standards:
            pass
        
        for deviant in self.model.config.deviants:
            pass
        
        grand_average = self.model.grand_average
        
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
    
    
    
    def output_for_r(self):
        self.model.mean_epochs = array(self.model.mean_epochs)
        subjects, conditions, samples, channels = shape(self.model.mean_epochs)
        print shape(self.model.mean_epochs)
        
        out = "subject condition sample channel value\n"
        
        for subject in xrange(subjects):
            for condition in xrange(conditions):
                for sample in xrange(samples):
                    for channel in xrange(channels):
                        out += "s%d c%d %d ch%d %f\n" % (subject+1, condition+1, sample-self.model.config.epoch_pre, channel+1, self.model.mean_epochs[subject, condition, sample, channel])
                    
        return out
    
    def to_table(self, data):
        table = data.createTable(
                    where=data.root,
                    name='epochsTable',
                    description=Sample
                    )
        
        sample_row = table.row
        self.model.mean_epochs = array(self.model.mean_epochs)
        subjects, conditions, samples, channels = shape(self.model.mean_epochs)
        for subject in xrange(subjects):
            for condition in xrange(conditions):
                for sample in xrange(samples):
                    for channel in xrange(channels):
                        sample_row['subject'] = subject
                        sample_row['condition'] = condition
                        sample_row['sample'] = sample-self.model.config.epoch_pre
                        sample_row['channel'] = channel
                        sample_row['hemisphere_x'] = hemisphere(channel, axis='x')
                        sample_row['hemisphere_y'] = hemisphere(channel, axis='y')
                        sample_row['amplitude'] = amplitude
                        
        return True
        
        
class Sample(IsDescription):
    subject   = StringCol(5)
    condition = Int32Col()
    sample    = Int32Col()
    channel   = Int32Col()
    amplitude = Float32Col()
    hemisphere_x = BoolCol() # Left is True, Right is False
    hemisphere_y = BoolCol() # Anterior is True, Posterior is False
        
    

class Experiment():
    def __init__(self):
        
        # Models
        self.config = Configuration()
        self.model = Model(self.config)
        
        self.model.analyze()
        
        # Views
        self.view = View(self.model)
        
        output = self.view.output_for_r()
        self.save("output.txt", output)
        
        #self.view.plot_mmf()
        
    def save(self, filename, contents):
        fh = open(filename, 'w')
        fh.write(contents)
        fh.close()

class Data(object):
    
    def __init__(self, h5_filename, trigger_channels):
        self.h5_file = self.load_data(h5_filename, trigger_channels)
    
    def load_data(self, h5_filename, trigger_channels):
        """Loads an H5 data file containing MEG data."""
        
        print "Loading data ..."
        
        self.h5_file = tables.openFile(h5_filename, mode = "r+")
        raw_data = self.h5_file.root.raw_data
        
        # Create CArray for lowpassed data.
        if "/lowpass_data" not in self.h5_file:
            lowpass_data = self.h5_file.createCArray(
                where=self.h5_file.root, 
                name='lowpass_data', 
                atom=tables.Float32Atom(), 
                shape=shape(raw_data),
                filters=tables.Filters(1)
                )
                
        self.load_triggers()
        
    
    def load_triggers(self):
        """Create and fill triggers VLArray. Allows for ragged rows."""
        if "/triggers" in self.h5_file:
            self.h5_file.root.triggers.remove()
            
        self.triggers = self.h5_file.createVLArray(
                       where=self.h5_file.root, 
                       name='triggers',
                       atom=tables.Int32Atom(),
                       filters=tables.Filters(1)
                       )
                       
        print "Finding triggers ..."
        for trigger_set in find_triggers(self.raw_data, self.trigger_channels):
            self.triggers.append(trigger_set)
        
    
class Channel(object):
    def __init__(self, channel_number):
        self.channel_number = channel_number
        
        left      = [  1,   2,   3,   4,   5,   6,   7,   8,   9,  11, 
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
        
        anterior  = [ ]
        
        posterior = [ ]
        
        if self.channel_number in left:
            self.hemisphere_x = "left"
        elif self.channel_number in right:
            self.hemisphere_x = "right"
        else:
            raise ValueError("Channel %d is not a valid channel." % self.channel_number)
            
        if self.channel_number in anterior:
            self.hemisphere_y = "anterior"
        elif self.channel_number in posterior:
            self.hemisphere_y = "posterior"
        else:
            raise ValueError("Channel %d is not a valid channel." % self.channel_number)
        

    
        
        
            
    
if __name__ == "__main__":
    
    exp = Experiment()

