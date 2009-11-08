import ConfigParser
import sys

class Experiment():
    def __init__(self, config_file):
        config = ConfigParser.RawConfigParser()
        config.read(config_file)

        # Experiment metadata
        self.experiment_name = config.get("Experiment", "name")
        self.experimenter = config.get("Experiment", "experimenter")
        self.experiment_type = config.get("Experiment", "type")

        if self.experiment_type.lower() == "mmf":
            # Experiment parameters
            self.standards = eval(config.get("Parameters", "standards"))
            self.deviants  = eval(config.get("Parameters", "deviants"))

        # Epoch parameters
        self.expected_epochs = config.getint("Epochs", "expected_epochs")
        self.epochs_pre  = config.getint("Epochs", "epochs_pre")
        self.epochs_post = config.getint("Epochs", "epochs_post")
        
        # Subject parameters
        subjects = config.items("Subjects")
        subjects = [(subject[0].upper() + ".h5", eval(subject[1])) for subject in subjects]
            

if __name__ == "__main__":
    
    config_file = sys.argv[1]
    experiment = Experiment(config_file)
    
    

