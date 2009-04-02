function [brain, refs] = sqd2mat(file, interesting_chans)

% MEG data channels: 0:156
% MEG ref  channels: 157, 158, 159
% Matlab data channels: 1:157
% Matlab ref  channels: 158:160

% These channels are loaded because they are the ones most likely to contain
% evidence that a blink has occured. Automatic epoch rejection looks only at
% these channels.
front_chans    = [0, 41, 42, 83, 84, 107, 106, 105, 104, 103, 102, 101, 100, 62, 61, 24, 23];
data_chans = [front_chans  interesting_chans];

% These should be changed based on what triggers you are using in your
% experiment. Use MEG160 notation, not MATLAB (i.e., 0 is the first
% channel).
trigger_chans = [162, 163, 164, 165, 166, 167, 168, 169];

% This should be changed based on how many triggers you expect to find.
expected_triggers = 100;

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

disp('Filtering and decimating ...')
for channel = data_chans,
   data{channel+1} = lowpassfilter(data{channel+1}, 1000, 20);
   %data{channel+1} = lowpassfilter(data{channel+1}, 1000, 20);
end

disp('Finding triggers ...')

triggers = zeros(expected_triggers,size(trigger_chans,2)); % Preallocate memory

for condition = 1:8, % TODO remove hardcoded 8
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
