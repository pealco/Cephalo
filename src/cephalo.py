import sys
import yaml
import tables
from lib import filters
from numpy import zeros, mean, array, random, shape, size, nan, ma, isnan
from lib.megprocess import baseline, find_triggers
from lib.epoch_rejection import reject_by_std_method, reject_by_diff_method, \
    reject_by_entropy
from lib.utility import get_hemisphere, save_table

class Configuration():
    def __init__(self):
        self.get_config()
    
    def get_config(self):
        """Gets the the configuration file. Asks for one if one is not specified
        at the command line."""
        try:
            config_file = sys.argv[1]
        except IndexError:
            config_file = raw_input(
                "No configuration file specified. Specify one now: ")
        
        self.parse_config(config_file)
        
    
    def parse_config(self, config_file):
        """Parses the configuration file. Makes many class attributes."""
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
            
        if 'output_directory' in config:
            self.output_directory = config['output_directory']
        else:
            self.output_directory = "output/"
    
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
        if 'design' in config:
            self.design = config['design']
        else:
            self.design = "mmf"
            print "No design specified. Assuming this is an MMF design."
    
        # Load standard and deviants lists.
        if self.design.lower() == "mmf" or self.design.lower() == "mmn":
            if 'standards' not in config or 'deviants' not in config:
                raise ValueError("This is an MMF design and no standards or \
                deviants are specified.")
            self.standards = config['standards']
            self.deviants = config['deviants']
            self.trigger_channels = sorted(self.standards.keys() + 
                self.deviants.keys())
            self.num_of_conditions = len(self.trigger_channels)
    
        if 'subjects' not in config or config['subjects'] == {}:
            raise ValueError("No subjects specified.")
        else:
            self.subjects = config['subjects']
            
        if 'sampling_frequency' in config:
            self.sampling_frequency = config['sampling_frequency']
        else:
            self.sampling_frequency = 1000
            print "No sampling frequency specified. Setting to 1000Hz."
            
        if 'lowpass_frequency' in config:
            self.lowpass_frequency = config['lowpass_frequency']
        else:
            self.lowpass_frequency = 20
            print "No lowpass frequency specified. Setting to 20Hz."
            

class Model():
    """Controls the flow of data."""
    
    def __init__(self, config):
        self.config = config
    
    def process(self, subject):
        """Implements the various steps of the processing chain."""
        
        print "Working on", subject, "..."
        data = Data(subject, self.config)
        
        # Lowpass the data
        data.lowpass()
        
        # Epoch data
        data.epoch("raw_data")
        data.epoch("lowpass_data")
        
        # Automatic epoch rejection
        data.reject_epochs(method="diff")
        
        # Compute mean epochs
        data.mean_epochs()
                
        #data.h5_file.close()
        
        return data
        
    def analyze(self):
        """Loops through subjects to process them."""
        self.data = [self.process(subject) for subject in self.config.subjects]

class View():
    """Controls data output."""
    
    def __init__(self, model):
        self.model = model
    
    #def plot_mmf(self):
    #    """Plots the MMF and difference waves."""
    #    
    #    for standard in self.model.config.standards:
    #        pass
    #    
    #    for deviant in self.model.config.deviants:
    #        pass
    #    
    #    grand_average = self.model.grand_average
    #    
    #    standard_4 = grand_average[0, :]  # dlif  standard
    #    deviant_3  = grand_average[1, :]  # delif deviant
    #    standard_3 = grand_average[2, :]  # delif standard
    #    deviant_4  = grand_average[3, :]  # dlif  deviant
    #    standard_2 = grand_average[4, :]  # ldif  standard
    #    deviant_1  = grand_average[5, :]  # ledif deviant
    #    standard_1 = grand_average[6, :]  # ledif standard
    #    deviant_2  = grand_average[7, :]  # ldif  deviant
    #    
    #    
    #    difference_wave_1 = difference_wave(standard_1, deviant_1) # ledif
    #    difference_wave_2 = difference_wave(standard_2, deviant_2) # ldif 
    #    difference_wave_3 = difference_wave(standard_3, deviant_3) # delif
    #    difference_wave_4 = difference_wave(standard_4, deviant_4) # dlif
    #    
    #    figure()
    #    
    #    subplot(211)
    #    title("ledif")
    #    plot(standard_1, label="standard")
    #    plot(deviant_1, label="deviant")
    #    #xlim(300, 400)
    #    #ylim(0, 70)
    #    legend()
    #    
    #    subplot(212)
    #    title("ldif")
    #    plot(standard_2, label="standard")
    #    plot(deviant_2, label="deviant")
    #    #xlim(300, 400)
    #    #ylim(0, 70)
    #    legend()
    #    
    #    figure()
    #    
    #    subplot(211)
    #    title("delif")
    #    plot(standard_3, label="standard")
    #    plot(deviant_3, label="deviant")
    #    #xlim(300, 400)
    #    #ylim(0, 70)
    #    legend()
    #    
    #    subplot(212)
    #    title("dlif")
    #    plot(standard_4, label="standard")
    #    plot(deviant_4, label="deviant")
    #    #xlim(300, 400)
    #    #ylim(0, 70)
    #    legend()
    #    
    #    show()
    
    
    
    def data_table(self, data_sets):
        """Outputs a text table."""
        
        print "Outputting table ..."
        out = "subject condition sample channel value hemisphere_x\n"
        for data in data_sets:
            data.mean_epochs = array(data.mean_epochs)
            conditions, samples, channels = shape(data.mean_epochs)
        
            for condition in xrange(conditions):
                for sample in xrange(samples):
                    for channel in xrange(channels):
                        true_channel = data.channels_of_interest[channel]
                        out += "%s c%d %d ch%d %f %s\n" % (
                                data.subject, 
                                condition+1, 
                                sample-self.model.config.epoch_pre, 
                                true_channel, 
                                data.mean_epochs[condition, sample, channel],
                                get_hemisphere(true_channel, axis='x'),
                                )
                        
            return out
    
    def print_table(self, data_sets):
        """Writes a table to disk."""
        
        out = "subject condition sample channel hemisphere_x hemisphere_y \
            amplitude\n"
        for data in data_sets:
            table = data.h5_file.root.epochsTable.iterrows()
            for row in table:
                if row['hemisphere_x']:
                    hemisphere_x = "right"
                else:
                    hemisphere_x = "left"
                    
                if row['hemisphere_y']:
                    hemisphere_y = "posterior"
                else:
                    hemisphere_y = "anterior"
                
                out += "%s c%d %d ch%d %s %s %f\n" % \
                    (row['subject'], row['condition'], row['sample'], 
                    row['channel'], hemisphere_x, hemisphere_y, 
                    row['amplitude'])
        return out
                
    
    def to_table(self, data_sets):
        """Creates a pytables Table."""
        
        for data in data_sets:
            if "/epochsTable" in data.h5_file:
                data.h5_file.root.epochsTable.remove()
            
            table = data.h5_file.createTable(
                        where='/',
                        name='epochsTable',
                        description=Sample,
                        expectedrows=size(data.mean_epochs),
                        filters=tables.Filters(2)
                        )
                        
            data.mean_epochs = array(data.mean_epochs)
            conditions, samples, channels = shape(data.mean_epochs)
        
            sample_row = table.row
            for condition in xrange(conditions):
                for sample in xrange(samples):
                    for channel in xrange(channels):
                        sample_row['subject'] = data.subject
                        sample_row['condition'] = condition+1
                        sample_row['sample'] = \
                            sample-self.model.config.epoch_pre
                        sample_row['channel'] = \
                            data.channels_of_interest[channel]
                        sample_row['hemisphere_x'] = \
                            get_hemisphere(channel, axis='x', boolean=True)
                        sample_row['hemisphere_y'] = \
                            get_hemisphere(channel, axis='y', boolean=True)
                        sample_row['amplitude'] = \
                            data.mean_epochs[condition, sample, channel]
                        sample_row.append()
            
            table.flush()
                                
        
class Sample(tables.IsDescription):
    subject   = tables.StringCol(16)
    condition = tables.UInt8Col()
    sample    = tables.Int16Col()
    channel   = tables.UInt8Col()
    amplitude = tables.Float32Col()
    hemisphere_x = tables.BoolCol() # Left is True, Right is False
    hemisphere_y = tables.BoolCol() # Anterior is True, Posterior is False


class Experiment():
    def __init__(self):
        
        # Models
        self.config = Configuration()
        self.model = Model(self.config)
        
        self.model.analyze()
        
        # Views
        self.view = View(self.model)
        self.view.to_table(self.model.data)
        
        output_filename = self.config.output_directory + '/' + \
            self.config.name + ".output.txt"
        #data_table = self.view.data_table(self.model.data)
        data_table = self.view.print_table(self.model.data)
        
        save_table(output_filename, data_table)
        
        
        
        #self.view.plot_mmf()
        


class Data(object):
    
    def __init__(self, subject, config):
        
        self.subject = subject
        self.config = config
        
        self.load_data()
        self.load_triggers()
        self.channels_of_interest = self.config.subjects[self.subject]
    
    def load_data(self):
        """Loads an H5 data file containing MEG data."""
        
        print "Loading data ..."
        self.h5_filename = self.config.data_directory + self.subject + ".h5"
        self.h5_file = tables.openFile(self.h5_filename, mode = "r+")
        
    
    def load_triggers(self):
        """Create and fill triggers VLArray. Allows for ragged rows."""
        if "/triggers" in self.h5_file:
            self.h5_file.root.triggers.remove()
            
        self.triggers = self.h5_file.createVLArray(
                       where=self.h5_file.root, 
                       name='triggers',
                       atom=tables.Int32Atom(),
                       filters=tables.Filters(2)
                       )
                       
        print "Finding triggers ..."
        raw_data = self.h5_file.root.raw_data
        trigger_channels = self.config.trigger_channels
        for trigger_set in find_triggers(raw_data, trigger_channels):
            self.triggers.append(trigger_set)
        
        self.triggers.flush()
        return True
    
    def lowpass(self):
        """Lowpass filters the data."""

        # Create CArray for lowpassed data.
        if "/lowpass_data" not in self.h5_file:
            
            lowpass_data = self.h5_file.createCArray(
                where=self.h5_file.root, 
                name='lowpass_data', 
                atom=tables.Float32Atom(), 
                shape=shape(self.h5_file.root.raw_data),
                filters=tables.Filters(2)
                )
        
            print "Filtering ..."
            for channel in range(157):
                self.h5_file.root.lowpass_data[channel] = \
                    filters.lowpass(self.h5_file.root.raw_data[channel] * \
                    self.h5_file.root.convfactor[channel], 
                    sampling_frequency=self.config.sampling_frequency, 
                    lowpass_frequency=self.config.lowpass_frequency) 
    
    
    def epoch(self, data_array, apply_baseline=True):
        """Pulls out the epochs from the long data file."""
        self.front_sensors = [0, 41, 42, 83, 84, 107, 106, 105, 
                                104, 103, 102, 101, 100, 62, 61, 24, 23]
        self.loaded_channels = self.front_sensors + self.channels_of_interest
        
        channels = self.loaded_channels
        conditions = self.config.num_of_conditions
        expected_epochs = self.config.expected_epochs
        stimulus_pre = self.config.epoch_pre
        stimulus_post = self.config.epoch_post
        triggers = self.h5_file.root.triggers
        
        self.epoch_length  = stimulus_pre + 1 + stimulus_post # Include 0 point.
        
        epochs = zeros((conditions, self.epoch_length, len(channels), \
            expected_epochs))
        
        for (channel_index, channel) in enumerate(channels):
            print "Epoching channel %s ..." % channel
            the_chan = self.h5_file.getNode('/', data_array)[channel][:]
            for condition in range(conditions): 
                epoch_indices = range(len(triggers[condition]))
                random.shuffle(epoch_indices)
                epoch_indices = epoch_indices[:expected_epochs]
                
                for index, time in enumerate(epoch_indices):
                    epoch_start = triggers[condition][time] - stimulus_pre
                    epoch_end   = triggers[condition][time] + stimulus_post
                    the_epoch = the_chan[range(epoch_start, epoch_end + 1)]
                    epochs[condition, :, channel_index, index] = the_epoch
        
        
        
        ## This should work in the next version of pytables. 
        ## Uses fancy indexing.   
        #for condition in conditions: 
        #    print "Epoching condition %s ..." % condition
        #    for t in range(max_epochs):
        #        epoch_start = triggers[condition][t] - stimulus_pre
        #        epoch_end   = triggers[condition][t] + stimulus_post
        #        the_epoch = data[channels][range(epoch_start, epoch_end + 1)]
        #        epochs[condition, :, :, t] = the_epoch
        
        if apply_baseline:
            epochs = baseline(epochs.copy(), self.config.epoch_pre)
            
        self.save_epochs(epochs, data_array)
        
    def save_epochs(self, epochs, name):
        """ This needs cleaning up to avoid repitition."""
            
        print "Saving epochs ..."
        print "Shape:", shape(epochs)
        
        #if "/epochs_epochs" in self.h5_file:
        #    self.h5_file.root.epochs_epochs.remove()
        #
        #if "/epochs_filtered" in self.h5_file:
        #    self.h5_file.root.epochs_filtered.remove()
        #    
        #if "/raw_data_epochs" in self.h5_file:
        #    self.h5_file.root.raw_data_epochs.remove()
        #    
        #if "/lowpass_data_epochs" in self.h5_file:
        #    self.h5_file.root.lowpass_data_epochs.remove()
        
        array_name = name + "_epochs"
        if "/" + array_name not in self.h5_file:
            self.h5_file.createCArray(
                where=self.h5_file.root, 
                name=array_name, 
                atom=tables.Float32Atom(), 
                shape=shape(epochs),
                filters=tables.Filters(2))
        
        self.h5_file.getNode('/', array_name)[:] = epochs
        
        print "Done saving ..."
    
    def reject_epochs(self, method="std"):
        """
        Takes a set of epochs: conditions x samples x channels x epochs and
        masks out the rejected data points.
        """
        raw_data_epochs = self.h5_file.root.raw_data_epochs[:]
        lowpass_data_epochs = self.h5_file.root.lowpass_data_epochs[:]
        
        if method == "std":
            print "Rejecting epochs using standard deviation method ..."
            reject_fn = reject_by_std_method
        elif method == "diff":
            print "Rejecting epochs using difference method ..."
            reject_fn = reject_by_diff_method
        elif method == "entropy":
            print "Rejecting epochs using entropy method ..."
            reject_fn = reject_by_entropy
        else:
            raise ValueError('Rejection method "%s" not available.' % method)
        
        for condition in range(self.config.num_of_conditions):
            accepted, rejected = reject_fn(raw_data_epochs[condition, ...])
        
            lowpass_data_epochs[condition, :, :, rejected] = nan
        
        lowpass_data_epochs = ma.masked_array(lowpass_data_epochs, \
            isnan(lowpass_data_epochs))
        
    def mean_epochs(self):
        """Computes mean epochs."""
        
        epochs = self.h5_file.root.lowpass_data_epochs[:]
        self.mean_epochs = zeros((self.config.num_of_conditions, \
            shape(epochs)[1], len(self.channels_of_interest)))    
        for condition in range(self.config.num_of_conditions):
            self.mean_epochs[condition, :, :] = \
                mean(epochs[condition, :, len(self.front_sensors):, :], 2)
            

#class Channel(object):
#    def __init__(self, channel_number):
#        self.channel_number = channel_number
#        
#        left      = [  1,   2,   3,   4,   5,   6,   7,   8,   9,  11, 
#                      33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  
#                      43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
#                      58,  64,  67,  71,  73,  74,  75,  76,  77,  78,
#                      79,  80,  82,  83,  84,  85,  87,  88,  90,  91,  
#                     105, 106, 107, 108, 109, 110, 126, 127, 128, 129, 
#                     130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 
#                     140, 142, 150, 151]
#                     
#        right     = [ 10,  12,  13,  14,  15,  16,  17,  18,  19,  20, 
#                      21,  22,  23,  24,  25,  26,  27,  28,  29,  30, 
#                      31,  32,  53,  54,  55,  56,  57,  59,  60,  61,
#                      62,  63,  65,  66,  68,  69,  70,  72,  81,  86,
#                      89,  92,  93,  94,  95,  96,  97,  98,  99, 100, 
#                     101, 102, 103, 104, 111, 112, 113, 114, 115, 116, 
#                     117, 118, 119, 120, 121, 122, 123, 124, 125, 141, 
#                     143, 144, 145, 146, 147, 148, 149, 152, 153, 154, 
#                     155, 156]
#        
#        anterior  = [ ]
#        
#        posterior = [ ]
#        
#        if self.channel_number in left:
#            self.hemisphere_x = "left"
#        elif self.channel_number in right:
#            self.hemisphere_x = "right"
#        else:
#            raise ValueError("Channel %d is not a valid channel." % \
#                self.channel_number)
#            
#        if self.channel_number in anterior:
#            self.hemisphere_y = "anterior"
#        elif self.channel_number in posterior:
#            self.hemisphere_y = "posterior"
#        else:
#            raise ValueError("Channel %d is not a valid channel." % \
#                #self.channel_number)
        

if __name__ == "__main__":
    
    Experiment()

