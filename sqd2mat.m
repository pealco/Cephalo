function [brain, refs] = sqd2mat(file)

% MEG data channels: 0:156
% MEG ref  channels: 157, 158, 159
% Matlab data channels: 1:157
% Matlab ref  channels: 158:160

data_chans    = [0:10];
trigger_chans = [162, 163, 164, 165, 167, 168, 169, 170];
expected_triggers = 200;

info = sqdread(file, 'info');
sqd_length = info.SamplesAvailable;

for channel = data_chans,
   data{channel+1} = zeros(1,sqd_length); % Preallocate memory
end

for channel = 1:length(data_chans)/2,
    disp(['Reading channel ' num2str(channel*2-1) ' and ' num2str(channel*2) ' ...'])
    current_channel = sqdread(file,'Channels',[((channel*2)-1)-1, (channel*2)-1]);
    data{(channel*2)-1} = current_channel(:,1);
    data{(channel*2)}   = current_channel(:,2);
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
