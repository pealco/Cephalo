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
front_chans = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23];

data_chans = [front_chans chans];

info = sqdread(file, 'info');
sqd_length = info.SamplesAvailable;

for channel = data_chans,
   data{channel+1} = zeros(1,sqd_length); % Preallocate memory
end

disp(['Processing file ' file])

for channel = data_chans,
    disp(['Reading channel ' num2str(channel) ' ...'])
    current_channel = sqdread(file,'Channels',[channel]);
    data{channel+1} = current_channel(:,1);
end

disp('Finding triggers ...')

triggers = zeros(expected_triggers,size(trigger_chans,2)); % Preallocate memory

for condition = 1:length(trigger_chans),
    triggerline = sqdread(file,'Channels',trigger_chans(condition)); 
    temp = find(diff(triggerline) > max(diff(triggerline)*0.4)); % find triggers, correcting for any smeared across adjacent frames
    temp2 = temp(diff(temp)>1);
    temp2(length(temp2)+1) = temp(length(temp)); 
    currtrigger = sort(temp2);
    disp(['Found ' num2str(length(currtrigger)) ' triggers in channel ' num2str(trigger_chans(condition))])
    triggers_remaining = expected_triggers;
    for i = 1:length(currtrigger), % random sampling without replacement to get expected_triggers triggers from each trigger channel
        if rand()<(triggers_remaining/(length(currtrigger)-i))
            triggers(expected_triggers-triggers_remaining+1,condition) = currtrigger(i);
            triggers_remaining=triggers_remaining-1;
        end;
    end;
    disp(['Kept ' num2str(expected_triggers-triggers_remaining) ' triggers'])
    triggers(:,condition) = currtrigger(:)
end



% Save the mat file.
savefile = [file(1:end-4),'.mat']
save(savefile, 'data', 'triggers')

disp('Done with preprocessing!')
