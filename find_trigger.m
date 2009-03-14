function trigger = find_trigger(filename, channels)
% trigger = find_trigger(filename, channels)
% to find trigger for the input channels
% Input: sqd filename and channels
% Output: triggers for each channels as sample index
% 
% Trigger is form High to Low now
% You may choose different way, like, from low to high or in the middle
% 
% example
%       filename= 'C:\awang\MEG\RawData\R0292 ModBand (1.30.04)\R0292.ModBand.1.30.04.Run2.sqd';
%       trigger = find_trigger(filename, [160:171])  

[data,info] = sqdread(filename,'Channels',channels);

threshold = (25-1) /info.InputGain *2;
% changes from Ray's sqdread file

for iTrigger = 1:length(channels)
    
    % low to high
    %trigger(:,iTrigger) = find(diff(data(:,iTrigger)) >  threshold);
    
    % same as meg160: high to low
    trigger(:,iTrigger) = find(diff(data(:,iTrigger)) < -threshold);
    %trigger{iTrigger} = find(diff(data(:,iTrigger)) < -threshold);

%    disp('              ')
    %fprintf('---- For trigger:  %3g ---- Triggers Found: %3g \n',channels(iTrigger),length(trigger{iTrigger}));
%     fprintf('---- For trigger:  %3g ---- Triggers Found: %3g \n',channels(iTrigger),length(trigger(:,iTrigger)));
%    disp('              ')

    %disp(['For trigger: ' num2str(channels(iTrigger))])
    
end;