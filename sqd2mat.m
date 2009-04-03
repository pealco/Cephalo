function [brain, refs] = sqd2mat(file, chans, trigger_chans, expected_triggers)
% SQD2MAT Read channels from .sqd file, filters it and stores it in a .mat file.
%
%    SQD2MAT(FILE, CHANS, TRIGGER_CHANS, EXPECTED_TRIGGERS) reads channels CHANS 
%    and TRIGGER_CHANS from .sqd file FILE and outputs a .mat file containing 
%    two arrays: DATA, containing continuous MEG data low-passed filtered at 
%    20 Hz and TRIGGERS containing the index of triggers for channels CHANS.
%
%    FILE
%    A MEG160 .sqd file.
%
%    CHANS
%    The channels that you want to read from the .sqd file. Use MEG160 notation,
%    not MATLAB (i.e., 0 is the first channel).
%
%    TRIGGER_CHANS
%    The channels which contain your triggers. Use MEG160 notation, not MATLAB.
%
%    EXPECTED_TRIGGERS
%    The number of triggers you expected to find in each channel.
%


% trigger_chans = [162, 163, 164, 165, 166, 167, 168, 169];
% expected_triggers = 100;

% These channels are loaded because they are the ones most likely to contain
% evidence that a blink has occured. Automatic epoch rejection looks only at
% these channels.
front_chans = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, ...
               61, 24, 23];

data_chans = [front_chans  chans];

info = sqdread(file, 'info');
sqd_length = info.SamplesAvailable;

for channel = data_chans,
   data{channel+1} = zeros(1,sqd_length); % Preallocate memory
end

for channel = data_chans,
    disp(['Reading channel ' num2str(channel) ' ...'])
    current_channel = sqdread(file,'Channels',[channel]);
    data{channel+1} = current_channel(:,1);
end

disp('Filtering ...')
for channel = data_chans,
   data{channel+1} = lowpassfilter(data{channel+1}, 1000, 20);
end

disp('Finding triggers ...')

triggers = zeros(expected_triggers,size(trigger_chans,2)); % Preallocate memory

for condition = 1:length(trigger_chans),
    tmp = find_trigger(file,trigger_chans(condition));
    triggers(:,condition) = tmp(1:expected_triggers);
end

%Some hackery to find the subject name.

[a,b] = strtok(file,'R');
subjectname = strrep(b,'.sqd','');

%[a,b,c] = mkdir(['matfiles']);

savefile = [file,'.mat']
save(savefile, 'data', 'triggers')

disp('Done with preprocessing!')
