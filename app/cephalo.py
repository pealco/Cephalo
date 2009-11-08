import sys
import yaml
import tables.

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
            
        if 'subjects' not in config or config['subjects'] == {}:
            raise ValueError("No subjects specified.")
        else:
            self.subjects = config['subjects']
        
    def load_data(self):
        pass
        
        
        
class View():
    pass
        
class Experiment():
    def __init__(self):
        self.model = Model()
        self.view = View()
        
        self.model.get_config()
        self.model.load_data()
    

exp = Experiment()

print exp.model.deviants